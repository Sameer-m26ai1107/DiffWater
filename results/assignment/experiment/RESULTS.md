# RESULTS (generated)

> **GENERATED FILE. Do not edit by hand.** Rebuilt by `collate.py` on 2026-10-30 01:42 (local time). Source: the front matter of the `Run*.md` files and `data/<RunName>/eval_metrics.csv`.

## Warnings

- ⚠ Run0: status is done but these front matter fields are empty: owner, gpu
- ⚠ RunA: status is done but these front matter fields are empty: owner
- ⚠ RunB: status is done but these front matter fields are empty: owner

## Status of the runs

| File | Run | Tag | Status | Owner | GPU | Started | Total min | n_eval | PSNR out | SSIM out | PSNR in | SSIM in |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Run0 | 0 | main | done | – | – | 2026-10-29 13:38 UTC | 161.9 | 30 | 16.91 ± 3.08 | 0.792 ± 0.071 | 20.65 | 0.889 |
| Run0_legacy | 0 | legacy | done | JR | Tesla T4 | 2026-10-28 19:46 UTC | 155.2 | 30 | 17.72 ± 2.81 | 0.732 ± 0.073 | 19.85 | 0.779 |
| RunA | A | main | done | – | Tesla T4 | 2026-10-29 07:59 UTC | 280.1 | 30 | 14.36 ± 3.02 | 0.770 ± 0.112 | 20.65 | 0.889 |
| RunB | B | main | done | – | Tesla T4 | 2026-10-29 13:30 UTC | 270.1 | 30 | 12.85 ± 2.19 | 0.763 ± 0.097 | 20.65 | 0.889 |

## Settings check (frozen values from EXPERIMENT.md)

| Setting | Frozen | Run0 | RunA | RunB |
|---|---|---|---|---|
| exponent | 0, A: 1 / B: 2 | 1 | 1 | 2 |
| epochs | 10 | – | 10 | 10 |
| batch_size | 4 | – | 4 | 4 |
| lr | 1e-05 | – | 1e-05 | 1e-05 |
| seed | 1234 | 1234 | 1234 | 1234 |
| n_train | 800 | – | 800 | 800 |
| train_dark | 575 | – | – | – |
| train_scenes | 225 | – | – | – |
| train_fingerprint | 6a9f33de995c | – | 6a9f33de995c | 6a9f33de995c |
| split_fingerprint | f8cc4714a30c | f8cc4714a30c | f8cc4714a30c | f8cc4714a30c |
| n_eval | 30 | 30 | 30 | 30 |
| checkpoint | I390000_E78_gen.pth | I390000_E78_gen.pth | I390000_E78_gen.pth | I390000_E78_gen.pth |
| finetune_md5 | 38c97203e8ccafdfb80cb2be74b0bb3a | 38c97203e8ccafdfb80cb2be74b0bb3a | 38c97203e8ccafdfb80cb2be74b0bb3a | 38c97203e8ccafdfb80cb2be74b0bb3a |

## Paired comparisons (main runs, same test images)

Images scored by every finished run: **30**. Difference = first minus second, per image. Rule of thumb: |mean| below 2 standard errors is not distinguishable from zero with this sample.

| Comparison | Metric | n | Mean diff | s.e. | Wins | Verdict |
|---|---|---|---|---|---|---|
| RunA − Run0 | PSNR (dB) | 30 | -2.548 | 0.534 | 6/30 | distinguishable |
| RunA − Run0 | SSIM | 30 | -0.022 | 0.014 | 14/30 | not distinguishable from 0 |
| RunB − Run0 | PSNR (dB) | 30 | -4.059 | 0.544 | 3/30 | distinguishable |
| RunB − Run0 | SSIM | 30 | -0.029 | 0.012 | 11/30 | distinguishable |
| RunB − RunA | PSNR (dB) | 30 | -1.511 | 0.398 | 5/30 | distinguishable |
| RunB − RunA | SSIM | 30 | -0.007 | 0.008 | 9/30 | not distinguishable from 0 |

| Run | PSNR out (mean ± std) | SSIM out (mean ± std) | PSNR in | SSIM in |
|---|---|---|---|---|
| Run0 | 16.91 ± 3.07 | 0.792 ± 0.071 | 20.65 | 0.889 |
| RunA | 14.36 ± 3.02 | 0.770 ± 0.112 | 20.65 | 0.889 |
| RunB | 12.85 ± 2.19 | 0.763 ± 0.097 | 20.65 | 0.889 |

## Legacy results (different test images, never compared with the main runs)

- **Run0_legacy**: PSNR 17.723 ± 2.810, SSIM 0.732 ± 0.073 (n = 30).
