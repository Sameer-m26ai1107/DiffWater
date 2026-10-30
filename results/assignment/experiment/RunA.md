---
run: A                 # 0 | A | B
tag: main            # main | legacy | variant tag
status: done
owner:
account:
started: 2026-10-29 07:59 UTC
finished: 2026-10-30 19:42 UTC
gpu: Tesla T4
torch: 2.11.0+cu130
python: 3.13.16
diffwater_commit: 7db68f34060bbf1d7c5b8153664fb16a3dcda1ae
finetune_md5: 38c97203e8ccafdfb80cb2be74b0bb3a
exponent: 1
epochs: 10
batch_size: 4
lr: 1e-5
seed: 1234
n_train: 800
train_dark:
train_scenes:
train_fingerprint: 6a9f33de995c
split_fingerprint: f8cc4714a30c
n_eval: 30
checkpoint: I390000_E78_gen.pth
train_minutes:
eval_minutes:
total_minutes: 280.1
final_train_loss: 0.06355
psnr_out_mean: 14.360
psnr_out_std: 3.020
ssim_out_mean: 0.7701
ssim_out_std: 0.1117
psnr_in_mean: 20.647
ssim_in_mean: 0.8887
results_dir: Drive: FoundationModel-Assignment/runs/RunA ; local copy data/RunA/
---

# Run A: fine-tune with the original schedule (exponent 1)

## Purpose
Fine-tune the pretrained checkpoint on the EUVP training subset with the original noise schedule θₜ = ᾱₜ. Separates the effect of fine-tuning on our data (A minus Run 0) from the effect of the schedule (B minus A).

## Setup actually used
Anything that differs from `EXPERIMENT.md`, and which notebook cells were run. Write `as specified` if nothing differs.

## Observations
- Per-epoch training loss: epoch 1 0.05631, epoch 2 0.05745 (L1 on predicted noise, averaged over 200 steps). The per-step loss swings between about 0.05 and 0.065 because every step draws random timesteps and the difficulty depends on the timestep. A flat curve over two epochs is expected for a fine-tune of an already trained model and is not a sign of a problem. Read the trend over all 10 epochs, not between two of them.

## Issues and fixes
In order. Include exact error text if short.

## Deviations from the protocol
- Run A was interrupted by a Colab disconnect and **resumed from `resume.pt` at epoch 8** (2026-10-29 12:58 UTC, same account, same `finetune.py` md5, same command). Epochs 1 to 10 were trained in session 1 (its `run.log` lines end at 09:42:23), but `resume.pt` on Drive was the epoch-8 save, so epochs 9 and 10 were trained again in session 2, together with final-evaluation images 4 to 24. Method and settings are unchanged. Weights and Adam state were restored; per-epoch seeds are `seed + epoch`, so the data order of epochs 9 and 10 is the one an uninterrupted run would use. Run B is expected to run uninterrupted; GPU non-determinism makes bit-identical results impossible in either case.
- **Session 3 (2026-10-30, 18:51 UTC):** the remaining final-evaluation images (25 to 30) are produced in the Google account that ran Run B, with the Run A folder (shared by the Run A account, added as a Drive shortcut named `RunA`) used directly as `--out_dir`. The script resumed from `resume.pt` at epoch 10. Same T4 class, same script md5, same DiffWater commit, same data fingerprints (preflight OK); only the account differs. Weights, seeds and the 24 images already written are unchanged. This session wrote image 25 and was then stopped by Colab (resource exhausted, owner's report); images 26 to 30 are still missing.
- **Session 4 (2026-10-30, 19:10 UTC):** a further resume from epoch 10 in Run 0's Google account (owner's statement), again with the shared Run A folder used as `--out_dir`. It started at image 26, so image 25 from session 3 had reached Drive. Everything else as in session 3.

## Log
Append-only. Format: `- YYYY-MM-DD HH:MM UTC [who] TYPE  text`. Types: START, PROGRESS, ISSUE, FIX, DECISION, RESULT, NOTE, DONE.

- 2026-10-29 [collator] NOTE  File created from TEMPLATE_RUN.md. Nothing has been run yet.

- 2026-10-29 07:34 UTC [collator] RESULT  Step 6a benchmark (source: `data/RunA/cell_output.txt`, "Step 6"): `schedule OK` exponent 1.0, T 2000, abar_last 4.386e-05. batch 1: 0.35 s/step, peak 3.3 GB; batch 2: 0.62 s/step, 4.6 GB; batch 4: 1.14 s/step, 7.4 GB; batch 8: 1.66 s/step, 13.3 GB.
- 2026-10-29 [collator] NOTE  Step 6b printed 277 min per run because `S_PER_STEP` was left at the default 1.6. With the measured 1.14 s/step at batch 4, training is 2000 × 1.14 s ≈ 38 min and the total is about 261 min (38 + 5 saves + 62 samples + 156 final evaluation), computed by the collator.
- 2026-10-29 [collator] NOTE  Step 4 screenshot (`data/RunA/Screenshot 2026-10-29 at 1.14.51 PM.png`): abar A / B at t=250: 0.8545 / 0.7301; t=500: 0.5339 / 0.2851; t=1000: 0.0814 / 0.0066. Matches the Step 2 numbers. Step 5 demo: buffer 0.81, 0.25 became 0.90, 0.50 after `load_state_dict`.
- 2026-10-29 07:35 UTC [collator] ISSUE  Step 7 smoke test failed for both `--run B` and `--run 0`: `RuntimeError: Error(s) in loading state_dict for GaussianDiffusion: size mismatch for betas: copying a param with shape torch.Size([2000]) from checkpoint, the shape in current model is torch.Size([20])` (same for the 11 other schedule buffers), raised in `build_model`. Cause: smoke mode built the model with T=20 but the checkpoint stores the buffers with T=2000. Only `--smoke` is affected; the benchmark (T=2000) loaded the checkpoint without error.
- 2026-10-29 [collator] FIX  `finetune.py` smoke mode now applies T=20 after loading (D-013). New md5 `38c97203e8ccafdfb80cb2be74b0bb3a`. Re-upload the script and re-run Step 7.

- 2026-10-29 07:52 UTC [collator] RESULT  Step 7 smoke test passed after the fix (source: `data/RunA/smoke_test_after_fix.txt`). `--run B`: `schedule OK` exponent 2.0, T 20; 5 epochs, samples at every epoch, `resume.pt`, `final_eval/`, `train_log.csv`, `train_steps.csv`, `metrics.csv` all written; `ALL DONE`. `--run 0`: `schedule OK` exponent 1.0, no training, 2 images evaluated, `ALL DONE`. The garbage PSNR (about 10 dB) is expected at T=20 and means nothing. Both runs report the same input-vs-reference values (PSNR 17.465, SSIM 0.8675) for the same 2 images, consistent with an identical test set.

- 2026-10-29 (time not recorded) [owner] START  Step 8 launched with RUN="A" in a Colab session, outputs to `FoundationModel-Assignment/runs/RunA` on the owner's Drive. Command (source: Step 8 cell output): `python -u /content/finetune.py --run A --repo_dir /content/DiffWater/DiffWater --ckpt_prefix /content/drive/MyDrive/DW/LSUI/I390000_E78 --train_root /content/euvp_train --eval_root /content/euvp_test --out_dir /content/drive/MyDrive/FoundationModel-Assignment/runs/RunA --epochs 10 --batch_size 4 --n_eval 30 --n_samples 3`. Learning rate and seed were not passed, so the script defaults apply (1e-5 and 1234); to be confirmed from the first line of `run.log`.
- 2026-10-29 [collator] DECISION  Batch size 4 confirmed by the owner (D-010).

- 2026-10-29 07:59 UTC [collator] RESULT  Run started (source: `data/RunA/RunA_stdout.log`, the Colab-local stdout copy of the log). `run=A exponent=1.0`, `epochs 10, batch_size 4, lr 1e-05, seed 1234, n_samples 3, n_eval 30`, `train pairs: 800`, `schedule OK: exponent 1.0, T 2000, abar_last 4.386e-05`. Front matter `started`, `lr`, `seed`, `n_train` filled from these lines.
- 2026-10-29 08:01 UTC [collator] PROGRESS  Epoch 1: step 50/200 loss 0.0638 (1.19 s/step), step 100/200 loss 0.0548 (1.23 s/step). Slightly slower than the benchmark (1.14 s/step), about 5 to 8 percent; the data loader's colour compensation runs on the CPU. At 1.23 s/step training takes about 41 min, so the expected total is about 4.5 h (end near 12:30 UTC).
- 2026-10-29 [collator] NOTE  The stdout log also contains `UserWarning: Conversion from CIE-LAB, via XYZ to sRGB color space resulted in N negative Z values that have been clipped to zero` from `ColorChannelCompensation.py`. Harmless; the same warning appeared in the first Run 0.

- 2026-10-29 08:23 UTC [collator] PROGRESS  Epochs 1 and 2 done (source: `data/RunA/monitor_0823UTC.txt`). train_loss per epoch: 0.05631, 0.05745 (not a decrease; see Observations). Epoch 1 took 4.1 min, epoch 2 4.2 min (1.24 to 1.27 s/step). `resume.pt` saved at 08:07:58, 13 s after the epoch ended.
- 2026-10-29 08:23 UTC [collator] PROGRESS  Epoch 2 samples written: 3 images at about 302 s each (6.6 it/s), 903 s in total. Mean over those 3 images: PSNR 14.10, SSIM 0.780 (output vs reference). Only 3 images, no baseline for the same images yet (Run 0 not done), so this number is not interpretable on its own. `samples/epoch_02/metrics.csv` on Drive also holds the input-vs-reference values for the same 3 images.
- 2026-10-29 08:23 UTC [collator] NOTE  Projected finish: each even-epoch cycle (2 epochs of training, save, 3 samples) takes about 23.7 min; epoch 10 samples done near 09:57 UTC; the remaining 27 final-evaluation images at about 5.0 min each end near 12:15 UTC.

- 2026-10-29 [collator] NOTE  ENV block pasted by the owner: `gpu: Tesla T4`, `torch: 2.11.0+cu130`, `python: 3.13.16`, `diffwater_commit: 7db68f34060bbf1d7c5b8153664fb16a3dcda1ae`, `finetune_md5: 38c97203e8ccafdfb80cb2be74b0bb3a`. The md5 equals the frozen value, so Run A used the fixed script (D-013) and there is no deviation. Front matter `gpu`, `torch`, `python`, `diffwater_commit`, `finetune_md5` filled.

- 2026-10-29 (time not recorded) [owner] ISSUE  The Colab GPU runtime disconnected because it had no active job: the background launch (`subprocess.Popen(start_new_session=True)`, cell returned immediately) does not count as activity for Colab's idle check. Epoch reached and disconnect time not yet reported; to be read from `runs/RunA/run.log` and `resume.pt` on Drive.
- 2026-10-29 [collator] NOTE  `finetune.py` resumes from `out_dir/resume.pt` (saved at epochs 2, 4, 6, 8, 10) and skips sample and final-eval images already on Drive (source: `finetune.py` lines 326 to 421). Loss at most the work since the last save. Proposed fix: relaunch with the same command, but as a foreground cell that stays busy (no change to any frozen setting). If the job resumes, log the resume epoch and add it under "Deviations from the protocol" as a resume, not a change of method.

- 2026-10-29 12:57 UTC [owner] START  Session 2: re-ran setup cells, relaunched the identical command as a foreground cell (`!python -u ... | grep --line-buffered -v ...`) in the same account (source: pasted run.log lines, 12:57:55 to 12:58:58).
- 2026-10-29 12:58 UTC [collator] RESULT  `resumed from epoch 8` (12:58:45), then `schedule OK` with exponent 1.0, T 2000, abar_last 4.386e-05 (unchanged). So `resume.pt` on Drive was the epoch-8 save; epochs 9 and 10 of session 1 were not saved and are retrained. Epoch 8 samples were taken by session 1 before the disconnect.
- 2026-10-29 12:58 UTC [collator] RESULT  `epoch 8 sample PSNR 14.16 SSIM 0.762` (3 images, output vs reference), printed 13 s after the schedule check. Interpretation, not stated in the log: 13 s is far too short to sample 3 images (about 300 s each at epoch 2), so the three epoch-8 images already existed and were skipped; the line is the metrics recomputed from the files on Drive. Time of the disconnect was not reported.
- 2026-10-29 12:59 UTC [collator] NOTE  Projection from session-2 timings (about 4.2 min per epoch, 903 s for 3 samples, about 5.0 min per final-eval image): epochs 9 and 10 done near 13:07, epoch-10 samples near 13:23, the other 27 final-eval images near 15:40 UTC. Estimate only.
- 2026-10-29 [collator] RESULT  Step 3 output of session 2, read from the owner's as-run notebook (`RunAB_Finetune_Guide_v2.ipynb`, Step 3 cell): `underwater_dark` trainA/trainB 5550/5550 matched 5550; `underwater_scenes` 2185/2185 matched 2185; training pool 7700 pairs after removing 5 exact duplicates and 0 near-duplicates of a test image; `test split identical to the one saved on Drive`; **`split fingerprint: f8cc4714a30c`**; `wrote 800 train pairs and 30 test pairs`. Front matter `split_fingerprint` filled.
- 2026-10-29 [collator] NOTE  The fingerprint cell below Step 3 (train counts and `train fingerprint`) has no output in the as-run notebook, so the train fingerprint of session 2 (epochs 9 and 10) was not recorded; `train_dark`, `train_scenes` and `train_fingerprint` stay blank in this file. The script and seed are the same and the draw is deterministic, but that is an argument, not an observation. Run the fingerprint cell once Run A has finished (the data is still in `/content` in that session) and paste the line.

- 2026-10-29 13:08 UTC [collator] PROGRESS  Session 2, epochs 9 and 10 (source: `data/RunA/cell_output.txt`): 1.38 to 1.40 s/step (session 1 ran 1.24 to 1.27; benchmark 1.14), 4.6 min per epoch. train_loss epoch 9 0.06070, epoch 10 0.06355. `resume.pt` saved at epoch 10 at 13:08:19.
- 2026-10-29 13:24 UTC [collator] RESULT  Epoch-10 samples: 321 s per image; mean over the 3 images PSNR 13.91, SSIM 0.771 (output vs reference). For comparison, the same 3 images gave PSNR 14.10 / SSIM 0.780 at epoch 2 and 14.16 / 0.762 at epoch 8. No Run 0 baseline for these images yet, so no reading of these numbers beyond 'they are in the same range'.
- 2026-10-29 13:51 UTC [collator] PROGRESS  Final evaluation: images 1 to 3 reused from the epoch-10 samples (same weights, same seeds); 4/30 done at 13:29:43, 5/30 at 13:35:03, 6/30 at 13:40:24, 7/30 at 13:45:46, 8/30 at 13:51:07 (5.3 min per image). 22 images remain, estimated 117 min, so the end is near 15:49 UTC.
- 2026-10-29 [collator] NOTE  train_loss at epochs 1, 2, 9, 10: 0.0563, 0.0575, 0.0607, 0.0636, a rise of about 0.007. Within one epoch the 50-step means range from 0.055 to 0.070 (random t), so an epoch mean has a noise of roughly 0.003 (estimate); the rise is borderline, not clearly real. Epochs 3 to 8 are in `train_log.csv` on Drive and have not been copied yet; read the whole curve before saying anything about it. The test-set metric is what decides, not the training loss.

- 2026-10-29 15:16 UTC [collator] PROGRESS  Final evaluation reached image 24/30 at 15:16:40 (112.3 min elapsed), 5.3 to 5.4 min per image (source: `data/RunA/cell_output.txt`). That is the last line of the log: images 1 to 24 are done (1 to 3 reused from epoch 10), **images 25 to 30 are missing**.
- 2026-10-29 (time not recorded) [owner] ISSUE  Colab reported the session as disconnected for inactivity while the tab was open and the cell was running. Trying to resume afterwards gave 'GPU exhausted' (owner's words; the exact message was not pasted). Run B, started later with the same launch cell, was still running at that time, so the cause is not the launch method; the collator suspects this account's GPU usage limit (this account had by then used the T4 for about 1.7 h in session 1 and 2.3 h in session 2), which is a guess.
- 2026-10-29 [collator] NOTE  State needed to finish: `resume.pt` (epoch 10, saved 13:08:19 UTC) plus `samples/` and `final_eval/` on Drive. A resume loads epoch 10, skips epochs, finds the epoch-10 samples and final-eval images 1 to 24 already written, samples images 25 to 30 (about 32 min), then computes `eval_metrics.csv` and writes `final_gen.pth`. Estimated 40 min of T4 in total. Decision pending: D-016.

- 2026-10-29 [owner] ISSUE  Tried to resume in the original account (option 1 of D-016): Colab answered 'You cannot currently connect to a GPU due to usage limits in Colab.' So the disconnect in this account was a usage limit, not (only) idleness, and the account cannot get a T4 for now (no time given). Run A stays `interrupted`; images 25 to 30 of the final evaluation are still missing.

- 2026-10-30 18:51 UTC [owner] START  Session 3: Run A relaunched in the account that ran Run B, using the v3 launch cell with `RUN = "A"` (source: `data/RunA/new_cell_output.txt`). Preflight: `md5 38c97203... OK`, `commit 7db68f34... OK`, `train_fp 6a9f33de995c OK`, `split_fp f8cc4714a30c OK`. Command as in session 2 with `--out_dir .../runs/RunA` (the shortcut).
- 2026-10-30 18:52 UTC [collator] RESULT  First lines of session 3: `run=A exponent=1.0`, `train pairs: 800`, `eval pairs available: 30`, **`resumed from epoch 10`** (18:52:00), `schedule OK: exponent 1.0, abar_last 4.386e-05, T 2000`. So `resume.pt` (epoch 10) was found through the shortcut and the schedule is the original one. Front matter `train_fingerprint` filled from this session's preflight (it equals the frozen value; sessions 1 and 2 did not record theirs).
- 2026-10-30 [collator] NOTE  Expected from here (estimate): the epoch-10 samples are only rescored (a few seconds, the line should read PSNR 13.91 SSIM 0.771); training is skipped; images 1 to 24 already exist and are skipped silently; images 25 to 30 are sampled at about 5.3 min each, so about 32 min, ending near 19:25 UTC; `eval_metrics.csv` is then written for all 30 images and `final_gen.pth` saved.

- 2026-10-30 18:52 UTC [collator] RESULT  Session 3, continued (source: `data/RunA/new_cell_output.txt`, updated 00:28 IST): `18:52:13 epoch 10 sample PSNR 13.91 SSIM 0.771` (13 s after the schedule check, equal to the value printed in session 2, so the epoch-10 files and weights were read correctly through the shortcut), then `18:57:33 final eval 25/30 done (5.3 min elapsed)`. That is the last line of the file.
- 2026-10-30 ~18:58 UTC [owner] ISSUE  Colab stopped this session with 'resource exhausted' (owner's words; the message itself is not in the pasted file). The Run B account had only a little quota left, which this session used up (it ran about 7 minutes of sampling after setup). Run A is `interrupted` again: images 1 to 25 are done if image 25's four files reached Drive (to be checked: `final_eval/idx25_{input,output,target,traj}.png`), images 26 to 30 are missing, about 27 min of T4 at 5.3 min per image plus about 2 min to load.
- 2026-10-30 [collator] NOTE  What this attempt proved: resuming from `resume.pt` through a shortcut into another account's shared folder works, the epoch-10 rescore matches, and the run writes new images into that folder. It does not prove the final steps (`eval_metrics.csv`, `final_gen.pth`) will write; those have not run yet.

- 2026-10-30 19:10 UTC [owner] START  Session 4: relaunched with the v3 launch cell, `RUN = "A"` (source: `data/RunA/session4_cell_output.txt`, pasted in chat). Preflight `md5`, `commit`, `train_fp 6a9f33de995c`, `split_fp f8cc4714a30c` all OK. `resumed from epoch 10` at 19:11:48 (81 s after start, a slower load than session 3's 32 s), `schedule OK` exponent 1.0, `epoch 10 sample PSNR 13.91 SSIM 0.771` at 19:12:15.
- 2026-10-30 19:28 UTC [collator] PROGRESS  Final evaluation: 26/30 at 19:17:48 (5.5 min elapsed), 27/30 at 19:23:19, 28/30 at 19:28:50 (16.6 min elapsed); 5.5 min per image, slightly slower than the 5.3 of the earlier sessions. There is no line for image 25: it was written in session 3 and is skipped. Estimate: 29/30 near 19:34, 30/30 near 19:40 UTC, then the `FINAL` line, `eval_metrics.csv`, `final_gen.pth` and `ALL DONE`.

- 2026-10-30 19:42 UTC [collator] RESULT  **Run A finished** (source: `data/RunA/run.log`, `eval_metrics.csv`): final-evaluation images 29 and 30 at 19:34:21 and 19:39:51; `FINAL  PSNR 14.360  SSIM 0.7701  over 30 images  (input vs ref: PSNR 20.647 SSIM 0.8887)`, then `ALL DONE` at 19:42:35. Recomputed from `eval_metrics.csv` (30 rows, idx 1 to 30): PSNR out 14.360 ± 3.020, SSIM out 0.7701 ± 0.1117 (sample standard deviation); means equal the `FINAL` line. The input-vs-reference columns are identical in Run 0, Run A and Run B for all 30 images, so the three runs scored the same images in the same order. `run_config.json`: run A, exponent 1.0, epochs 10, batch 4, lr 1e-05, seed 1234, n_eval 30.
- 2026-10-30 [collator] RESULT  Drive/log files received in `data/RunA/`: `run.log` (all four sessions appended), `train_log.csv` (10 epochs), `train_steps.csv` (2000 rows), `eval_metrics.csv`, `run_config.json`, `samples-20261029T194624Z-1-001.zip` (65 files, extracted to `data/RunA/samples/`: epochs 02, 04, 06, 08, 10 with 3 images each plus `metrics.csv`).
- 2026-10-30 [collator] RESULT  train_loss per epoch (final `train_log.csv`): 0.05631, 0.05745, 0.05512, 0.05914, 0.05822, 0.06145, 0.05696, 0.06329, 0.06070, 0.06355. Samples at epochs 2, 4, 6, 8, 10, mean over the same 3 test images (PSNR / SSIM, output vs reference): 14.10 / 0.780, 14.70 / 0.800, 13.01 / 0.706, 14.16 / 0.762, 13.91 / 0.771.
- 2026-10-30 [collator] NOTE  The full `run.log` shows what happened in session 1: epoch 9 finished at 09:37:59 (loss 0.06070), epoch 10 at 09:42:10 (loss 0.06372), and `saved resume state at epoch 10` was logged at 09:42:23; that is the last line of session 1, so it lasted 103 min (07:59:23 to 09:42:23) and no epoch-10 samples were made. Session 2 nevertheless resumed from epoch 8: the epoch-10 save never reached Drive (the runtime ended right after writing it; Drive uploads lag). Epochs 9 and 10 were therefore trained a second time. The two passes agree: epoch 9 loss 0.06070 both times, epoch 10 0.06372 vs 0.06355. This is a small reproducibility check of the resume path (same data order, restored optimizer), not an exact repeat (GPU non-determinism).
- 2026-10-30 [collator] NOTE  `total_minutes` 280.1 is the sum of the first-to-last log timestamps of the four sessions (103.0 + 138.8 + 6.2 + 32.2); it excludes the waiting between sessions and the time before session 2's and 3's first line, and session 2's end is taken as its last logged image (15:16:40), so it is a lower bound. `train_minutes` and `eval_minutes` are left blank because the sessions mix both.
- 2026-10-30 [collator] NOTE  To check on Drive: `runs/RunA/final_gen.pth` (about 593 MB). `ALL DONE` was logged 1 s after `FINAL`; the file goes through Drive's upload queue and could be missing if the runtime was closed straight away, as happened with the epoch-10 `resume.pt` in session 1. It is not needed for any result.

- 2026-10-30 [collator] NOTE  Drive listing of `runs/RunA` (`data/RunA/Screenshot 2026-10-30 at 1.34.42 AM.png`): `final_gen.pth` 592.7 MB is present (modified 1:12 AM IST = 19:42 UTC), so the check left open above is closed. Also present: `eval_metrics.csv`, `resume.pt` 1.74 GB, `run_config.json`, `run.log`, `train_log.csv`, `train_steps.csv`, `samples/`, `final_eval/`. Ownership is mixed: `eval_metrics.csv` and `final_gen.pth` (written in session 4) are owned by the other Google account that wrote them, the rest by the Run A account. `eval_metrics.csv` is already copied locally; `final_gen.pth` exists only on Drive.

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.

- `data/RunA/cell_output.txt`: pasted output of notebook Steps 5, 6 and 7.
- `data/RunA/Screenshot 2026-10-29 at 1.14.51 PM.png`: Step 4 forward-process figure (A on top, B below).
- `data/RunA/smoke_test_after_fix.txt`: Step 7 smoke test output after the fix (Run B and Run 0 paths).
- `data/RunA/RunA_stdout.log`: stdout of the running job (a partial copy taken during the run).
- `data/RunA/monitor_0823UTC.txt`: monitor output after epoch 2 (loss, samples, process list).
- `data/RunA/new_cell_output.txt`: output of session 3 (resume from epoch 10 in the Run B account). `data/RunA/cell_output.txt` holds session 2.
- `data/RunA/session4_cell_output.txt`: session 4 output as pasted in chat (resume from epoch 10, images 26 to 28).
- `data/RunA/` now also holds `run.log`, `train_log.csv`, `train_steps.csv`, `eval_metrics.csv`, `run_config.json`, the samples zip and the extracted `samples/` folder.
- `data/RunA/Screenshot 2026-10-30 at 1.34.42 AM.png`: Drive listing of `runs/RunA` after the run.
