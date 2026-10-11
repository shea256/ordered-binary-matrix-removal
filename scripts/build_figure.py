#!/usr/bin/env python3
"""Render dated GitHub milestones with optional Matplotlib 3.9.4.

The horizontal axis is proportional UTC time; vertical counts use log10.
Source records distinguish commit dates, release publication, and PR opening.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
COLORS = {"openai-66": "#555555", "proveit-5": "#BE862D",
          "erebos-4": "#8061AD", "project-3x4": "#129B78"}
EARLIER = "#2C7FCC"
INK = "#171A1C"
MUTED = "#646B70"


def utc(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main():
    status = json.loads((ROOT / "results/current.json").read_text())
    records = json.loads((OUT / "pattern-size-events.json").read_text())
    events = records["events"]
    by_id = {event["id"]: event for event in events}
    assert by_id["project-3x4"]["shape"] == [status["pattern_rows"], status["pattern_columns"]]
    assert by_id["erebos-4"]["shape"] == [status["baseline_pattern_rows"], status["baseline_pattern_columns"]]
    assert status["status"] == "candidate" and status["new_result_formalized"]
    times = [utc(e["timestamp"]) for e in events]
    assert times == sorted(times)
    for event in events:
        event["x"] = mdates.date2num(utc(event["timestamp"]))
        event["entries"] = event["shape"][0] * event["shape"][1]
    milestones = [event for event in events if event["series"] == "milestone"]
    assert all(a["entries"] > b["entries"] for a,b in zip(milestones,milestones[1:]))
    title = "Ordered binary matrix removal: 66×66 → 3×4"
    y_ticks = [10, 100, 1000, 10000]
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 14,
        "axes.unicode_minus": False, "svg.fonttype": "path",
        "svg.hashsalt": "ordered-binary-matrix-removal-dated-history",
    })
    fig = plt.figure(figsize=(18, 11), facecolor="white")
    ax = fig.add_axes([0.095, 0.29, 0.86, 0.465])
    fig.text(0.06, 0.943, title, fontsize=26, color=INK)
    fig.text(0.06, 0.898,
             "GitHub record dates · proportional time axis (UTC) · logarithmic entry counts",
             fontsize=15, color=MUTED)
    fig.legend(handles=[
        Line2D([0], [0], color=COLORS["openai-66"], lw=3, label="OpenAI"),
        Line2D([0], [0], color=COLORS["proveit-5"], lw=3, label="ProveIt"),
        Line2D([0], [0], color=COLORS["erebos-4"], lw=3, label="Erebos Labs"),
        Line2D([0], [0], color=COLORS["project-3x4"], lw=3, label="This work: 3×4"),
        Line2D([0], [0], color=EARLIER, marker="o", markerfacecolor="white",
               markeredgewidth=2, linestyle="none", label="Our earlier stages"),
    ], loc="upper left", bbox_to_anchor=(0.055, 0.853), frameon=False,
        ncol=5, fontsize=13, labelcolor=MUTED, handlelength=1.8, columnspacing=2)

    ax.set_xlim(utc("2026-10-06T00:00:00Z"), utc("2026-10-12T18:00:00Z"))
    ax.set_yscale("log")
    ax.set_ylim(8, 10000)
    ax.yaxis.set_major_locator(FixedLocator(y_ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_locator(mdates.DayLocator(tz=timezone.utc))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("Oct %d", tz=timezone.utc))
    ax.tick_params(axis="both", which="both", length=0, pad=11, labelcolor=MUTED)
    ax.set_ylabel("Entries in the forbidden pattern · log₁₀ scale", fontsize=14,
                  color=MUTED, labelpad=16)
    ax.set_xlabel("GitHub record date · October 2026 · UTC", fontsize=12, color=MUTED, labelpad=13)
    ax.grid(axis="y", color="#E1E4E1", linewidth=1.05)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#BFC5BF")

    for a,b in zip(milestones,milestones[1:]):
        ax.plot([a["x"],b["x"]], [a["entries"],a["entries"]], color=COLORS[a["id"]], lw=3)
        ax.plot([b["x"],b["x"]], [a["entries"],b["entries"]], color=COLORS[b["id"]], lw=3)
    last = milestones[-1]
    ax.plot([last["x"],mdates.date2num(utc("2026-10-12T12:00:00Z"))],
            [last["entries"],last["entries"]], color=COLORS[last["id"]], lw=3)
    for event in events:
        stage = event["series"] == "project_stage"
        color = EARLIER if stage else COLORS[event["id"]]
        ax.scatter(event["x"], event["entries"], s=110,
                   facecolor="white" if stage else color,
                   edgecolor=color if stage else "white", linewidth=2.5, zorder=5)

    # Labels use leaders where several October 10 stages fall close together.
    labels = {
        "openai-66": (12, 13, "66×66 · OpenAI\nOct 6 commit", 17),
        "proveit-5": (-155, 34, "5×5 · ProveIt\nOct 7 commit", 16),
        "erebos-4": (-106, 66, "4×4 · Erebos Labs\nOct 9 release", 16),
        "project-15": (-53, 16, "Our 15×15\nOct 10 commit", 13),
        "project-5": (-83, 40, "Our 5×5", 12),
        "project-4": (8, 27, "Our 4×4", 12),
        "project-3x4": (12, 14, "3×4 · This work\nOct 11 PR", 17),
    }
    for event in events:
        dx,dy,label,size = labels[event["id"]]
        color = EARLIER if event["series"] == "project_stage" else COLORS[event["id"]]
        ax.annotate(label, xy=(event["x"],event["entries"]), xytext=(dx,dy),
                    textcoords="offset points", fontsize=size, color=color, va="bottom",
                    fontweight="bold" if event["id"] == "project-3x4" else "normal",
                    arrowprops={"arrowstyle":"-", "color":color, "lw":0.8,
                                "shrinkA":5,"shrinkB":7} if dy>25 else None)
    ax.text(0.52, 0.86, "4×4 → 3×4", transform=ax.transAxes, fontsize=26,
            fontweight="bold", color=COLORS["project-3x4"])
    ax.text(0.52, 0.76, "16 → 12 entries · 25% fewer", transform=ax.transAxes,
            fontsize=18, color=INK)
    ax.text(0.52, 0.63, "The 3×4 theorem is verified in Lean", transform=ax.transAxes,
            fontsize=14, color=MUTED)

    fig.text(0.06, 0.188,
             "Erebos Labs 4×4: GitHub v1.0.0 released October 9, 2026 at 12:40:51 UTC.",
             fontsize=13, color=COLORS["erebos-4"])
    fig.text(0.06, 0.149,
             "Line: minimum entries among shown results. Hollow dots: our later intermediate constructions.",
             fontsize=11.5, color=MUTED)
    fig.text(0.06, 0.113,
             "Commit dates are repository metadata. OpenAI’s manuscript is dated Sep 25; its plotted commit is Oct 6.",
             fontsize=11.5, color=MUTED)
    fig.text(0.06, 0.077,
             "Hosts can be arbitrarily large. Independent mathematical review pending; sources and timestamp types in assets/README.md.",
             fontsize=11.5, color=MUTED)
    fig.text(0.06, 0.041,
             "github.com/shea256/ordered-binary-matrix-removal  ·  OpenAI Problem #190",
             fontsize=11.5, color="#82898D")
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "pattern-size-history.png", dpi=150,
                metadata={"Software":"Matplotlib", "Title":title})
    fig.savefig(OUT / "pattern-size-history.svg", metadata={
        "Date":None, "Title":title,
        "Description":"Proportional UTC timeline of selected GitHub records, with logarithmic pattern-entry counts. OpenAI 66×66: October 6 commit (manuscript dated September 25); ProveIt 5×5: October 7 commit; Erebos Labs 4×4: v1.0.0 release on October 9 at 12:40:51 UTC; this work 3×4: October 11 PR. Hollow points mark later project stages of 15×15, 5×5 and 4×4 on October 10. These are documented record dates, not asserted discovery or first-publication dates.",
    })
    svg = OUT / "pattern-size-history.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)
    receipt = {
        "current_result_id":status["result_id"],
        "event_ids":[e["id"] for e in events],
        "pattern_shapes":[e["shape"] for e in events],
        "entries":[e["entries"] for e in events],
        "timestamps":[e["timestamp"] for e in events],
        "y_scale":"logarithmic", "y_ticks":y_ticks,
        "x_scale":"linear UTC time", "x_order":"documented GitHub record timestamps",
        "current_theorem_formalized":status["new_result_formalized"],
        "matplotlib":matplotlib.__version__,
        "artifacts":{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
            "scripts/build_figure.py", "assets/pattern-size-events.json",
            "assets/pattern-size-history.png", "assets/pattern-size-history.svg")},
    }
    (OUT / "pattern-size-history.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("Wrote dated PNG, SVG and source/data receipt in assets/.")


if __name__ == "__main__":
    main()
