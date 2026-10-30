---
frozen.model: DiffWater
frozen.checkpoint: I390000_E78_gen.pth
frozen.exponent_A: 1
frozen.exponent_B: 2.0
frozen.epochs: 10
frozen.batch_size: 4
frozen.lr: 1e-5
frozen.seed: 1234
frozen.n_train: 800
frozen.train_dark: 575
frozen.train_scenes: 225
frozen.train_fingerprint: 6a9f33de995c
frozen.split_fingerprint: f8cc4714a30c
frozen.n_eval: 30
frozen.finetune_md5: 38c97203e8ccafdfb80cb2be74b0bb3a
---

# Experiment: noise schedule ablation on DiffWater (Runs 0, A, B)

Group 25 · Foundation Models and Generative AI. How to document: `PROTOCOL.md`. Decisions: `DECISIONS.md`. Compiled results: `RESULTS.md` (generated).

## Question
Does replacing the schedule quantity θₜ = ᾱₜ by θₜ^x (x = 2.00) change the quality of an underwater-image enhancement diffusion model after a short fine-tune from the same pretrained checkpoint?

## The runs

| Run | What it is | Schedule | Training | Test |
|---|---|---|---|---|
| `Run0` | pretrained checkpoint, no fine-tuning | θₜ (exponent 1) | none | 30 held-out Dark pairs |
| `RunA` | fine-tune from the checkpoint | θₜ (exponent 1) | 800 pairs, Dark + Scenes mix | same 30 |
| `RunB` | fine-tune from the checkpoint | θₜ^x, x = 2.00 | the same 800 pairs, same order | same 30 |
| `Run0_legacy` | first Run 0, on the EUVP `test_samples` folder | θₜ | none | 30 `test_samples` pairs (different images) |

A and B differ **only** in the exponent. Run 0, A and B use the same sampler (2000-step ancestral sampling) and the same per-image sampling seeds, so every image starts from identical noise in every run. `Run0_legacy` is never compared with the others.

## Frozen settings (identical across runs; machine-checked by `collate.py`)
These are the `frozen.*` values in the front matter above. Blank means not yet decided or not yet observed. Fill it in through a `DECISIONS.md` entry.

| Setting | Value | Note |
|---|---|---|
| Model | DiffWater (Guan-MS/DiffWater), conditional DDPM, 256 px | |
| Checkpoint | `I390000_E78_gen.pth` (LSUI folder of the authors' Drive) | |
| Noise schedule | linear β, 2000 steps, 1e-6 to 1e-2; B uses ᾱ² | |
| Epochs | 10 | one epoch = one pass over the 800 training pairs; samples at epochs 2, 4, 6, 8, 10 |
| Batch size | 4 | from the Step 6a benchmark (D-010); same for A and B |
| Learning rate | 1e-5 | fresh Adam, no EMA, no augmentation |
| Seed | 1234 | per-epoch seed = seed + epoch; per-image sampling seed = seed × 1000 + image index |
| Training set | 800 pairs: 575 Dark + 225 Scenes | seeded random draw from the EUVP Dark and Scenes training folders, minus exact and near duplicates of any test image |
| Train fingerprint | `6a9f33de995c` | MD5 of the sorted training file names, first 12 hex digits |
| Test set | 30 held-out Dark pairs (seed 1234) | split file `test_split_dark30.json`; fingerprint printed by notebook Step 3 |
| Evaluated images | 30 | reduce only by decision, identically for all runs |
| Metrics | scikit-image PSNR and SSIM, `data_range=255`, `channel_axis=2`, 256×256 | output vs reference; also the colour-compensated input vs reference |
| Script | `finetune.py`, md5 in the front matter | any change to the script is a decision |

## Deliverable map (assignment requirement → where it is)

| Requirement | Artifact |
|---|---|
| Code with `# MODIFIED` / `# ADDED` markers; x as a named constant at the top | `../finetune.py` (`X = 2.00`) |
| README with commands, seed, environment | `../README.md` and the run files |
| CSV with epoch and train_loss per fine-tuning run | `data/RunA/train_log.csv`, `data/RunB/train_log.csv` |
| Generated samples at 5 equally spaced epochs (≥ 3 samples each) | `runs/Run{A,B}/samples/epoch_XX/` (Drive), summarised in the run files |
| Inference trajectories at 5 timesteps (≥ 3 samples) | `idx*_traj.png` in the same folders |
| Baseline with no fine-tuning (Run 0) | `Run0.md`, `data/Run0/` |
| Report | `../report/Report.md` (draft of 2026-10-30; figures in `../report/figures/`, made by `../report/make_figures.py`, tables in `../report/tables.md`) |

## Status
See the first table of `RESULTS.md` (rebuilt by `collate.py`). Current state, written by hand on 2026-10-30 about 01:30 IST: `Run0`, `RunA` and `RunB` are all `done` (30 evaluation images each); `Run0_legacy` is `done`. Next: the report.

## Open items
- Report draft open items: Run 0 sample images for Figure 6, page/line evidence for DiffWater's pretraining data, library versions, contribution statement (listed at the top of `report/Report.md`).
- `frozen.split_fingerprint`: filled 2026-10-29 (D-015) from the Step 3 print in Run A session 2. Still to confirm: the train fingerprint printed in session 2 (not captured, see `RunA.md`).
- Instructor approval of the model change (UW-DiffPhys → DiffWater) and the evaluation set.
- Evidence (page/line) from the DiffWater paper on what it was pretrained on.
- Composition of `test_samples` (affects only the legacy result).
