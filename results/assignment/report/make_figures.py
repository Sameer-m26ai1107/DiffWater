"""Builds the report figures and tables from the run data in ../experiment/data.
Usage: python3 -I report/make_figures.py        (run from results/assignment)
Reads only files; writes report/figures/*.png and report/tables.md."""
import csv, math, statistics as st
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "experiment" / "data"
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)
X = 2.0
COL = {"Run 0": "#6b7280", "Run A": "#1f77b4", "Run B": "#d62728"}

# ------------------------------------------------------------------ schedule (Figure 1)
T = 2000
betas = np.linspace(1e-6, 1e-2, T, dtype=np.float64)      # DiffWater: linear, 1e-6 .. 1e-2, T = 2000
abar = np.cumprod(1 - betas); abarx = abar ** X
t = np.arange(1, T + 1)                                   # t = 1..T (the code's integer index is t - 1)
snr = abar / (1 - abar); snrx = abarx / (1 - abarx)
alphax = abarx / np.append(1., abarx[:-1]); betax = 1 - alphax
facts = {
    "abar_T": abar[-1], "abarx_T": abarx[-1], "abar_1": abar[0],
    "beta_x_min": betax.min(), "beta_x_max": betax.max(),
    "t_half_A": int(np.argmax(abar < 0.5) + 1), "t_half_B": int(np.argmax(abarx < 0.5) + 1),
    "t_noise_A": int(np.argmax(abar < 0.01) + 1), "t_noise_B": int(np.argmax(abarx < 0.01) + 1),
    "max_amp_A": float(np.sqrt(1 / abar).max()), "max_amp_B": float(np.sqrt(1 / abarx).max()),
    "all_in_01": bool(((abar > 0) & (abar < 1) & (abarx > 0) & (abarx < 1)).all()),
    "monotone": bool((np.diff(abar) < 0).all() and (np.diff(abarx) < 0).all()),
}
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
ax[0].plot(t, abar, color=COL["Run A"], label=r"$\theta_t=\bar\alpha_t$ (Run A)")
ax[0].plot(t, abarx, color=COL["Run B"], label=r"$\theta_t^{x}=\bar\alpha_t^{\,2.00}$ (Run B)")
ax[0].set_xlabel("t"); ax[0].set_ylabel(r"$\theta_t$"); ax[0].set_title("(a) schedule"); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].plot(t, 10 * np.log10(snr), color=COL["Run A"], label="Run A"); ax[1].plot(t, 10 * np.log10(snrx), color=COL["Run B"], label="Run B")
ax[1].axhline(0, color="k", lw=.6); ax[1].set_xlabel("t"); ax[1].set_ylabel("SNR (dB)")
ax[1].set_title(r"(b) SNR$_t=\bar\alpha_t/(1-\bar\alpha_t)$"); ax[1].legend(); ax[1].grid(alpha=.3)
ax[2].plot(t, 10 * np.log10(abar / (1 + abar)), color="k")
ax[2].set_xlabel("t"); ax[2].set_ylabel("dB"); ax[2].set_title(r"(c) SNR$'$/SNR $=\bar\alpha_t/(1+\bar\alpha_t)$ in dB"); ax[2].grid(alpha=.3)
plt.tight_layout(); plt.savefig(FIG / "fig1_schedule.png", dpi=150); plt.close()

# ------------------------------------------------------------------ loss curves (Figure 2)
def read_csv(p): return list(csv.DictReader(open(p)))
loss = {r: read_csv(DATA / r / "train_log.csv") for r in ("RunA", "RunB")}
steps = {r: [(int(a), int(b), float(c)) for a, b, c in csv.reader(open(DATA / r / "train_steps.csv"))] for r in ("RunA", "RunB")}
fig, ax = plt.subplots(figsize=(8, 4.2))
for r, lab in (("RunA", "Run A"), ("RunB", "Run B")):
    y = np.array([s[2] for s in steps[r]]); x = np.array([(s[0] - 1) + s[1] / 200 for s in steps[r]])
    k = 100; ys = np.convolve(y, np.ones(k) / k, mode="valid")
    ax.plot(x[k - 1:], ys, color=COL[lab], alpha=.35, lw=1.2)
    ax.plot([int(l["epoch"]) - .5 for l in loss[r]], [float(l["train_loss"]) for l in loss[r]], "o-", color=COL[lab], label=f"{lab}: epoch mean")
ax.set_xlabel("epoch"); ax.set_ylabel("train loss (L1 on predicted noise)"); ax.set_xlim(0, 10); ax.grid(alpha=.3)
ax.set_title("Fine-tuning loss, Run A and Run B (thin line: 100-step moving mean)"); ax.legend()
plt.tight_layout(); plt.savefig(FIG / "fig2_loss.png", dpi=150); plt.close()

# ------------------------------------------------------------------ samples per epoch (Figures 3a, 3b)
EPOCHS = (2, 4, 6, 8, 10)
def img(p): return np.asarray(Image.open(p).convert("RGB"))
ep_metrics = {}
for r, lab in (("RunA", "Run A"), ("RunB", "Run B")):
    fig, ax = plt.subplots(3, 7, figsize=(17.5, 7.6))
    for k in (1, 2, 3):
        d10 = DATA / r / "samples" / "epoch_10"
        cols = [(d10 / f"idx{k:02d}_input.png", "input (compensated)")]
        for e in EPOCHS:
            m = read_csv(DATA / r / "samples" / f"epoch_{e:02d}" / "metrics.csv")[k - 1]
            ep_metrics[(r, e, k)] = (float(m["psnr_out"]), float(m["ssim_out"]))
            cols.append((DATA / r / "samples" / f"epoch_{e:02d}" / f"idx{k:02d}_output.png", f"{lab}, epoch {e}\nPSNR {float(m['psnr_out']):.2f}"))
        cols.append((d10 / f"idx{k:02d}_target.png", "reference"))
        for j, (p, ttl) in enumerate(cols):
            ax[k - 1][j].imshow(img(p)); ax[k - 1][j].axis("off"); ax[k - 1][j].set_title(ttl, fontsize=9)
        ax[k - 1][0].text(-0.05, .5, f"test image {k}", transform=ax[k - 1][0].transAxes, rotation=90, va="center", ha="right", fontsize=10)
    plt.tight_layout(); plt.savefig(FIG / f"fig3_samples_{lab.replace(' ', '')}.png", dpi=110); plt.close()

# ------------------------------------------------------------------ trajectories (Figure 4)
TS = ["t = 1999", "t = 1499", "t = 1000", "t = 500", "x$_0$ (t = 0)"]
fig, ax = plt.subplots(6, 5, figsize=(12.5, 15.4))
row = 0
for r, lab in (("RunA", "Run A"), ("RunB", "Run B")):
    for k in (1, 2, 3):
        strip = img(DATA / r / "samples" / "epoch_10" / f"idx{k:02d}_traj.png")
        for j in range(5):
            a = ax[row][j]; a.imshow(strip[:, j * 256:(j + 1) * 256]); a.set_xticks([]); a.set_yticks([])
            if row == 0: a.set_title(TS[j], fontsize=11)
            if j == 0: a.set_ylabel(f"{lab}\nimage {k}", fontsize=10)
        row += 1
plt.tight_layout(); plt.savefig(FIG / "fig4_trajectories.png", dpi=100); plt.close()

# ------------------------------------------------------------------ test-set scores (Figure 5) and tables
R = {n: read_csv(DATA / n / "eval_metrics.csv") for n in ("Run0", "RunA", "RunB")}
lab = {"Run0": "Run 0", "RunA": "Run A", "RunB": "Run B"}
col = lambda n, k: [float(x[k]) for x in R[n]]
idx = np.arange(1, 31)
fig, ax = plt.subplots(1, 3, figsize=(16, 4.2))
ax[0].plot(idx, col("Run0", "psnr_in"), "s", color="#bbbbbb", ms=4, label="input (compensated)")
for n in R: ax[0].plot(idx, col(n, "psnr_out"), "o-", lw=.8, ms=4, color=COL[lab[n]], label=lab[n])
ax[0].set_xlabel("test image"); ax[0].set_ylabel("PSNR (dB)"); ax[0].set_title("(a) PSNR per test image"); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
ax[1].plot(idx, col("Run0", "ssim_in"), "s", color="#bbbbbb", ms=4, label="input (compensated)")
for n in R: ax[1].plot(idx, col(n, "ssim_out"), "o-", lw=.8, ms=4, color=COL[lab[n]], label=lab[n])
ax[1].set_xlabel("test image"); ax[1].set_ylabel("SSIM"); ax[1].set_title("(b) SSIM per test image"); ax[1].grid(alpha=.3)
d = np.array(col("RunB", "psnr_out")) - np.array(col("RunA", "psnr_out"))
ax[2].bar(idx, d, color=np.where(d < 0, COL["Run B"], COL["Run A"]))
ax[2].axhline(0, color="k", lw=.6); ax[2].set_xlabel("test image"); ax[2].set_ylabel("PSNR(B) - PSNR(A)  (dB)"); ax[2].set_title("(c) Run B minus Run A, per image"); ax[2].grid(alpha=.3)
plt.tight_layout(); plt.savefig(FIG / "fig5_scores.png", dpi=150); plt.close()

def ms(v): return st.mean(v), st.stdev(v)
def paired(a, b, k):
    dd = [y - x for x, y in zip(col(a, k), col(b, k))]
    m = st.mean(dd); se = st.stdev(dd) / math.sqrt(len(dd)); return m, se, sum(v > 0 for v in dd), min(dd), max(dd)
out = ["### Test-set scores (output vs reference, 30 held-out Underwater Dark pairs)", "",
       "| Condition | PSNR (dB) mean ± sd | SSIM mean ± sd |", "|---|---|---|"]
pm, pss = ms(col("Run0", "psnr_in")), ms(col("Run0", "ssim_in"))
out.append(f"| Input (colour-compensated), no model | {pm[0]:.2f} ± {pm[1]:.2f} | {pss[0]:.3f} ± {pss[1]:.3f} |")
for n in R:
    a, b = ms(col(n, "psnr_out")), ms(col(n, "ssim_out"))
    out.append(f"| {lab[n]} | {a[0]:.2f} ± {a[1]:.2f} | {b[0]:.3f} ± {b[1]:.3f} |")
out += ["", "### Paired differences (per image, first minus second)", "",
        "| Comparison | Metric | Mean difference | s.e. | |mean|/s.e. | Second run higher on | Range |", "|---|---|---|---|---|---|---|"]
for a, b in (("Run0", "RunA"), ("Run0", "RunB"), ("RunA", "RunB")):
    for k, nm in (("psnr_out", "PSNR (dB)"), ("ssim_out", "SSIM")):
        m, se, w, lo, hi = paired(a, b, k)
        fmt = "{:+.2f}" if k == "psnr_out" else "{:+.3f}"
        out.append(f"| {lab[b]} − {lab[a]} | {nm} | {fmt.format(m)} | {se:.3f} | {abs(m) / se:.1f} | {w}/30 | {fmt.format(lo)} to {fmt.format(hi)} |")
out += ["", "### Epoch samples (mean over the 3 sampled test images, PSNR / SSIM)", "", "| Epoch | Run A | Run B |", "|---|---|---|"]
for e in EPOCHS:
    cells = []
    for r in ("RunA", "RunB"):
        p = np.mean([ep_metrics[(r, e, k)][0] for k in (1, 2, 3)]); s = np.mean([ep_metrics[(r, e, k)][1] for k in (1, 2, 3)])
        cells.append(f"{p:.2f} / {s:.3f}")
    out.append(f"| {e} | {cells[0]} | {cells[1]} |")
out += ["", "### Schedule facts (computed in float64, t = 1..T)", ""] + [f"- {k}: {v}" for k, v in facts.items()]
(HERE / "tables.md").write_text("\n".join(out) + "\n")

# ------------------------------------------------------------------ Run 0 vs A vs B samples (Figure 6), if Run 0 images are present
r0 = DATA / "Run0" / "final_eval"
have0 = all((r0 / f"idx{k:02d}_output.png").exists() for k in (1, 2, 3))
ncol = 5 if have0 else 4
fig, ax = plt.subplots(3, ncol, figsize=(3.4 * ncol, 10.4))
for k in (1, 2, 3):
    row = [(DATA / "RunA" / "samples" / "epoch_10" / f"idx{k:02d}_input.png", "input (compensated)")]
    if have0: row.append((r0 / f"idx{k:02d}_output.png", f"Run 0 (pretrained)\nPSNR {float(R['Run0'][k-1]['psnr_out']):.2f}"))
    row.append((DATA / "RunA" / "samples" / "epoch_10" / f"idx{k:02d}_output.png", f"Run A, epoch 10\nPSNR {float(R['RunA'][k-1]['psnr_out']):.2f}"))
    row.append((DATA / "RunB" / "samples" / "epoch_10" / f"idx{k:02d}_output.png", f"Run B, epoch 10\nPSNR {float(R['RunB'][k-1]['psnr_out']):.2f}"))
    row.append((DATA / "RunA" / "samples" / "epoch_10" / f"idx{k:02d}_target.png", "reference"))
    row = row if have0 else [row[0], row[1], row[2], row[3]]
    if not have0: row = [row[0]] + row[1:3] + [(row[-1][0], row[-1][1])]
    for j, (p, ttl) in enumerate(row[:ncol]):
        ax[k - 1][j].imshow(img(p)); ax[k - 1][j].axis("off"); ax[k - 1][j].set_title(ttl, fontsize=9)
plt.tight_layout(); plt.savefig(FIG / "fig6_compare_epoch10.png", dpi=110); plt.close()
print("Run 0 images present:", have0)
for k, v in facts.items(): print(k, v)
print("figures:", sorted(p.name for p in FIG.glob("*.png")))
