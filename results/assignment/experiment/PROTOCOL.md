# Documentation protocol for Run 0, Run A and Run B

Read this before you run anything, before you write anything down, and before you compile results. It applies to people and to AI assistants.

**Goal:** anyone can run one of the runs on any Google account, record it in one file, hand that file over, and the information can be compiled into a single results table without anyone re-asking questions.

## 1. Principles

1. **One file per run** is the single source of truth for that run: `Run0.md`, `RunA.md`, `RunB.md`.
2. **Never invent a number.** If you do not know a value, leave it empty (front matter) or write `TBD` (text). An empty value is information. A guessed value is damage.
3. **Record where each number came from.** In the Log, name the notebook step, the file, or paste the line it came from.
4. **The Log is append-only.** Add lines at the bottom. Do not rewrite or delete earlier lines, even your own. If something was wrong, add a `FIX` line that says what was wrong.
5. **The front matter holds the final state** (it is what the compile script reads). The Log holds the history.
6. **Frozen settings do not change silently.** Anything listed as frozen in `EXPERIMENT.md` is identical across runs. Changing one needs a `DECISIONS.md` entry first, and a new run.
7. **The generated file `RESULTS.md` is never edited by hand.** It is rebuilt by `collate.py`.
8. Dates and times: ISO format `YYYY-MM-DD HH:MM`, and say which clock (Colab clock is UTC, a laptop is local time). Write `UTC` or `IST` after the time.

## 2. Folder layout

```
results/assignment/experiment/
  PROTOCOL.md         this file
  EXPERIMENT.md       design, frozen settings (machine-readable), links
  DECISIONS.md        decision log, one entry per decision
  TEMPLATE_RUN.md     copy this to start a new run file
  Run0.md RunA.md RunB.md   one per run
  Run0_legacy.md      the first Run 0 on test_samples (kept, never compared with the new runs)
  collate.py          rebuilds RESULTS.md from the run files and their CSVs
  RESULTS.md          GENERATED. Do not edit.
  data/<RunName>/     small result files for each run: eval_metrics.csv, train_log.csv, run.log, run_config.json
```

`data/<RunName>/` uses the run file's name without `.md`, for example `data/RunA/eval_metrics.csv`.

## 3. Who does what

| Role | Responsibility |
|---|---|
| **Run owner** (whoever executes the run) | Fills in the run's file: front matter, Log, notes. Sends the file and the zip from notebook Step 9b. |
| **Collator** (a person or an AI assistant) | Copies the files into this folder, runs `collate.py`, reads the warnings, updates `EXPERIMENT.md` and `DECISIONS.md`. Never edits the owner's Log lines. |

## 4. File naming

- Normal runs: `Run0.md`, `RunA.md`, `RunB.md`.
- A later variant (for example a data-composition arm) gets a tag: `RunA_D.md`. Put `tag: D` in the front matter. Anything with a tag other than `main` is excluded from the main A-versus-B comparison and reported separately.
- A re-run of the same run is **not** a new file. Add an `attempt` line in the Log and update the front matter. If an earlier attempt must be kept, rename it `RunA_attempt1.md` with `tag: attempt1` and `status: abandoned`.

## 5. Anatomy of a run file

Every run file is the template `TEMPLATE_RUN.md`: a front matter block between two `---` lines, then fixed sections.

### 5.1 Front matter (machine-readable)
One `key: value` per line. No nesting. `# comment` after a value is allowed. Empty means unknown. `collate.py` reads exactly these keys.

| Key | Meaning | Filled by / when |
|---|---|---|
| `run` | `0`, `A` or `B` | pre-filled |
| `tag` | `main`, `legacy`, or a variant tag | pre-filled |
| `status` | `not_started`, `running`, `interrupted`, `done`, `failed`, `abandoned` | owner, every change |
| `owner` | who ran it (initials or role) | owner at start |
| `account` | which Google account (a label, not the email address) | owner at start |
| `started`, `finished` | ISO time and clock | owner |
| `gpu`, `torch`, `python` | from the ENV block (section 7) | owner at start |
| `diffwater_commit` | from the ENV block | owner at start |
| `finetune_md5` | md5 of the `finetune.py` actually used | owner at start |
| `exponent` | `1` for Run 0 and A, `2.0` for B | pre-filled, owner confirms from `run.log` (`schedule OK`) |
| `epochs`, `batch_size`, `lr`, `seed` | training settings used (blank for Run 0) | owner at start |
| `n_train`, `train_dark`, `train_scenes` | training set size and composition (blank for Run 0) | owner after Step 3 |
| `train_fingerprint` | printed by the cell after Step 3 (blank for Run 0) | owner after Step 3 |
| `split_fingerprint` | printed by Step 3 | owner after Step 3 |
| `n_eval` | test images evaluated | owner |
| `checkpoint` | file name of the pretrained weights | owner |
| `train_minutes`, `eval_minutes`, `total_minutes` | wall-clock, from `run.log` | owner at finish |
| `final_train_loss` | last row of `train_log.csv` (blank for Run 0) | owner at finish |
| `psnr_out_mean`, `psnr_out_std`, `ssim_out_mean`, `ssim_out_std` | output vs reference, over the `n_eval` images | owner at finish |
| `psnr_in_mean`, `ssim_in_mean` | colour-compensated input vs reference | owner at finish |
| `results_dir` | where the full outputs live (Drive path or zip name) | owner at finish |

The FINISH block (section 7) prints these lines ready to paste.

### 5.2 Body sections (fixed order)
1. **Purpose** (pre-filled).
2. **Setup actually used**: anything that differs from `EXPERIMENT.md`, and the cells you ran.
3. **Observations**: what you saw (loss behaviour, sample quality, anything odd).
4. **Issues and fixes**: problems met, in order.
5. **Deviations from the protocol**: anything not done as specified. Write `none` if none.
6. **Log**: append-only history.
7. **Artifacts**: where the files are.

## 6. Log line format

```
- 2026-10-29 14:05 UTC [owner-initials] START  Launched Step 8, RUN="A", epochs 10, batch 4.
```
`[who]` is the person or `[collator]` for compiled notes. Event types:

| Type | Use for |
|---|---|
| `START` | a run begins (also after a resume, with the word `resume`) |
| `PROGRESS` | planned checkpoints: epoch finished, samples written |
| `ISSUE` | something went wrong, with the exact error text if short |
| `FIX` | what was changed in response |
| `DECISION` | a choice made (also add to `DECISIONS.md`) |
| `RESULT` | numbers, with the source |
| `NOTE` | anything else |
| `DONE` | run finished, front matter updated |

## 7. What to record, and when

### Before the run (checklist)
- [ ] `finetune.py` uploaded; run the ENV block below and paste its output into the Log (`NOTE`).
- [ ] Step 3 printed: split fingerprint, and for A and B the train counts and train fingerprint. Copy them to the front matter.
- [ ] Settings in the Step 6b configuration cell match `EXPERIMENT.md`.

### ENV block (run once at the start, paste the output into the Log)
```python
import torch, sys, subprocess, hashlib
print("gpu:", torch.cuda.get_device_name(0)); print("torch:", torch.__version__); print("python:", sys.version.split()[0])
print("diffwater_commit:", subprocess.run(["git", "-C", "/content/DiffWater", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
print("finetune_md5:", hashlib.md5(open("/content/finetune.py", "rb").read()).hexdigest())
```

### During the run
- Log a `PROGRESS` line when epochs finish (copy from `run.log`) and an `ISSUE` line for every error or disconnect. After a disconnect add `START resume` and state the epoch it resumed from.

### FINISH block (run when `run.log` says `ALL DONE`)
Prints the front matter values. Paste them into the run file, replace `RUN` and the path if needed.
```python
import os, re, json, pandas as pd
RUN = "A"                                              # "0", "A" or "B"
A_DIR = "/content/drive/MyDrive/FoundationModel-Assignment"
OUT = f"{A_DIR}/runs/Run{RUN}"
ev = pd.read_csv(f"{OUT}/eval_metrics.csv")
txt = open(f"{OUT}/run.log").read()
secs = lambda h: int(h[:2]) * 3600 + int(h[3:5]) * 60 + int(h[6:8])
stamps = re.findall(r"^(\d\d:\d\d:\d\d) ", txt, re.M)
total = (secs(stamps[-1]) - secs(stamps[0])) % 86400 / 60
cfg = json.load(open(f"{OUT}/run_config.json"))
print("status: done")
print("exponent:", cfg["exponent"])
print("n_eval:", len(ev)); print("total_minutes:", round(total, 1))
if os.path.exists(f"{OUT}/train_log.csv"):
    print("final_train_loss:", round(pd.read_csv(f"{OUT}/train_log.csv").train_loss.iloc[-1], 5))
for k, c in (("psnr_out", "psnr_out"), ("ssim_out", "ssim_out")):
    print(f"{k}_mean:", round(ev[c].mean(), 4)); print(f"{k}_std:", round(ev[c].std(), 4))
print("psnr_in_mean:", round(ev.psnr_in.mean(), 4)); print("ssim_in_mean:", round(ev.ssim_in.mean(), 4))
```
Then copy `eval_metrics.csv`, `train_log.csv`, `run.log` and `run_config.json` from `runs/Run{RUN}/` into `experiment/data/Run{RUN}/` (they are small).

## 8. Reporting to an AI assistant (paste-back format)

When you tell an AI assistant about a run, paste the raw output, not a summary. Always say **which run** it is (`Run A`, `Run B`, `Run 0`) and **which step** produced it. The assistant will:
1. Append `RESULT` / `ISSUE` / `NOTE` lines to that run's Log, with the pasted text as the source.
2. Update the front matter only with values it can read from what you pasted.
3. Add an entry to `DECISIONS.md` for any decision made in the conversation.
4. Run `collate.py` and say which warnings (if any) it raised.

## 9. Disconnects, resumes, retries

- Disconnect during a run: Log `ISSUE`, then after restarting `START resume`, naming the epoch it resumed from (visible in `run.log`: `resumed from epoch N`). Resume in the **same Google account**, because `resume.pt` lives in that account's Drive.
- Run restarted from scratch: keep the old Log lines, add `START attempt 2`, and reset the front matter. If the first attempt produced results you want to keep, follow section 4.

## 10. Frozen settings and deviations

The frozen settings are in the front matter of `EXPERIMENT.md` (keys starting `frozen.`). `collate.py` compares every run with them and compares A with B. A mismatch is a **warning** that must be resolved: either the run was set up wrong (re-run it), or the frozen value must be changed by a `DECISIONS.md` entry that explains why, and then all affected runs are repeated.

## 11. Sharing and merging files between people

1. Each owner edits only their own run file.
2. Send the run file and the three or four small data files (section 7) together with the zip from notebook Step 9b.
3. The collator puts the run file in this folder and the data files in `data/<RunName>/`.
4. If two people edited the same file, the collator merges by keeping both Logs in time order and marking the added lines `[collator]`. Never delete a line.
5. After merging, run:
   ```
   python3 collate.py
   ```
   and read the **Warnings** section of `RESULTS.md` first.

## 12. Compiling (collation procedure)

1. Make sure each finished run has its front matter filled and its CSV files in `data/<RunName>/`.
2. `python3 collate.py` (from this folder). It prints warnings and rewrites `RESULTS.md`.
3. Resolve every warning, or add a `NOTE` line to the run file explaining why it is acceptable.
4. Update the status table in `EXPERIMENT.md` if needed, and carry the numbers into `../Run0_Report.md` or a new final report.

## 13. Rules for an AI assistant working in this folder

(These repeat the most important parts for assistants. `../CLAUDE.md` points here.)

- Read this file and `EXPERIMENT.md` before touching anything in `experiment/`.
- When the user reports anything about a run, record it right away in the correct run file, in the format above, and say which file you changed.
- Never fill a field you cannot read from what the user pasted. Never round or "clean up" a number: copy it.
- Never edit `RESULTS.md` by hand. Regenerate it with `collate.py`.
- Never edit a live Colab notebook. Give changes as chat snippets.
- If a user instruction would change a frozen setting, say so, propose the `DECISIONS.md` entry, and wait for confirmation.
- Keep the narrative in `../Experiments_Log.md` for the pre-experiment history only. New facts go into the run files and `DECISIONS.md`.
