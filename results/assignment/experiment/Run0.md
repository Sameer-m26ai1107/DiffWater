---
run: 0                 # 0 | A | B
tag: main            # main | legacy | variant tag
status: not_started  # not_started | running | interrupted | done | failed | abandoned
owner:
account:
started:
finished:
gpu:
torch:
python:
diffwater_commit:
finetune_md5:
exponent: 1
epochs:
batch_size:
lr:
seed:
n_train:
train_dark:
train_scenes:
train_fingerprint:
split_fingerprint:
n_eval:
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

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.
