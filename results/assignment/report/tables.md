### Test-set scores (output vs reference, 30 held-out Underwater Dark pairs)

| Condition | PSNR (dB) mean ± sd | SSIM mean ± sd |
|---|---|---|
| Input (colour-compensated), no model | 20.65 ± 4.13 | 0.889 ± 0.081 |
| Run 0 | 16.91 ± 3.07 | 0.792 ± 0.071 |
| Run A | 14.36 ± 3.02 | 0.770 ± 0.112 |
| Run B | 12.85 ± 2.19 | 0.763 ± 0.097 |

### Paired differences (per image, first minus second)

| Comparison | Metric | Mean difference | s.e. | |mean|/s.e. | Second run higher on | Range |
|---|---|---|---|---|---|---|
| Run A − Run 0 | PSNR (dB) | -2.55 | 0.534 | 4.8 | 6/30 | -11.03 to +2.41 |
| Run A − Run 0 | SSIM | -0.022 | 0.014 | 1.6 | 14/30 | -0.240 to +0.076 |
| Run B − Run 0 | PSNR (dB) | -4.06 | 0.544 | 7.5 | 3/30 | -12.33 to +2.43 |
| Run B − Run 0 | SSIM | -0.029 | 0.012 | 2.4 | 11/30 | -0.228 to +0.065 |
| Run B − Run A | PSNR (dB) | -1.51 | 0.398 | 3.8 | 5/30 | -6.43 to +3.44 |
| Run B − Run A | SSIM | -0.007 | 0.008 | 0.8 | 9/30 | -0.067 to +0.166 |

### Epoch samples (mean over the 3 sampled test images, PSNR / SSIM)

| Epoch | Run A | Run B |
|---|---|---|
| 2 | 14.10 / 0.780 | 12.81 / 0.701 |
| 4 | 14.70 / 0.800 | 12.34 / 0.771 |
| 6 | 13.01 / 0.706 | 13.75 / 0.759 |
| 8 | 14.16 / 0.762 | 14.13 / 0.742 |
| 10 | 13.91 / 0.771 | 12.46 / 0.774 |

### Schedule facts (computed in float64, t = 1..T)

- abar_T: 4.3859782361332086e-05
- abarx_T: 1.923680508783417e-09
- abar_1: 0.999999
- beta_x_min: 1.999999000079633e-06
- beta_x_max: 0.019899999999999918
- t_half_A: 527
- t_half_B: 373
- t_noise_A: 1356
- t_noise_B: 960
- max_amp_A: 150.99645935417007
- max_amp_B: 22799.93073749554
- all_in_01: True
- monotone: True
