#!/usr/bin/env python3
"""Compile the run files in this folder into RESULTS.md.  Standard library only.

  python3 collate.py            # from the experiment/ folder
  python3 collate.py --dir PATH # or point it at another copy of the folder

Reads:  EXPERIMENT.md (frozen.* settings), Run*.md (front matter), data/<RunName>/eval_metrics.csv.
Writes: RESULTS.md (GENERATED, never edit by hand).
Prints the warnings to the terminal as well.  Exit code 1 if there are warnings.
"""
import argparse
import csv
import datetime
import glob
import math
import os
import re
import statistics as st
import sys

STRING_SUFFIXES = ("fingerprint", "md5", "commit", "checkpoint", "gpu", "torch", "python", "owner", "account",
                   "started", "finished", "results_dir", "status", "run", "tag")
TRAIN_ONLY = {"epochs", "batch_size", "lr", "n_train", "train_dark", "train_scenes", "train_fingerprint"}
AB_MUST_MATCH = ["epochs", "batch_size", "lr", "seed", "n_train", "train_dark", "train_scenes",
                 "train_fingerprint", "n_eval", "checkpoint", "finetune_md5"]
ALL_MUST_MATCH = ["split_fingerprint", "n_eval", "checkpoint", "seed"]
REQUIRED_WHEN_DONE = ["owner", "started", "gpu", "exponent", "n_eval", "psnr_out_mean", "ssim_out_mean", "split_fingerprint",
                      "finetune_md5", "checkpoint"]
REQUIRED_WHEN_DONE_TRAIN = ["epochs", "batch_size", "lr", "n_train", "train_fingerprint", "final_train_loss"]


def parse_value(key, raw):
    raw = re.sub(r"\s+#.*$", "", raw).strip()
    if raw == "" or raw.lower() in ("null", "none", "tbd"):
        return None
    if any(key.endswith(s) for s in STRING_SUFFIXES):
        return raw
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        return raw


def parse_front(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: no front matter (file must start with ---)")
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}: bad front matter line: {line!r}")
        k, v = line.split(":", 1)
        fm[k.strip()] = parse_value(k.strip(), v)
    raise ValueError(f"{path}: front matter is not closed with ---")


def same(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12)
    return str(a) == str(b)


def read_csv(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return {int(r["idx"]): {k: float(v) for k, v in r.items() if k != "idx"} for r in rows}


def mean_std(xs):
    return (st.mean(xs), st.stdev(xs) if len(xs) > 1 else 0.0)


def fg(x):
    return "–" if x is None else (f"{x:g}" if isinstance(x, float) else str(x))


def fmt(x, nd=3):
    return "–" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.dirname(os.path.abspath(__file__)))
    d = ap.parse_args().dir
    warnings, runs = [], {}

    exp = parse_front(os.path.join(d, "EXPERIMENT.md"))
    frozen = {k[len("frozen."):]: v for k, v in exp.items() if k.startswith("frozen.")}

    for path in sorted(glob.glob(os.path.join(d, "Run*.md"))):
        name = os.path.splitext(os.path.basename(path))[0]
        try:
            fm = parse_front(path)
        except ValueError as e:
            warnings.append(str(e)); continue
        fm["_name"] = name
        csvp = os.path.join(d, "data", name, "eval_metrics.csv")
        fm["_csv"] = read_csv(csvp) if os.path.exists(csvp) else None
        fm["_main"] = fm.get("tag") == "main"
        runs[name] = fm

    main_runs = {r["run"]: r for r in runs.values() if r["_main"]}
    by_status = lambda r: r.get("status")

    # ---------------- checks ----------------
    for name, r in runs.items():
        if r.get("status") not in ("not_started", "running", "interrupted", "done", "failed", "abandoned"):
            warnings.append(f"{name}: unknown status {r.get('status')!r}")
        if r.get("status") == "done":
            req = REQUIRED_WHEN_DONE + ([] if r.get("run") == "0" else REQUIRED_WHEN_DONE_TRAIN)
            if r["_main"]:
                missing = [k for k in req if r.get(k) is None]
                if missing:
                    warnings.append(f"{name}: status is done but these front matter fields are empty: {', '.join(missing)}")
                if r["_csv"] is None:
                    warnings.append(f"{name}: no data/{name}/eval_metrics.csv")
        if r["_csv"]:
            ps = [v["psnr_out"] for v in r["_csv"].values()]; ss = [v["ssim_out"] for v in r["_csv"].values()]
            if r.get("n_eval") is not None and r["n_eval"] != len(r["_csv"]):
                warnings.append(f"{name}: n_eval={r['n_eval']} but eval_metrics.csv has {len(r['_csv'])} rows")
            if r.get("psnr_out_mean") is not None and abs(r["psnr_out_mean"] - mean_std(ps)[0]) > 0.01:
                warnings.append(f"{name}: front matter psnr_out_mean {r['psnr_out_mean']} differs from the CSV mean {mean_std(ps)[0]:.3f}")
            if r.get("ssim_out_mean") is not None and abs(r["ssim_out_mean"] - mean_std(ss)[0]) > 0.001:
                warnings.append(f"{name}: front matter ssim_out_mean {r['ssim_out_mean']} differs from the CSV mean {mean_std(ss)[0]:.4f}")
        if r["_main"] and r.get("status") not in ("not_started", None):
            expo = {"0": frozen.get("exponent_A"), "A": frozen.get("exponent_A"), "B": frozen.get("exponent_B")}.get(r["run"])
            if expo is not None and r.get("exponent") is not None and not same(r["exponent"], expo):
                warnings.append(f"{name}: exponent {r['exponent']} but the design says {expo}")
            for k, fv in frozen.items():
                if k in ("exponent_A", "exponent_B") or fv is None:
                    continue
                if r.get("run") == "0" and k in TRAIN_ONLY:
                    continue
                if r.get(k) is not None and not same(r[k], fv):
                    warnings.append(f"{name}: {k} = {r[k]} differs from the frozen value {fv}")

    started = [r for r in main_runs.values() if r.get("status") != "not_started"]
    for k in ALL_MUST_MATCH:
        vals = {r["_name"]: r.get(k) for r in started if r.get(k) is not None}
        if len(set(map(str, vals.values()))) > 1:
            warnings.append(f"{k} differs between runs: {vals}")
    if "A" in main_runs and "B" in main_runs:
        for k in AB_MUST_MATCH:
            a, b = main_runs["A"].get(k), main_runs["B"].get(k)
            if a is not None and b is not None and not same(a, b):
                warnings.append(f"RunA and RunB differ in {k}: A={a}, B={b}. A and B must be identical except for the exponent.")
        if main_runs["A"]["_csv"] and main_runs["B"]["_csv"] and set(main_runs["A"]["_csv"]) != set(main_runs["B"]["_csv"]):
            warnings.append("RunA and RunB eval_metrics.csv cover different image indices")

    # ---------------- report ----------------
    out = ["# RESULTS (generated)", "",
           f"> **GENERATED FILE. Do not edit by hand.** Rebuilt by `collate.py` on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} (local time). Source: the front matter of the `Run*.md` files and `data/<RunName>/eval_metrics.csv`.", ""]

    out += ["## Warnings", ""]
    out += [f"- ⚠ {w}" for w in warnings] if warnings else ["None."]
    out += ["", "## Status of the runs", "",
            "| File | Run | Tag | Status | Owner | GPU | Started | Total min | n_eval | PSNR out | SSIM out | PSNR in | SSIM in |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in runs.items():
        out.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            name, r.get("run", ""), r.get("tag", ""), r.get("status", ""), fmt(r.get("owner")), fmt(r.get("gpu")),
            fmt(r.get("started")), fmt(r.get("total_minutes"), 1), fmt(r.get("n_eval")),
            "–" if r.get("psnr_out_mean") is None else f"{r['psnr_out_mean']:.2f} ± {fmt(r.get('psnr_out_std'), 2)}",
            "–" if r.get("ssim_out_mean") is None else f"{r['ssim_out_mean']:.3f} ± {fmt(r.get('ssim_out_std'), 3)}",
            fmt(r.get("psnr_in_mean"), 2), fmt(r.get("ssim_in_mean"), 3)))

    out += ["", "## Settings check (frozen values from EXPERIMENT.md)", "",
            "| Setting | Frozen | " + " | ".join(f"Run{k}" for k in ("0", "A", "B")) + " |", "|---|---|---|---|---|"]
    for k in ["exponent", "epochs", "batch_size", "lr", "seed", "n_train", "train_dark", "train_scenes", "train_fingerprint",
              "split_fingerprint", "n_eval", "checkpoint", "finetune_md5"]:
        fv = "0, A: " + fg(frozen.get("exponent_A")) + " / B: " + fg(frozen.get("exponent_B")) if k == "exponent" else frozen.get(k)
        out.append(f"| {k} | {fg(fv)} | " + " | ".join(fg(main_runs[x].get(k)) if x in main_runs else "–" for x in ("0", "A", "B")) + " |")

    # paired comparisons on the main runs
    csvs = {k: r["_csv"] for k, r in main_runs.items() if r["_csv"] and r.get("status") == "done"}
    out += ["", "## Paired comparisons (main runs, same test images)", ""]
    if len(csvs) >= 2:
        common = sorted(set.intersection(*[set(c) for c in csvs.values()]))
        out += [f"Images scored by every finished run: **{len(common)}**. Difference = first minus second, per image. "
                "Rule of thumb: |mean| below 2 standard errors is not distinguishable from zero with this sample.", "",
                "| Comparison | Metric | n | Mean diff | s.e. | Wins | Verdict |", "|---|---|---|---|---|---|---|"]
        pairs = [("A", "0"), ("B", "0"), ("B", "A")]
        for x, y in pairs:
            if x in csvs and y in csvs:
                for m, nm in (("psnr_out", "PSNR (dB)"), ("ssim_out", "SSIM")):
                    diffs = [csvs[x][i][m] - csvs[y][i][m] for i in common]
                    mean = st.mean(diffs); se = st.stdev(diffs) / math.sqrt(len(diffs)) if len(diffs) > 1 else float("nan")
                    wins = sum(v > 0 for v in diffs)
                    verdict = "distinguishable" if abs(mean) > 2 * se else "not distinguishable from 0"
                    out.append(f"| Run{x} − Run{y} | {nm} | {len(diffs)} | {mean:+.3f} | {se:.3f} | {wins}/{len(diffs)} | {verdict} |")
        out += ["", "| Run | PSNR out (mean ± std) | SSIM out (mean ± std) | PSNR in | SSIM in |", "|---|---|---|---|---|"]
        for k in ("0", "A", "B"):
            if k in csvs:
                c = csvs[k]
                p, s = mean_std([c[i]["psnr_out"] for i in common]), mean_std([c[i]["ssim_out"] for i in common])
                out.append(f"| Run{k} | {p[0]:.2f} ± {p[1]:.2f} | {s[0]:.3f} ± {s[1]:.3f} | "
                           f"{st.mean(c[i]['psnr_in'] for i in common):.2f} | {st.mean(c[i]['ssim_in'] for i in common):.3f} |")
    else:
        out.append("Not available yet: needs at least two finished main runs with `data/<RunName>/eval_metrics.csv`.")

    legacy = [r for r in runs.values() if r.get("tag") == "legacy"]
    variants = [r for r in runs.values() if r.get("tag") not in ("main", "legacy", None)]
    if legacy:
        out += ["", "## Legacy results (different test images, never compared with the main runs)", ""]
        for r in legacy:
            out.append(f"- **{r['_name']}**: PSNR {fmt(r.get('psnr_out_mean'), 3)} ± {fmt(r.get('psnr_out_std'), 3)}, "
                       f"SSIM {fmt(r.get('ssim_out_mean'), 3)} ± {fmt(r.get('ssim_out_std'), 3)} (n = {fmt(r.get('n_eval'))}).")
    if variants:
        out += ["", "## Variant runs (tagged, reported separately)", ""]
        for r in variants:
            out.append(f"- **{r['_name']}** (tag {r['tag']}, status {r.get('status')}): PSNR {fmt(r.get('psnr_out_mean'), 3)}, SSIM {fmt(r.get('ssim_out_mean'), 3)}.")
    out.append("")

    open(os.path.join(d, "RESULTS.md"), "w", encoding="utf-8").write("\n".join(out))
    print(f"wrote {os.path.join(d, 'RESULTS.md')}  ({len(runs)} run files, {len(warnings)} warnings)")
    for w in warnings:
        print("WARNING:", w)
    sys.exit(1 if warnings else 0)


if __name__ == "__main__":
    main()
