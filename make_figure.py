"""Plot proved formulas; no optimisation or numerical fitting is involved.

Run: python3 make_figure.py  (writes figures/exact_coefficients.png next to this file)
"""
from pathlib import Path
import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "entropy_mpl_cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
out = ROOT / "figures"
out.mkdir(exist_ok=True)
q = np.geomspace(1e-4, 0.5, 800)
global_coefficient = np.log(1 / q) / (2 * np.log(2 / q))
threshold = np.exp(q / (1 - q) * np.log(q))

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#28232B", "text.color": "#28232B",
    "xtick.color": "#514B54", "ytick.color": "#514B54",
    "axes.edgecolor": "#C7C0C8", "savefig.facecolor": "white",
})
fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.35), constrained_layout=True)
plum, ochre, teal = "#6D3B70", "#B68031", "#267C78"
axs[0].plot(q, global_coefficient, color=plum, lw=2.4, label="Global KL coefficient")
n_points = np.arange(2, 11)
axs[0].plot(1 / n_points, np.log(n_points) / (2 * np.log(2 * n_points)), "o", ms=4.2,
            color=plum, mfc="white", mew=1.4, clip_on=False, zorder=5, label=r"$K_{n,n}$, $n=2,\ldots,10$")
axs[0].axhline(0.25, color=ochre, ls="--", lw=1.7, label="Local coefficient = 1/4")
axs[0].axhline(0.5, color="#A79FA9", ls=":", lw=1.2)
axs[0].set(title="Bipartite reset chain", ylabel="Contraction coefficient", ylim=(0.225, 0.515))
axs[0].legend(loc="lower left", bbox_to_anchor=(0.0, 0.09), frameon=False, fontsize=9)
axs[1].plot(q, threshold, color=teal, lw=2.4, label=r"Threshold $\alpha_*(q)$")
axs[1].fill_between(q, 0.48, threshold, color=teal, alpha=0.08)
axs[1].axhline(0.5, color=ochre, ls="--", lw=1.7, label="Half retention")
axs[1].set(title="Reverse erasure", ylabel="Retention probability", ylim=(0.47, 1.025))
axs[1].text(0.002, 0.67, "Point inputs optimise\non or below the curve", color=teal, fontsize=10)
axs[1].legend(loc="lower left", bbox_to_anchor=(0.0, 0.13), frameon=False, fontsize=9)
for ax in axs:
    ax.set_xscale("log")
    ax.set_xlim(q[0], q[-1])
    ax.set_xlabel(r"Smallest conditional / prior mass $q$")
    ax.set_xticks([1e-4, 1e-3, 1e-2, 0.1, 0.5])
    ax.set_xticklabels([r"$10^{-4}$", r"$10^{-3}$", "0.01", "0.1", "0.5"])
    ax.grid(axis="y", color="#E9E5E9", lw=0.7)
    ax.set_axisbelow(True)
fig.savefig(out / "exact_coefficients.png", dpi=220)
plt.close(fig)
