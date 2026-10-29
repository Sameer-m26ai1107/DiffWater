---
run: B                 # 0 | A | B
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
exponent: 2.0
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

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.
