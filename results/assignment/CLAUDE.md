# Instructions for AI assistants working in this folder

Project: Group 25, noise schedule ablation on DiffWater (Runs 0, A, B). The user (and their colleagues) run Colab notebooks and report back; you document and compile.

## Always
1. **Before writing anything about a run, read `experiment/PROTOCOL.md` and `experiment/EXPERIMENT.md`.** They define the file layout, the front matter fields, the Log format and the frozen settings.
2. **When the user reports anything about Run 0, A or B** (output, error, number, decision), record it in the same turn:
   - append a Log line to the correct `experiment/Run*.md` (`RESULT`, `ISSUE`, `FIX`, `NOTE`, ...), with the pasted text as the source;
   - update the front matter only with values you can read from what was pasted;
   - add a `DECISIONS.md` entry for any decision;
   - run `python3 experiment/collate.py` and mention any warning;
   - tell the user which files you changed.
3. **Never invent or round a number.** Unknown means an empty field or `TBD`.
4. **Never edit `experiment/RESULTS.md` by hand.** It is generated.
5. **Never edit a Colab notebook the user is running.** Give fixes as chat snippets. New versions go into new files.
6. **Frozen settings** (the `frozen.*` keys in `EXPERIMENT.md`) change only through a `DECISIONS.md` entry that the user has confirmed, and affected runs are repeated.
7. A and B must be identical except for the exponent. If a pasted value shows they are not, say so immediately.

## Facts that are easy to get wrong
- This project uses **DiffWater** (`Guan-MS/DiffWater`), not UW-DiffPhys, although the git repo around this folder is a UW-DiffPhys clone.
- The test set is 30 **held-out Underwater Dark** pairs. The earlier Run 0 on `test_samples` is `Run0_legacy` and is never compared with the main runs.
- θₜ = ᾱₜ. Run B uses ᾱₜ^x with x = 2.00. The schedule buffers live inside the checkpoint, so the schedule must be re-applied after loading (the script does this and asserts it).
- `0_k_input.png` / `idxNN_input.png` is the colour-compensated input, not the raw image.

## Style
- Plain language. The user is learning diffusion models: when you explain, say what a quantity is before using it, and point to the relevant step of `RunAB_Finetune_Guide_v3.ipynb`.
- Facts first, interpretation labelled as such. Report outcomes faithfully, including failures.
- Use they/them for people whose pronouns are not stated.
