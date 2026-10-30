---
run: 0                 # 0 | A | B
tag: main            # main | legacy | variant tag
status: done
owner:
account:
started: 2026-10-29 13:38 UTC
finished: 2026-10-29 16:20 UTC
gpu:
torch:
python:
diffwater_commit: 7db68f34060bbf1d7c5b8153664fb16a3dcda1ae
finetune_md5: 38c97203e8ccafdfb80cb2be74b0bb3a
exponent: 1
epochs:
batch_size:
lr:
seed: 1234
n_train:
train_dark:
train_scenes:
train_fingerprint:
split_fingerprint: f8cc4714a30c
n_eval: 30
checkpoint: I390000_E78_gen.pth
train_minutes:
eval_minutes: 161.8
total_minutes: 161.9
final_train_loss:
psnr_out_mean: 16.908
psnr_out_std: 3.075
ssim_out_mean: 0.7925
ssim_out_std: 0.0712
psnr_in_mean: 20.647
ssim_in_mean: 0.8887
results_dir: Drive: FoundationModel-Assignment/runs/Run0 ; local copy data/Run0/
---

# Run 0: pretrained DiffWater, no fine-tuning, on held-out Dark pairs

## Purpose
Baseline for the ablation. The pretrained checkpoint is applied to the 30 held-out Underwater Dark test pairs with no training, using the same sampler, code (`finetune.py --run 0`) and per-image seeds as the final evaluation of A and B. A and B are compared with it and with each other.

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

- 2026-10-29 [collator] NOTE  File created from TEMPLATE_RUN.md. Nothing has been run yet.
- 2026-10-29 [collator] NOTE  Replaces the first Run 0 (on `test_samples`), which is kept as `Run0_legacy.md` (decision D-005, D-007).

- 2026-10-29 13:38 UTC [owner] START  Run 0 launched with the v3 launch cell (blocking call). Preflight (source: `data/Run0/cell_output.txt`): `md5 38c97203e8ccafdfb80cb2be74b0bb3a OK`, `commit 7db68f34060bbf1d7c5b8153664fb16a3dcda1ae OK`, `split_fp f8cc4714a30c OK` (the train fingerprint is not checked for Run 0). Command: `--run 0 ... --eval_root /content/euvp_test --out_dir .../runs/Run0 --epochs 10 --batch_size 4 --n_eval 30 --n_samples 3`; `--epochs`, `--batch_size` and `--n_samples` are passed but unused in Run 0, so `epochs`, `batch_size`, `lr`, `n_train` stay blank in the front matter.
- 2026-10-29 13:38 UTC [collator] RESULT  First lines of `run.log`: `run=0 exponent=1.0`, `stage: eval`, `train_root: None`, `train pairs: 0`, `eval pairs available: 30 (using 30)`, `schedule OK: exponent 1.0, abar_last 4.386e-05, T 2000` (the same schedule as Run A).
- 2026-10-29 13:49 UTC [collator] PROGRESS  Final evaluation: image 1/30 done at 13:44:04 (5.3 min), image 2/30 at 13:49:28 (10.7 min). The Drive screenshot (`data/Run0/Screenshot 2026-10-29 at 7.21.44 PM.png`) shows `final_eval` with `idx01_{input,output,target,traj}.png` (7:14 PM local time) and `idx02_*` (7:19 PM), i.e. 13:44 and 13:49 UTC, matching the log. Sizes: idx01 131, 146, 133, 934 KB; idx02 152, 156, 153, 941 KB.
- 2026-10-29 [collator] NOTE  Estimate: 5.3 min per image x 30 = about 160 min, so the run ends near 16:19 UTC. ENV block (gpu, torch, python) not yet pasted for this run.

- 2026-10-29 16:20 UTC [collator] RESULT  Run 0 finished (source: `data/Run0/cell_output.txt`): final evaluation images 3 to 30 logged every 5.4 min (5.3 to 5.4 min each); `FINAL  PSNR 16.908  SSIM 0.7925  over 30 images  (input vs ref: PSNR 20.647 SSIM 0.8887)`, then `ALL DONE` and `exit code: 0`. 161.8 min of evaluation (from the log); total 161.9 min from the first to the last timestamp (13:38:42 to 16:20:36, computed). Front matter filled; the standard deviations need `eval_metrics.csv` (not yet copied into `data/Run0/`).
- 2026-10-29 [owner] NOTE  Colab later showed a 'disconnected for inactivity' message for this session. The log is complete (`ALL DONE`, exit code 0), so the run is a success whatever the message says; collator's reading is that the session went idle after the cell ended, which is not stated anywhere in the pasted text.
- 2026-10-29 [collator] NOTE  The model's output scores lower than the colour-compensated input against the reference (PSNR 16.91 vs 20.65, SSIM 0.793 vs 0.889). The legacy Run 0 on `test_samples` showed the same pattern (17.72 vs 19.85, 0.732 vs 0.779), on different images. Observation only: the EUVP reference images are not ground truth, and full-reference PSNR/SSIM reward staying close to the input. This bears on how the report phrases the A vs B comparison.

- 2026-10-29 [collator] RESULT  `data/Run0/eval_metrics.csv` received (30 rows, columns idx, psnr_out, ssim_out, psnr_in, ssim_in). Recomputed here: PSNR out 16.908 ± 3.075 (min 11.73, max 22.86), SSIM out 0.7925 ± 0.0712, PSNR in 20.647 ± 4.127, SSIM in 0.8887 ± 0.0811 (sample standard deviation). The means equal the `FINAL` line of the log. `run.log` copied; its last lines are `FINAL ...` and `ALL DONE`.
- 2026-10-29 [collator] NOTE  The Drive listing (`data/Run0/Screenshot 2026-10-29 at 11.36.19 PM.png`) shows `runs/Run0` with `final_eval/`, `eval_metrics.csv`, `run_config.json` and `run.log`. There is no `train_log.csv`, `train_steps.csv`, `resume.pt`, `samples/` or `final_gen.pth`, and there should not be: Run 0 does no training and writes no per-epoch samples (stage `eval`). `run_config.json` has not been copied into `data/Run0/` yet.

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.
- `data/Run0/cell_output.txt`: launch cell output (preflight and the log up to image 2).
- `data/Run0/Screenshot 2026-10-29 at 7.21.44 PM.png`: Drive `Run0/final_eval` listing after images 1 and 2.
- `data/Run0/cell_output.txt` now holds the whole log up to `ALL DONE`. Still to copy from Drive `runs/Run0/`: `eval_metrics.csv`, `run.log`, `run_config.json`.
- `data/Run0/eval_metrics.csv`, `data/Run0/run.log`: copied from Drive `runs/Run0/` after the run.
- `data/Run0/Screenshot 2026-10-29 at 11.36.19 PM.png`: Drive listing of `runs/Run0`.
