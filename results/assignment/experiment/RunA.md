---
run: A                 # 0 | A | B
tag: main            # main | legacy | variant tag
status: running
owner:
account:
started: 2026-10-29 07:59 UTC
finished:
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
train_fingerprint:
split_fingerprint: f8cc4714a30c
n_eval: 30
checkpoint:
train_minutes:
eval_minutes:
total_minutes:
final_train_loss:
psnr_out_mean:
psnr_out_std:
ssim_out_mean:
ssim_out_std:
psnr_in_mean:
ssim_in_mean:
results_dir:
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
- Run A was interrupted by a Colab disconnect and **resumed from `resume.pt` at epoch 8** (2026-10-29 12:58 UTC, same account, same `finetune.py` md5, same command). Epochs 1 to 8 ran in session 1, epochs 9 and 10 and the final evaluation run in session 2. Method and settings are unchanged. Weights and Adam state were restored; per-epoch seeds are `seed + epoch`, so the data order of epochs 9 and 10 is the one an uninterrupted run would use. Run B is expected to run uninterrupted; GPU non-determinism makes bit-identical results impossible in either case.

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

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.

- `data/RunA/cell_output.txt`: pasted output of notebook Steps 5, 6 and 7.
- `data/RunA/Screenshot 2026-10-29 at 1.14.51 PM.png`: Step 4 forward-process figure (A on top, B below).
- `data/RunA/smoke_test_after_fix.txt`: Step 7 smoke test output after the fix (Run B and Run 0 paths).
- `data/RunA/RunA_stdout.log`: stdout of the running job (a partial copy taken during the run).
- `data/RunA/monitor_0823UTC.txt`: monitor output after epoch 2 (loss, samples, process list).
