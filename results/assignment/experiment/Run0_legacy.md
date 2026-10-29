---
run: 0                 # 0 | A | B
tag: legacy            # main | legacy | variant tag
status: done  # not_started | running | interrupted | done | failed | abandoned
owner: JR
account:
started: 2026-10-28 19:46 UTC
finished:
gpu: Tesla T4
torch:
python:
diffwater_commit:
finetune_md5:
exponent: 1
epochs:
batch_size:
lr:
seed: 1234
n_train:
train_dark:
train_scenes:
train_fingerprint:
split_fingerprint:
n_eval: 30
checkpoint: I390000_E78_gen.pth
train_minutes:
eval_minutes:
total_minutes: 155.2
final_train_loss:
psnr_out_mean: 17.723
psnr_out_std: 2.810
ssim_out_mean: 0.732
ssim_out_std: 0.073
psnr_in_mean: 19.854
ssim_in_mean: 0.779
results_dir: Drive: FoundationModel-Assignment/run0_diffwater_live/Run0_EUVP_261028_194635/
---

# Run 0 (legacy): pretrained DiffWater on the EUVP `test_samples` folder

## Purpose
The first Run 0, made before the evaluation set was changed (D-005). It scored 30 pairs from the `test_samples` folder, whose composition is unknown. Kept as a secondary result. **Never compared with Run A or B**, because the test images differ.

## Setup actually used
Anything that differs from `EXPERIMENT.md`, and which notebook cells were run. Write `as specified` if nothing differs.

## Observations
What you saw: loss behaviour, sample quality, anything odd. Facts first, interpretation labelled as such.

## Issues and fixes
In order. Include exact error text if short.

## Deviations from the protocol
`none`, or a list.

## Log
Append-only. Format: `- YYYY-MM-DD HH:MM UTC [who] TYPE  text`. Types: START, PROGRESS, ISSUE, FIX, DECISION, RESULT, NOTE, DONE.

- 2026-10-28 19:46 UTC [owner] START  Step 7 of `Run0_DiffWater_with_edits.ipynb`: repo's unmodified `test.py` through a seeding wrapper, seed 1234 set once, 30 images, 2000-step sampling.
- 2026-10-28 [owner] RESULT  `elapsed: 155.2 min for 30 images`, about 6.47 it/s (source: Step 7 output).
- 2026-10-29 [owner] RESULT  Metrics computed from the Drive copies (the runtime had disconnected before Step 8): output vs reference PSNR 17.723 ± 2.810, SSIM 0.732 ± 0.073; saved input vs reference PSNR 19.854 ± 3.974, SSIM 0.779 ± 0.092 (source: from-Drive metrics cell).
- 2026-10-29 [collator] NOTE  Saved `0_k_input.png` is the colour-compensated input, not the raw image. Per-image values are in `data/Run0_legacy/eval_metrics.csv`, copied from `../Run0_Report.md`.

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.
