---
run: B                 # 0 | A | B
tag: main            # main | legacy | variant tag
status: done
owner:
account:
started: 2026-10-29 13:30 UTC
finished: 2026-10-29 18:00 UTC
gpu: Tesla T4
torch: 2.11.0+cu130
python: 3.13.16
diffwater_commit: 7db68f34060bbf1d7c5b8153664fb16a3dcda1ae
finetune_md5: 38c97203e8ccafdfb80cb2be74b0bb3a
exponent: 2.0
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
eval_minutes: 143.9
total_minutes: 270.1
final_train_loss: 0.05009
psnr_out_mean: 12.849
psnr_out_std: 2.192
ssim_out_mean: 0.7631
ssim_out_std: 0.0974
psnr_in_mean: 20.647
ssim_in_mean: 0.8887
results_dir: Drive: FoundationModel-Assignment/runs/RunB ; local copy data/RunB/
---

# Run B: fine-tune with the modified schedule θₜ^x (x = 2.00)

## Purpose
Identical to Run A (same checkpoint, training pairs and order, hyperparameters, seeds, sampler) except that the schedule is ᾱₜ raised to the power x = 2.00 in both training and sampling. Compared with Run A to isolate the effect of the schedule.

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
- 2026-10-29 [collator] NOTE  `run.log` must show `schedule OK` with `exponent: 2.0`. If it shows 1.0 the run is invalid (see D-003).

- 2026-10-29 13:30 UTC [owner] START  Run B launched with the v3 launch cell (blocking call). Preflight (source: `data/RunB/cell_output.txt`): `md5 38c97203e8ccafdfb80cb2be74b0bb3a OK`, `commit 7db68f34060bbf1d7c5b8153664fb16a3dcda1ae OK`, `train_fp 6a9f33de995c OK`, `split_fp f8cc4714a30c OK`. Command: `--run B ... --train_root /content/euvp_train --eval_root /content/euvp_test --out_dir .../runs/RunB --epochs 10 --batch_size 4 --n_eval 30 --n_samples 3`.
- 2026-10-29 13:30 UTC [collator] RESULT  First lines of `run.log`: `run=B exponent=2.0`; args identical to Run A's (epochs 10, batch_size 4, lr 1e-05, seed 1234, n_samples 3, n_eval 30, stage all); `train pairs: 800`, `eval pairs available: 30 (using 30)`; `schedule OK: exponent 2.0, abar_first 0.999998, abar_last 1.924e-09, beta_min 2.0e-06, beta_max 0.0199, T 2000`. These match the values computed beforehand for the squared schedule (abar_T about 1.9e-9, beta from 2e-6 to 0.0199).
- 2026-10-29 13:39 UTC [collator] PROGRESS  Epochs 1 and 2 done (source: `data/RunB/run.log`). Speed 1.30 to 1.36 s/step. train_loss: epoch 1 0.04467 (4.5 min), epoch 2 0.04533 (4.5 min). `resume.pt` saved at 13:39:54. `data/RunB/train_steps.csv` has 400 rows (2 epochs x 200 steps), as expected.
- 2026-10-29 13:50 UTC [collator] PROGRESS  Epoch 2 samples: image 1 saved at 13:45:15 and image 2 at 13:50:36 (321 s each, the same as Run A). Image 3 and the epoch-2 PSNR/SSIM line were not yet in the pasted log.
- 2026-10-29 [collator] NOTE  B's training loss (0.045) is lower than A's (0.056 at epochs 1 and 2). This is not evidence that B is better: at the same t the two schedules present different noise levels, so the tasks differ. Only the test-set metrics compare A and B.
- 2026-10-29 [collator] NOTE  `data/RunB/test_split_dark30.json` holds 30 entries; its fingerprint recomputed here (md5 of `json.dumps` of the list, first 12 hex digits) is `f8cc4714a30c`, equal to Run A's.
- 2026-10-29 [collator] NOTE  Estimate, from the session timings (an epoch pair 9.0 min, save 0.2 min, 3 samples 16 min; about 5.3 min per final-eval image): epoch-10 samples done near 15:37 UTC, the other 27 images near 18:00 UTC. ENV block (gpu, torch, python) not yet pasted for this run.

- 2026-10-29 17:44 UTC [collator] PROGRESS  Run B is still running (source: `data/RunB/cell_output.txt`, updated 17:45 UTC). Training finished at 15:20:44 (110.0 min of training), `resume.pt` saved at epochs 2, 4, 6, 8, 10; 1.35 to 1.37 s/step; no errors. Final evaluation 27/30 done at 17:44:45 (127.9 min), 5.3 min per image; the last 3 images are estimated to finish near 18:01 UTC.
- 2026-10-29 [collator] RESULT  train_loss per epoch (epochs 1 to 10): 0.04467, 0.04533, 0.04273, 0.04693, 0.04551, 0.04929, 0.04514, 0.05059, 0.04877, 0.05009. Epoch 10 is about 12 percent above epoch 1 (Run A: 0.0563 at epoch 1 and 0.0636 at epoch 10, about 13 percent). Both runs drift up by a similar amount, so the cause is common to A and B (fresh Adam at lr 1e-5 on a model pretrained at 3e-6 is one candidate; not tested) and does not by itself separate A from B.
- 2026-10-29 [collator] RESULT  Samples at epochs 2, 4, 6, 8, 10, mean over the same 3 test images (PSNR / SSIM, output vs reference): 12.81 / 0.701, 12.34 / 0.771, 13.75 / 0.759, 14.13 / 0.742, 12.46 / 0.774. Run A on the same 3 images: epoch 2 14.10 / 0.780, epoch 8 14.16 / 0.762, epoch 10 13.91 / 0.771. Three images each: this is only a description of what is on disk, no comparison is drawn.

- 2026-10-29 18:00 UTC [collator] RESULT  Run B finished (source: `data/RunB/cell_output.txt`): final evaluation images 28 to 30 at 17:50:05, 17:55:25, 18:00:45 (143.9 min of evaluation); `FINAL  PSNR 12.849  SSIM 0.7631  over 30 images  (input vs ref: PSNR 20.647 SSIM 0.8887)`; `ALL DONE`; `exit code: 0`. Total 270.1 min from 13:30:42 to 18:00:49 (computed from the log). `train_minutes` left blank: the log's 'since start' figure (110.0 min at epoch 10) includes the four rounds of epoch samples.
- 2026-10-29 [owner] NOTE  ENV block pasted by the owner for this run: `gpu: Tesla T4`, `torch: 2.11.0+cu130`, `python: 3.13.16`, `diffwater_commit 7db68f34...`, `finetune_md5 38c97203...` (both equal to the frozen values). Front matter filled.
- 2026-10-29 [collator] RESULT  Files received in `data/RunB/`: `run.log`, `train_log.csv` (10 epochs), `train_steps.csv` (2000 rows), `eval_metrics.csv` (30 rows), `run_config.json`, `samples-20261029T181202Z-1-001.zip` (65 files, extracted to `data/RunB/samples/`: epochs 02, 04, 06, 08, 10, each with 3 images x {input, output, target, traj} and `metrics.csv`), and a Drive listing screenshot. Recomputed from `eval_metrics.csv`: PSNR out 12.849 ± 2.192, SSIM out 0.7631 ± 0.0974, PSNR in 20.647, SSIM in 0.8887 (sample standard deviation); the means equal the `FINAL` line. `train_log.csv` equals the epoch means in the log (0.04467 to 0.05009).
- 2026-10-29 [collator] RESULT  The input-vs-reference columns of `RunB/eval_metrics.csv` and `Run0/eval_metrics.csv` are identical for all 30 images, which confirms both runs used the same 30 test images in the same order. Paired difference B minus Run 0 (output vs reference): PSNR mean -4.059 dB, s.e. 0.545 (|mean|/s.e. 7.5), B lower on 27 of 30 images, range -12.33 to +2.43; SSIM mean -0.0294, s.e. 0.0123 (|mean|/s.e. 2.4), B lower on 19 of 30. This is B against the pretrained model, which differs from B in two ways (the fine-tune and the schedule). **It does not isolate the schedule; Run A is the control for that.**
- 2026-10-29 [collator] NOTE  Drive listing (`data/RunB/Screenshot 2026-10-29 at 11.44.17 PM.png`): `runs/RunB` holds `final_eval/`, `samples/`, `eval_metrics.csv`, `final_gen.pth` (592.7 MB), `resume.pt` (1.74 GB), `run_config.json`, `run.log`, `train_log.csv`, `train_steps.csv`. This account's Drive shows a banner 'Drive 84% of storage used'.

- 2026-10-30 [collator] NOTE  Correction to the 2026-10-29 entry on the rising training loss: it said both runs drift up by a similar amount, 'so the cause is common to A and B'. That inference is too strong. Run A and Run B use the same per-epoch seeds (seed + epoch), hence the same batches, timesteps and noise, so their loss curves are expected to move in parallel (visible in `report/figures/fig2_loss.png`); the agreement is not two independent confirmations. The rise itself (A 0.0563 to 0.0636, B 0.0447 to 0.0501, about 12 to 13 percent) is modest against an epoch-mean noise of roughly 0.003 (estimate).

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.
- `data/RunB/cell_output.txt`: launch cell output (preflight and the log as printed).
- `data/RunB/run.log`, `data/RunB/train_steps.csv`: Drive copies taken at about 13:54 UTC (epochs 1 and 2 only).
- `data/RunB/test_split_dark30.json`: the test split file (fingerprint `f8cc4714a30c`).
- `data/RunB/` : all files listed above, including the extracted `samples/` folder (the zip is kept next to it).
