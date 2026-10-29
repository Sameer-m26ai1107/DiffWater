# RESULTS (generated)

> **GENERATED FILE. Do not edit by hand.** Rebuilt by `collate.py` on 2026-10-29 18:48 (local time). Source: the front matter of the `Run*.md` files and `data/<RunName>/eval_metrics.csv`.

## Warnings

None.

## Status of the runs

| File | Run | Tag | Status | Owner | GPU | Started | Total min | n_eval | PSNR out | SSIM out | PSNR in | SSIM in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Run0 | 0 | main | not_started | – | – | – | – | – | – | – | – | – |
| Run0_legacy | 0 | legacy | done | JR | Tesla T4 | 2026-10-28 19:46 UTC | 155.2 | 30 | 17.72 ± 2.81 | 0.732 ± 0.073 | 19.85 | 0.779 |
| RunA | A | main | running | – | Tesla T4 | 2026-10-29 07:59 UTC | – | 30 | – | – | – | – |
| RunB | B | main | not_started | – | – | – | – | – | – | – | – | – |

## Settings check (frozen values from EXPERIMENT.md)

| Setting | Frozen | Run0 | RunA | RunB |
|---|---|---|---|---|
| exponent | 0, A: 1 / B: 2 | 1 | 1 | 2 |
| epochs | 10 | – | 10 | – |
| batch_size | 4 | – | 4 | – |
| lr | 1e-05 | – | 1e-05 | – |
| seed | 1234 | – | 1234 | – |
| n_train | 800 | – | 800 | – |
| train_dark | 575 | – | – | – |
| train_scenes | 225 | – | – | – |
| train_fingerprint | 6a9f33de995c | – | – | – |
| split_fingerprint | f8cc4714a30c | – | f8cc4714a30c | – |
| n_eval | 30 | – | 30 | – |
| checkpoint | I390000_E78_gen.pth | – | – | – |
| finetune_md5 | 38c97203e8ccafdfb80cb2be74b0bb3a | – | 38c97203e8ccafdfb80cb2be74b0bb3a | – |

## Paired comparisons (main runs, same test images)

Not available yet: needs at least two finished main runs with `data/<RunName>/eval_metrics.csv`.

## Legacy results (different test images, never compared with the main runs)

- **Run0_legacy**: PSNR 17.723 ± 2.810, SSIM 0.732 ± 0.073 (n = 30).
