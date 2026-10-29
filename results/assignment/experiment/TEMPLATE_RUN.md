---
run:                 # 0 | A | B
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
exponent:
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

# Run <0|A|B>: <one-line description>

## Purpose
<what this run is for, one or two sentences>

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

## Artifacts
Where the files are: Drive path, zip name, `data/<RunName>/` contents.
