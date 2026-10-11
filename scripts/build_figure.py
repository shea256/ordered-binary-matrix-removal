#!/usr/bin/env python3
"""Render selected pattern sizes with optional Matplotlib 3.9.4.

Sources: BASELINE.md, IMPROVEMENTS.md, and results/current.json.
The x-axis orders selected constructions by size, not publication date.
The logarithmic y-axis counts specified binary entries (rows times columns).
"""
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
BASELINE = "#555555"
EARLIER = "#2C7FCC"
PRIOR = "#8061AD"
CURRENT = "#129B78"
INK = "#171A1C"
MUTED = "#646B70"


def main():
    status = json.loads((ROOT / "results/current.json").read_text())
    current_shape = (status["pattern_rows"], status["pattern_columns"])
    prior_shape = (status["baseline_pattern_rows"], status["baseline_pattern_columns"])
    assert current_shape == (3, 4) and prior_shape == (4, 4)
    assert status["status"] == "candidate" and status["new_result_formalized"]
    shapes = [(66, 66), (15, 15), (5, 5), prior_shape, current_shape]
    entries = [rows * columns for rows, columns in shapes]
    stages = ["OpenAI\nbaseline", "Earlier project\nstage", "Earlier project\nstage",
              "Known 4×4\nErebos", "Current 3×4\nresult"]
    colors = [BASELINE, EARLIER, EARLIER, PRIOR, CURRENT]
    title = "Ordered binary matrix removal: 66×66 → 3×4"

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 14,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
        "svg.hashsalt": "ordered-binary-matrix-removal-size-history",
    })
    fig = plt.figure(figsize=(16, 10), facecolor="white")
    ax = fig.add_axes([0.10, 0.265, 0.855, 0.48])
    fig.text(0.06, 0.94, title, fontsize=25, color=INK)
    fig.text(0.06, 0.891,
             "Smaller fixed forbidden patterns. The host matrices can be arbitrarily large.",
             fontsize=15, color=MUTED)
    fig.legend(handles=[
        Line2D([0], [0], color=BASELINE, lw=3, label="OpenAI construction"),
        Line2D([0], [0], color=EARLIER, lw=3, label="Earlier project stages"),
        Line2D([0], [0], color=PRIOR, lw=3, label="Prior 4×4 result"),
        Line2D([0], [0], color=CURRENT, lw=3, label="Current 3×4 result"),
    ], loc="upper left", bbox_to_anchor=(0.06, 0.847), frameon=False,
        ncol=4, fontsize=12.5, labelcolor=MUTED, handlelength=1.8, columnspacing=1.8)

    ax.set_xlim(-0.18, 4.52)
    ax.set_yscale("log")
    ax.set_ylim(8, 10000)
    ax.yaxis.set_major_locator(FixedLocator([12, 25, 100, 225, 1000, 4356]))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.set_xticks(range(len(shapes)), stages)
    ax.tick_params(axis="both", which="both", length=0, pad=10, labelcolor=MUTED)
    ax.tick_params(axis="x", labelsize=13)
    ax.set_ylabel("Entries in the forbidden pattern · log scale", fontsize=14,
                  color=MUTED, labelpad=16)
    ax.grid(axis="y", color="#E1E4E1", linewidth=1.05)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#BFC5BF")
        ax.spines[side].set_linewidth(1)

    for x in range(len(shapes) - 1):
        ax.plot([x, x + 1], [entries[x], entries[x]], color=colors[x], lw=3)
        ax.plot([x + 1, x + 1], [entries[x], entries[x + 1]], color=colors[x + 1], lw=3)
    ax.plot([4, 4.36], [entries[-1], entries[-1]], color=CURRENT, lw=3.5)
    for x, ((rows, columns), count, color) in enumerate(zip(shapes, entries, colors)):
        ax.scatter(x, count, s=120, facecolor=color, edgecolor="white", linewidth=2.5, zorder=4)
        ax.annotate(f"{rows}×{columns}", xy=(x, count), xytext=(10, 16),
                    textcoords="offset points", fontsize=21, color=color,
                    fontweight="bold" if x == 4 else "normal", ha="left", va="bottom")
        ax.annotate(f"{count:,} entries", xy=(x, count), xytext=(11, 1),
                    textcoords="offset points", fontsize=11.5, color=MUTED,
                    ha="left", va="bottom")

    ax.text(0.58, 0.71, "4×4 → 3×4", transform=ax.transAxes,
            fontsize=25, fontweight="bold", color=CURRENT)
    ax.text(0.58, 0.61, "25% fewer specified entries", transform=ax.transAxes,
            fontsize=17, color=INK)
    ax.text(0.58, 0.51, "3×4 removal theorem verified in Lean", transform=ax.transAxes,
            fontsize=14, color=MUTED)

    fig.text(0.10, 0.177,
             "Selected constructions ordered by size · equally spaced stages, not a publication timeline",
             fontsize=11.5, color=MUTED)
    fig.text(0.06, 0.118,
             "Prior work: Erebos — earlier 4×4 theorem; ProveIt — earlier 5×5 work and the H4 candidate.",
             fontsize=12, color=MUTED)
    fig.text(0.06, 0.080,
             "Current result: main theorem checked in Lean; independent mathematical review pending.",
             fontsize=12, color=MUTED)
    fig.text(0.06, 0.043,
             "github.com/shea256/ordered-binary-matrix-removal  ·  OpenAI Problem #190",
             fontsize=11.5, color="#82898D")

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "pattern-size-history.png", dpi=150,
                metadata={"Software": "Matplotlib", "Title": title})
    fig.savefig(OUT / "pattern-size-history.svg", metadata={
        "Date": None, "Title": title,
        "Description": "Selected patterns 66×66, 15×15, 5×5, 4×4, 3×4 have 4356, 225, 25, 16, 12 entries. Logarithmic vertical scale; categorical size order, not publication dates. Erebos has the earlier 4×4 theorem; ProveIt has earlier 5×5 work and the H4 candidate. The current 3×4 main theorem is Lean checked; independent review remains pending.",
    })
    svg = OUT / "pattern-size-history.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)
    receipt = {
        "current_result_id": status["result_id"],
        "pattern_shapes": shapes,
        "entries": entries,
        "y_scale": "logarithmic",
        "x_order": "selected constructions ordered by size, not publication date",
        "current_theorem_formalized": status["new_result_formalized"],
        "matplotlib": matplotlib.__version__,
        "artifacts": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                      for name in ("scripts/build_figure.py", "assets/pattern-size-history.png",
                                   "assets/pattern-size-history.svg")},
    }
    (OUT / "pattern-size-history.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print("Wrote PNG, SVG and source/data receipt in assets/.")


if __name__ == "__main__":
    main()
