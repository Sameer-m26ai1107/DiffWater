# Run 0 Report: pretrained DiffWater on EUVP, no fine-tuning

Group 25 · Foundation Models and Generative AI · Noise Schedule Ablation in Diffusion Models

Status: this report covers the **first Run 0, on the EUVP `test_samples` folder** (30 of 30 images). On 2026-10-29 the team decided to evaluate Run 0, A and B on held-out EUVP **Underwater Dark** pairs, as named in the declaration, because the composition of `test_samples` is unknown. **Run 0 is therefore being repeated on the new test set** (`finetune.py --run 0`, same sampler and per-image seeds as A and B). This report stays as a secondary result on a mixed test set. Runs A and B not started.

---

## 1. What Run 0 is, and why it matters for the ablation

The assignment compares two fine-tuning runs from the same pretrained checkpoint. Run A uses the original noise schedule. Run B uses a modified schedule, θₜ raised to a power x. Run 0 is the reference point for both: the pretrained model applied to our test images with no fine-tuning at all. If A and B improve over Run 0, we know fine-tuning on our data had an effect. The A-versus-B difference then isolates the schedule.

Run 0 therefore has to be fixed in a way that A and B can copy exactly: same test images, same sampler, same metrics.

## 2. Model change from the declaration

The Phase 1 declaration named **UW-DiffPhys** (github.com/bachzz/UW-DiffPhys). This report is about a **different repository: DiffWater** (github.com/Guan-MS/DiffWater, Apache-2.0).

Why we switched:

- UW-DiffPhys publishes its pretrained checkpoint on a Google Drive that is restricted to signed-in, approved accounts. We could not get access. We checked that the link redirects to a Google sign-in page, so this is a permission problem and not a download quota problem.
- Training UW-DiffPhys from scratch on a Colab T4 was not feasible. A colleague's earlier attempt ran about 1.3 s per step and about 55 minutes per epoch, and reached only epoch 2 before stopping.
- DiffWater is a conditional DDPM for paired underwater enhancement, its code is open, and its weights are in a public Drive folder that opened for us.

The model change needs instructor approval, and the declaration deadline has passed. This is listed under open items in section 9.

Does the schedule ablation still apply? Yes. DiffWater uses the standard DDPM forward process, so the quantity θₜ = ᾱₜ (cumulative product of 1 − βₜ) exists and can be raised to a power. We checked this numerically (section 7).

## 3. Setup

| Item | Value |
|---|---|
| Model | DiffWater conditional DDPM (SR3-style UNet), 155.3 M parameters |
| Checkpoint | `I390000_E78_gen.pth` (593 MB), from the `LSUI` folder of the authors' public Drive |
| Image size | 256 × 256 |
| Noise schedule | linear β, 2000 timesteps, β from 1e-6 to 1e-2 |
| Sampler | repo's own `p_sample_loop`, all 2000 steps, no skipping |
| Test data | EUVP `test_samples` (`Inp` degraded, `GTr` reference), 515 pairs available, **30 used** |
| Image selection | common filename stems shuffled with `random.Random(1234)`, first 30 taken, then sorted |
| Preprocessing | resize to 256 with LANCZOS, saved as PNG. The repo's loader then applies its own colour channel compensation to the input |
| Seed | 1234, set once at the start of the process (wrapper script, `test.py` itself is unmodified) |
| Hardware | Colab T4 (15 GB), model peak memory about 0.9 GB at batch size 1 |
| Run time | 155.2 min for 30 images, about 5.2 min per image, 6.47 it/s |
| Run date | 2026-10-28, started 19:46 on the Colab clock |

Why 30 images and not all 515: at 5.2 min per image, 515 images would take about 45 hours per run. A and B each need the same test set, and the course schedule did not allow it. Thirty was the largest set the team agreed it could afford.

## 4. How we measured

We computed PSNR and SSIM ourselves with scikit-image, on 256 × 256 uint8 RGB images, `data_range=255`, SSIM over channels (`channel_axis=2`). Output is compared with the reference image.

We did **not** use the repo's `eval.py`. Reading the code, it compares the input image with the target and not the output with the target, and its SSIM function is non-standard. Numbers from it would not be Run 0 numbers.

The table in section 5 reports two things for each image:

- **Output vs reference.** This is the Run 0 result.
- **Saved input vs reference.** `test.py` saves the input *after* the repo's colour channel compensation, so this is the compensated input, not the raw EUVP image. It is what the model sees as its condition, and it is a useful "do nothing" comparison. It is not the same as raw-vs-reference.

## 5. Results

### Summary (30 images, one sample per image)

| | PSNR (dB) | SSIM |
|---|---|---|
| Model output vs reference | 17.72 ± 2.81 | 0.732 ± 0.073 |
| Saved (compensated) input vs reference | 19.85 ± 3.97 | 0.779 ± 0.092 |
| Paired difference (output minus input) | −2.13 ± 0.81 (s.e.) | −0.047 ± 0.011 (s.e.) |

(± on the first two rows is the standard deviation across images. On the third row it is the standard error of the mean paired difference, n = 30.)

The output beats the saved input on PSNR in **9 of 30** images (2, 6, 10, 11, 15, 21, 22, 23, 27) and on SSIM in **6 of 30** (2, 6, 10, 14, 15, 22).

### Per-image results

| idx | PSNR out | SSIM out | PSNR in | SSIM in |
|---|---|---|---|---|
| 1 | 17.781 | 0.775 | 19.899 | 0.784 |
| 2 | 17.921 | 0.837 | 17.584 | 0.830 |
| 3 | 17.124 | 0.733 | 22.287 | 0.772 |
| 4 | 20.994 | 0.783 | 22.501 | 0.847 |
| 5 | 15.217 | 0.739 | 22.006 | 0.881 |
| 6 | 19.784 | 0.717 | 11.736 | 0.611 |
| 7 | 17.661 | 0.768 | 23.528 | 0.794 |
| 8 | 15.581 | 0.655 | 19.619 | 0.778 |
| 9 | 15.033 | 0.692 | 23.443 | 0.839 |
| 10 | 19.524 | 0.728 | 19.059 | 0.722 |
| 11 | 23.320 | 0.844 | 19.127 | 0.880 |
| 12 | 19.633 | 0.832 | 24.419 | 0.856 |
| 13 | 18.511 | 0.778 | 18.767 | 0.878 |
| 14 | 20.718 | 0.786 | 22.326 | 0.776 |
| 15 | 23.640 | 0.793 | 14.835 | 0.769 |
| 16 | 16.788 | 0.743 | 23.019 | 0.789 |
| 17 | 17.210 | 0.720 | 24.254 | 0.859 |
| 18 | 16.055 | 0.748 | 23.363 | 0.820 |
| 19 | 11.419 | 0.690 | 12.027 | 0.691 |
| 20 | 18.581 | 0.783 | 22.139 | 0.801 |
| 21 | 20.369 | 0.692 | 19.407 | 0.768 |
| 22 | 17.966 | 0.614 | 17.651 | 0.571 |
| 23 | 16.262 | 0.764 | 14.909 | 0.807 |
| 24 | 17.542 | 0.780 | 24.021 | 0.855 |
| 25 | 17.584 | 0.658 | 18.334 | 0.668 |
| 26 | 21.449 | 0.746 | 24.064 | 0.783 |
| 27 | 13.223 | 0.482 | 9.326 | 0.511 |
| 28 | 15.503 | 0.689 | 21.195 | 0.826 |
| 29 | 13.907 | 0.732 | 20.074 | 0.874 |
| 30 | 15.389 | 0.649 | 20.714 | 0.730 |

Notable rows: images 6, 15 and 27 gain 8.0, 8.8 and 3.9 dB over the input. Those are also inputs with low starting PSNR (11.7, 14.8, 9.3 dB), so the model helps most where the input is furthest from the reference. Image 19 is the worst output (11.4 dB) and its input is also poor (12.0 dB).

### Qualitative check (image 1 only)

We have looked at the saved files for image 1 only (input, output, target, denoising process). The output is close to the input, with slightly more contrast. The reference is clearer and has warmer, greener colours. The denoising-process grid shows the input, then 10 frames from pure noise to the final image, with structure appearing around the seventh frame.

Grid frame timing, from the code: `sample_inter = 1 | (2000 // 10) = 201`, so frames are saved at t = 1809, 1608, 1407, 1206, 1005, 804, 603, 402, 201 and 0. The first panel is the colour-compensated input, and the last panel is the final output. We looked at the other 29 sets only through the metrics, not visually. Before the report is final, someone should look at a handful more.

## 6. Interpretation

**Run 0 is a weak baseline on this data, and that is the useful finding.** On average the pretrained model lands 2.1 dB below the "do nothing" comparison and does not beat it on most images.

Our reading of why, in order of how confident we are:

1. **The references are not ground truth.** EUVP's reference images are enhanced images produced by a different process, with their own colour style. PSNR and SSIM reward staying close to that style. A model trained on a different dataset has no reason to match it.
2. **Domain shift.** The checkpoint comes from the authors' LSUI-trained set. EUVP images differ in resolution, camera and water type. This is plausible but we have not isolated it.
3. **Stochastic sampling.** Each number is a single random sample. Spread between samples of the same image is not measured, so some of the per-image variation could be sampling noise.

What we are **not** claiming: that DiffWater is a poor model in general, or that PSNR against EUVP references measures visual quality. The visual output for image 1 is a plausible, slightly sharper version of the input.

Why this still works as a baseline: fine-tuning on EUVP paired training data pulls the model towards the EUVP reference style. We expect A and B to move above Run 0 on these metrics, and the difference between A and B is the quantity the ablation is about.

## 7. Noise schedule facts for Runs A and B

Checked in notebook Step 5 on the real config:

| Quantity | Value |
|---|---|
| ᾱ₁ | 0.99999900 |
| ᾱ_T (T = 2000) | 4.386e-5 |
| Range | strictly decreasing, inside (0, 1) at every t |

So θₜ = ᾱₜ is well defined and bounded. For the modified schedule θₜ^x with x = 2.00, ᾱₜ² also stays inside (0, 1) (first value about 0.999998, last about 1.9e-9) and keeps decreasing, so it is a valid schedule.

Effect on signal-to-noise ratio, with SNR(t) = ᾱₜ / (1 − ᾱₜ):

SNR′(t) = ᾱₜ² / (1 − ᾱₜ²) = SNR(t) · ᾱₜ / (1 + ᾱₜ)

At early timesteps (ᾱ close to 1) the factor is close to 1/2, so SNR roughly halves. At late timesteps (ᾱ close to 0) the factor goes to 0, so noise dominates sooner. The modified schedule therefore corrupts images faster. Use this in the Run B discussion.

An implementation note for A and B, from reading the code: the DiffWater UNet receives the **integer timestep t** (sinusoidal embedding), and training samples a random t, noises the target with `q_sample` using √ᾱₜ and √(1 − ᾱₜ), and regresses the added noise. So the schedule lives in the precomputed ᾱ-derived buffers, and the network input t keeps its meaning as an index. The change to ᾱₜ^x has to go into every buffer that derives from ᾱ, in both the forward noising and the sampling posterior. If only one side changes, B is an inconsistent model and not a clean schedule ablation.

One consequence worth stating in the Run B discussion: the pretrained network learned "timestep t means noise level ᾱₜ". Under the modified schedule the same t means ᾱₜ², so the model starts Run B mismatched and fine-tuning has to absorb that. This is part of what the ablation measures.

## 8. Limitations

- **Sample size.** 30 images, one seed, one sample per image. The standard error of the mean PSNR difference is 0.81 dB, so differences of about 1 dB between A and B will be hard to resolve. The report for A and B should say so.
- **One checkpoint.** `I390000_E78` from the LSUI folder. The authors' Drive also has a UIEB model. We did not evaluate it.
- **Seed handling.** The seed is set once, so a given image's noise depends on how many images ran before it. For A and B we will seed per image so both runs see identical noise for each image.
- **Reference quality.** See section 6.
- **`test_samples` composition unknown.** We have not established which EUVP subsets those 515 pairs come from (Dark, Scenes, ImageNet, or a mix).
- **Raw-versus-reference not reported.** Our table uses the compensated input. The notebook's Step 8 computes raw-versus-reference as well, but Step 8 was not run in the final session (see the README).

## 9. Open items and deviations

1. **Instructor approval** for replacing UW-DiffPhys with DiffWater. The declaration deadline (Oct 10) has passed.
2. **Declaration fields.** The page and line evidence fields in the Phase 1 declaration are blank. For DiffWater we still need the paper citation (IEEE Xplore, document 10365517) and the page or line showing which datasets it was pretrained on, to support the claim that EUVP was not in pretraining. We have not verified that claim.
3. **Dataset scope.** The declaration lists EUVP Dark and Scenes (5,550 and 2,185 training pairs) and excludes ImageNet. Run 0 evaluates on `test_samples`. For A and B, train on Dark and Scenes only so we match the declaration.
4. **Visual review.** Only image 1 has been inspected by eye.

## 10. Where everything is

| Item | Location |
|---|---|
| Notebook | `results/assignment/Run0_DiffWater.ipynb` (see README for how it differs from the live Colab copy) |
| Raw outputs (30 × input, output, target, denoising process) | Drive: `FoundationModel-Assignment/run0_diffwater_live/Run0_EUVP_261028_194635/` |
| Per-image metrics | Drive: `FoundationModel-Assignment/run0_metrics_from_drive.csv` |
| 30-image split list | Drive: `FoundationModel-Assignment/test_split_30.json`, if saved (the split is also reproducible from seed 1234 and the Kaggle dataset) |
| Seed | 1234 |
| Environment | Colab T4, Python/PyTorch as preinstalled on Colab at run time, plus tensorboardX, scikit-image, lmdb, pyyaml, gdown, kagglehub |

## 11. What carries over to Runs A and B

- Same 30 test images (same `random.Random(1234)` selection).
- Same sampler: 2000 steps, same wrapper idea, but seeded per image.
- Same metrics code (skimage, `data_range=255`, SSIM over channels).
- Same checkpoint as the starting point.
- All hyperparameters identical between A and B. Only the exponent differs.
- Compare A and B against Run 0 as well as against each other.
