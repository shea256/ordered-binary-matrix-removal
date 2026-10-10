#!/usr/bin/env python3
"""Render the README size comparison with optional Matplotlib 3.9.4.

Sources: BASELINE.md and the three candidate proofs linked from README.md.
The x-axis records refinement order, not elapsed time. The y-axis measures
the fixed pattern's side length, not host size, copy density, or runtime.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
SIZES = (66, 15, 5, 4)
STAGES = (
    "OpenAI baseline\nSep 25, 2026",
    "First refinement\nOct 10, 2026",
    "Second refinement\nOct 10, 2026",
    "Current refinement\nOct 10, 2026",
)
BASELINE = "#555555"
EARLIER = "#2C7FCC"
CURRENT = "#129B78"
INK = "#171A1C"
MUTED = "#646B70"


def main():
    status = json.loads((ROOT / "results/current.json").read_text())
    assert SIZES[0] == status["baseline_pattern_size"]
    assert SIZES[-1] == status["pattern_size"]
    assert status["status"] == "candidate"

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 14,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
        "svg.hashsalt": "ordered-binary-matrix-removal-size-history",
    })
    fig = plt.figure(figsize=(16, 9.6), facecolor="white")
    ax = fig.add_axes([0.087, 0.235, 0.865, 0.565])

    fig.text(0.06, 0.935,
             "Ordered binary matrix removal: 66×66 → 4×4",
             fontsize=24, color=INK)
    fig.text(0.087, 0.848,
             "Smaller fixed forbidden patterns. All constructions use arbitrarily large host matrices.",
             fontsize=15, color=MUTED)

    ax.set_xlim(-0.12, 3.48)
    ax.set_ylim(0, 72)
    ax.set_yticks(range(0, 71, 10))
    ax.set_xticks(range(4), STAGES)
    ax.tick_params(axis="both", which="both", length=0, pad=10, labelcolor=MUTED)
    ax.tick_params(axis="x", labelsize=13)
    ax.set_ylabel("Rows and columns in the forbidden pattern", fontsize=14,
                  color=MUTED, labelpad=17)
    ax.grid(axis="y", color="#E1E4E1", linewidth=1.05)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#BFC5BF")
        ax.spines[side].set_linewidth(1)

    # Each horizontal segment retains the current pattern until the next
    # categorical refinement; the three candidate improvements form one path.
    ax.plot([0, 1], [66, 66], color=BASELINE, linewidth=3.2)
    ax.plot([1, 1, 2, 2, 3], [66, 15, 15, 5, 5],
            color=EARLIER, linewidth=3.2, solid_capstyle="round")
    ax.plot([3, 3, 3.36], [5, 4, 4],
            color=CURRENT, linewidth=3.6, solid_capstyle="round")

    for x, (size, color) in enumerate(zip(SIZES, (BASELINE, EARLIER, EARLIER, CURRENT))):
        ax.scatter(x, size, s=135, facecolor=color, edgecolor="white",
                   linewidth=2.7, zorder=4)
        ax.annotate(f"{size}×{size}", xy=(x, size), xytext=(11, 15),
                    textcoords="offset points", fontsize=21,
                    fontweight="bold" if x == 3 else "normal",
                    color=color, ha="left", va="bottom")

    ax.legend(handles=[
        Line2D([0], [0], color=BASELINE, lw=3, label="OpenAI construction"),
        Line2D([0], [0], color=EARLIER, lw=3, label="Earlier candidate refinements"),
        Line2D([0], [0], color=CURRENT, lw=3, label="Current 4×4 candidate"),
    ], loc="upper right", bbox_to_anchor=(1, 0.985), frameon=False,
        fontsize=13, labelcolor=MUTED, handlelength=2, labelspacing=0.7)

    fig.text(0.087, 0.142,
             "Refinement order · stages equally spaced, not elapsed time",
             fontsize=11.5, color=MUTED)
    fig.text(0.06, 0.085,
             "Candidate refinements: proof drafts and exact checks; independent mathematical review pending.",
             fontsize=12, color=MUTED)
    fig.text(0.06, 0.05,
             "github.com/shea256/ordered-binary-matrix-removal  ·  OpenAI Problem #190",
             fontsize=11.5, color="#82898D")

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "pattern-size-history.png", dpi=150,
                metadata={"Software": "Matplotlib", "Title": "Ordered binary matrix removal: pattern-size refinements"})
    fig.savefig(OUT / "pattern-size-history.svg", metadata={
        "Date": None,
        "Title": "Ordered binary matrix removal: 66×66 to 4×4",
        "Description": "Fixed forbidden pattern side lengths 66, 15, 5, and 4 in refinement order. Candidate refinements await independent review.",
    })
    plt.close(fig)
    print("Wrote assets/pattern-size-history.png and .svg")


if __name__ == "__main__":
    main()
