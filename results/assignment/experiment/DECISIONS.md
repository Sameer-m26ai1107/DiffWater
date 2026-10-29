# Decision log

One entry per decision, newest last. Entries are never deleted: if a decision is reversed, add a new entry that supersedes it and mark the old one `superseded by D-0NN`.

Format: **D-NNN · date · status** (`active`, `pending`, `superseded`) · decision · why · alternatives considered · affects.

---

**D-001 · 2026-10-28 · active** · Replace UW-DiffPhys by DiffWater (Guan-MS/DiffWater) as the model.
Why: the UW-DiffPhys checkpoint is on a restricted Google Drive and cannot be opened, and training it from scratch on a Colab T4 is infeasible. DiffWater is a conditional DDPM for underwater enhancement, open code (Apache-2.0), public weights, and uses θₜ = ᾱₜ.
Alternatives: wait for access (no time), train from scratch (days).
Affects: everything. **Not yet approved by the instructor.**

**D-002 · 2026-10-28 · active** · Use the LSUI checkpoint `I390000_E78_gen.pth` (593 MB, generator only).
Why: it was in the authors' public folder; the generator file is all inference and fine-tuning need. The `UIEB` checkpoint was not evaluated.
Affects: all runs.

**D-003 · 2026-10-28 · active** · θₜ is defined as ᾱₜ = ∏(1 − βₜ). Run B uses θₜ^x with x = 2.00; all per-step αₜ, βₜ, posterior variance and mean coefficients are re-derived from the new cumulative product, and the schedule is re-applied after every checkpoint load.
Why: training noising and sampling must use one consistent schedule. The schedule buffers are stored inside the checkpoint's `state_dict`, so loading overwrites a modified schedule unless it is re-applied.
Affects: Run B (and the assertion in all runs).

**D-004 · 2026-10-28 · active (legacy)** · First Run 0 on the EUVP `test_samples` folder, 30 images, one seed for the whole run, repo's unmodified `test.py`. Result: PSNR 17.723, SSIM 0.732.
Why: first working baseline. **Kept only as `Run0_legacy`.**

**D-005 · 2026-10-29 · active** · Evaluate Run 0, A and B on 30 **held-out Underwater Dark** pairs taken from `trainA`/`trainB`, not on `test_samples`.
Why: the declaration names Dark and Scenes; `test_samples` has unknown composition; the EUVP `validation` folder has no reference images (1 of 570 names matches a `trainB` name) and contains byte-identical copies of training files (10 Dark, 1 Scenes).
Decided before any new result existed. The decision rests on the declaration and the data audit, not on metric values.
Affects: Run 0 must be repeated; all comparisons.

**D-006 · 2026-10-29 · active** · Training files that are exact (MD5) or near (64-bit dHash, Hamming distance ≤ 6) duplicates of a test image are removed from the training pool.
Why: prevent leakage. Same-scene-different-frame correlation is not removed (limitation shared with EUVP's own split).

**D-007 · 2026-10-29 · active** · Run 0 is repeated through `finetune.py --run 0`: pretrained weights, no training, the same sampler code and per-image seeds as A and B.
Why: makes Run 0, A and B directly comparable image by image and removes the seed confound of the first Run 0.

**D-008 · 2026-10-29 · active** · Fine-tune hyperparameters, identical for A and B: 10 epochs over 800 pairs, learning rate 1e-5, fresh Adam, no EMA, no augmentation, seed 1234 (per-epoch seed = seed + epoch).
Why: the authors pre-trained with 3e-6 at batch size 1; we train a few thousand steps only, so a moderately larger rate is used. No EMA or augmentation because the repo has none in the training path. Batch size is set from the benchmark (see D-010).

**D-009 · 2026-10-29 · active** · Training set: a seeded random draw of 800 pairs from the Dark and Scenes training folders in their natural proportion. Actual first draw: 575 Dark + 225 Scenes, fingerprint `6a9f33de995c`.
Alternatives: Dark-only, Scenes-only or a 50/50 mix. These would test the effect of training-data composition and are deferred as an exploratory extension, run with schedule A only, after the main experiment.

**D-010 · 2026-10-29 · active** · Batch size, and the number of evaluated images (planned 30; 20 if only one GPU session is available). To be fixed from the Step 6a benchmark and the available sessions. The same value for A and B.
Benchmark (Run A session, T4, source `data/RunA/cell_output.txt`): batch 1: 0.35 s/step, 3.3 GB; batch 2: 0.62 s/step, 4.6 GB; batch 4: 1.14 s/step, 7.4 GB; batch 8: 1.66 s/step, 13.3 GB.
Recommendation: **batch 4**. It gives 2000 optimisation steps (10 epochs × 200) at 38 min of training and leaves memory headroom. Batch 8 is faster per image but peaks at 13.3 GB on a 15 GB card and would halve the number of steps. **Confirmed by the user on 2026-10-29: batch size 4, `n_eval` 30, `n_samples` 3, 10 epochs.** `frozen.batch_size: 4`.

**D-011 · 2026-10-29 · active** · Runs are spread over separate Google accounts, one run per account. Each account has its own copy of the checkpoint. A resume must happen in the same account. Results are packaged per run (Step 9b) and consolidated later.
Why: Colab GPU quota is per account.

**D-012 · 2026-10-29 · active** · Documentation protocol: one file per run with machine-readable front matter, append-only Log, decisions in this file, results compiled by `collate.py` (see `PROTOCOL.md`).

**D-013 · 2026-10-29 · active** · `finetune.py` smoke mode fixed: the tiny schedule (T=20) is now applied after the checkpoint is loaded. New script md5 `38c97203e8ccafdfb80cb2be74b0bb3a` (`frozen.finetune_md5` updated).
Why: the first smoke test failed with `size mismatch for betas ... checkpoint [2000], model [20]`. The checkpoint stores the schedule buffers with T=2000, so building the model with T=20 failed the strict load. The change touches only `--smoke` code. The real-run path (T=2000) was already exercised by the benchmark.
Affects: every session must re-upload `finetune.py`. A run that started with the previous script (md5 `3fcb89b892df1df144aa6d1e4a2df9b2`) is equivalent for training and evaluation, and must record its md5 and a deviation note.

**D-014 · 2026-10-29 · active** · Every run is launched as a blocking (foreground) cell, `!python -u /content/finetune.py ...`, not as a detached background process. After any disconnect the recovery is: reconnect (same account), re-run the setup cells, check the md5 and both fingerprints, relaunch the identical command; `finetune.py` resumes from `resume.pt` and skips images already written.
Why: Run A's first session was lost to Colab's idle timeout, because the background `Popen` launch does not count as activity. No change to the script or to any frozen setting.
Affects: Run 0, Run B (and the A resume from epoch 8, see `RunA.md`).

**D-015 · 2026-10-29 · active** · (a) `frozen.split_fingerprint` = `f8cc4714a30c`, observed in the Step 3 print of Run A session 2, which also reported that the split equals the one saved on Drive (`test_split_dark30.json`). (b) New notebook `RunAB_Finetune_Guide_v3.ipynb`, built from the as-run `RunAB_Finetune_Guide_v2.ipynb` (which stays unchanged as the record of Run A): outputs cleared; hard-coded Run A relaunch cell removed; Step 8 launch cell is blocking (D-014) and starts only if the script md5, DiffWater commit, train fingerprint (not for Run 0), split fingerprint and the settings (10, 4, 30, 3) equal the frozen values; optional healthchecks.io heartbeat cell; `S_PER_STEP` set to the measured 1.14; monitor cell no longer reads a stdout log file. No change to `finetune.py`.
Why: the frozen experiment is now enforced by the launch cell instead of by hand-checking, and a stale or different session cannot start by mistake.
