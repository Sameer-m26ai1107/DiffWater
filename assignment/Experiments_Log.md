# Experiments and ideas log (Run 0 phase)

A record of what we tried on the way to Run 0, what happened, and what we decided. It is written so a teammate can see why the setup looks the way it does, and avoid repeating a dead end. The result tables are in `Run0_Report.md`.

Dates are 2026. "Status" is one of: **adopted**, **rejected**, **not applied** (considered, left for later), **failed** (tried, did not work).

---

## 1. Getting the original repo to run (UW-DiffPhys)

| Idea | What happened | Status |
|---|---|---|
| `conda env create -f environment.yml` | Failed with `PackagesNotFoundError`. The file is a `conda env export` from Linux x86_64 with CUDA builds, so exact-build pins do not exist on macOS or Colab. | failed |
| Fix: create a fresh env and install the top-level packages, or use Colab's preinstalled torch | Not pursued further because of the checkpoint problem below. | not applied |
| Download the authors' pretrained checkpoint from the README's Google Drive link | The link redirects to a Google sign-in page. It is restricted, not a quota problem. We could not get access. | failed |

## 2. Audit of a colleague's earlier Colab run

We read `FM_Assignment.ipynb`, a from-scratch training attempt of UW-DiffPhys on a Colab T4.

- It trained at about 1.3 s per step, 2573 steps per epoch, about 55 min per epoch.
- It stopped at step 6000 (epoch 2) with no traceback. `n_epochs` was probably very large, so it did not finish by design. It was most likely cut off by the Colab session.
- The "checkpoints" in its `ckpts/` folder were about 900 KB each. Those were Google HTML error pages, not weights. The run therefore did **not** produce usable checkpoints, and a failed download had been mistaken for a saved model.
- Its data included Underwater ImageNet (5550 + 2185 + 3700 = 11,435 pairs), while the declaration lists Dark and Scenes only.
- A repo bug: `datasets/underwater.py` uses an unsorted `glob.glob`, so raw/reference pairing is not guaranteed.

## 3. Options after losing the checkpoint

| Option | Reasoning | Status |
|---|---|---|
| Train UW-DiffPhys from scratch on a T4 | At about 55 min per epoch and the number of epochs a diffusion model needs, this is far outside our time budget. | rejected |
| Wait for the Drive owner to grant access | Access was not coming and we had no time to wait. | rejected |
| Switch to another pretrained underwater diffusion model | Searched the web. Chose **DiffWater** (Guan-MS/DiffWater): conditional DDPM, paired enhancement, 256 px, open code, Apache-2.0, public weights folder, same kind of θₜ = ᾱₜ schedule. | **adopted** |

The team is working on the assumption that a model change is allowed. It has not been formally approved by the instructor. See open items in the report.

## 4. Checkpoint handling (several wrong turns)

| Problem | Cause | Fix |
|---|---|---|
| We believed checkpoints would be about 14 GB. | The 14 GB figure was GPU memory for fine-tuning another model. | DiffWater's generator file is about 593 MB, and only `_gen.pth` is needed for inference. The `_opt.pth` (about 1.16 GB) matters only for resuming training. |
| `/content/diffwater_ckpt` was not visible in Drive. | That was Colab's local disk, not Drive. | Notebook now uses `MyDrive/DW`, which survives disconnects. |
| The shared Drive folder has `UIEB` and `LSUI` subfolders, not loose files. | The authors keep one model per training dataset. | The notebook stops if checkpoints sit in several folders and selects one by file name. |
| We copied `I860000_E607_gen.pth` into a folder named `LSUI`. | That file is probably the UIEB model, so the folder name was misleading. | Re-copied the real LSUI file and select by name: `CKPT_NAME = "I390000_E78_gen.pth"`. |
| Google Drive "Make a copy" does not work on folders. | Drive limitation. | Copy files individually in the browser, then load from `MyDrive/DW`. |

## 5. Test data (EUVP)

| Step | Result |
|---|---|
| Use a colleague's Drive copy of EUVP | No access to that Drive. `NameError: DRIVE_EUVP` appeared because a later cell depended on an optional earlier cell. Fix: placeholders in the settings cell. |
| Download EUVP from Kaggle (`pamuduranasinghe/euvp-dataset`) | Works. The notebook prints the folder tree and the sibling folders with equal counts to help choose. |
| First pick: `EUVP/Unpaired` | **Wrong.** raw 3205, ref 3140, 0 matched filenames. Unpaired folders contain unrelated images. |
| Second pick: `EUVP/test_samples/Inp` and `GTr` | 515 and 515, 515 matched by filename. We confirmed visually that the left images are degraded and the right ones are better. **Adopted.** |
| Pairing | Pairs matched by filename stem, then written with identical zero-padded names so the repo's sorted-order pairing is correct. |

Open question: which EUVP subsets `test_samples` came from. It may include ImageNet-derived images.

## 6. Making Run 0 reproducible without editing the authors' code

| Idea | Outcome | Status |
|---|---|---|
| Run the repo's `test.py` as is | It has **no seed**, so repeated runs differ. | rejected |
| Edit `test.py` to add a seed | Works, but changes the authors' code. | rejected |
| Wrapper `run0_test.py` that seeds Python, NumPy and PyTorch (CPU and CUDA) and then runs the unmodified `test.py` via `runpy` | Clean. The repo stays untouched. | **adopted** |
| Compute metrics with the repo's `eval.py` | Per our reading, it compares input with target and not output with target, and its SSIM is non-standard. | rejected |
| Compute PSNR and SSIM with scikit-image on output vs target | Standard and transparent. | **adopted** |

## 7. Checks before spending GPU hours

- **Strict checkpoint load.** Loaded the generator with strict matching. 155.3 M parameters, no missing or extra keys.
- **Memory.** Peak about 0.89 GB at batch size 1, so a T4 has a lot of headroom.
- **Timing.** The dry run measured 137.3 ms per denoising step, which predicted about 275 s per image. The real run was 6.47 it/s, about 310 s per image (13% slower than predicted). Plan with about 5.2 min per image, not 4.6.
- **Schedule check.** ᾱ₁ = 0.99999900, ᾱ_T = 4.386e-5, strictly decreasing and inside (0, 1). ᾱₜ² is also valid. This is the basis for using x = 2.00 later.

## 8. Choosing how many test images

| Option | Cost per run | Verdict |
|---|---|---|
| 5 images | about 26 min | Used for the first trial only. |
| 30 images | about 2.6 h | **Adopted.** The team's cap was 50. |
| 100 images | about 8.6 h | Too long. |
| 515 images (all) | about 45 h | Not possible. |

The 30-image set contains the 5-image trial set, since the selection is the first N of the same seeded shuffle.

## 9. Ideas to speed up sampling (not applied)

Proposed as ways to cut the 5 min per image. None was used, because anything adopted must be identical across Run 0, A and B, and Run 0 is already done at full fidelity.

- Half precision (fp16) for the UNet only.
- Strided sampling (fewer than 2000 steps).
- Batch size above 1 for inference.
- A faster GPU (A100) or Colab Pro.

Revisit these for the intermediate-epoch samples in A and B, where the budget is tighter. If used, apply them to both runs and document them.

## 10. Keeping a long Colab job alive

| Problem | What we did | Result |
|---|---|---|
| `/content` is wiped when the runtime disconnects. | Ran a background thread in the notebook that copies new result PNGs to Drive every 120 s (skipping files modified in the last 5 s). | Worked. The Drive folder name matches the local experiment folder name, and all 30 sets were present afterwards. |
| The runtime disconnected in the morning, after the run finished. | The notebook output was lost, so Steps 8 and 9 did not run in that session. | We recomputed metrics from the Drive copies with a standalone cell (README, section 6). |
| Laptop sleep and tab closure. | Plugged in, kept the Mac awake with `caffeinate -dis`, kept the tab open. | Run finished in 155.2 min. |

Lesson: write results to Drive as they are produced. Do not rely on a final "save" cell.

## 11. Mistakes and corrections worth remembering

- **Wrong EUVP folders** (Unpaired). Caught by the zero-match assertion. Always check the match count before running.
- **Mislabelled checkpoint folder** (UIEB model in a folder called LSUI). Select checkpoints by file name and say which one was used.
- **Saved "input" is not the raw image.** The repo's loader applies colour channel compensation before the model, and `test.py` saves that compensated input. Our "input vs reference" column is therefore compensated-vs-reference. We initially assumed it was raw.
- **UNet input.** We first wrote that the UNet takes a continuous noise level. The code shows it takes the integer timestep t. Corrected in the report. This matters for how the schedule change is implemented in Runs A and B.
- **Trajectory grid.** We first suspected that the last grid frame differed from `output.png`. By the code they are the same tensor (the last saved frame is t = 0). We could not tell from a visual comparison, so do not judge by eye.
- **Editing the notebook while it was running.** The generated file on disk diverged from the live Colab copy. We stopped editing it and gave fixes as snippets. Because of this, the notebook file in this folder does not contain every change that was made in the live copy (README, section 7).

## 12. Findings that came out of the experiments

1. The pretrained DiffWater LSUI checkpoint, applied to EUVP test pairs, scores 17.72 dB PSNR and 0.732 SSIM. That is below the compensated input compared with the same reference (19.85 dB, 0.779).
2. It improves the images that start furthest from the reference (inputs 6, 15, 27) and degrades many that start close to it.
3. The 30-image, single-seed design gives a standard error of 0.81 dB on the paired PSNR difference. This limits how finely A and B can be told apart.
4. About 5.2 min per full-length sample is the main cost driver for every later run.

## 13. Open items

- Instructor approval of the model change and an updated declaration.
- Paper page and line evidence for what DiffWater was pretrained on.
- Composition of EUVP `test_samples`.
- Visual review of more than one Run 0 sample.
- Decide the fine-tuning budget (steps per epoch, epochs) and sampling settings for the intermediate-epoch samples, identical for A and B.
- Implement the modified schedule (exponent x as a named constant at the top of the fine-tuning script, `# MODIFIED` and `# ADDED` markers), per-image seeding, the CSV log (`epoch`, `train_loss`), samples at 5 equally spaced epochs, and 5-timestep trajectories.
