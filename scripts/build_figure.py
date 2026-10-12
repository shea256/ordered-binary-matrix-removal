#!/usr/bin/env python3
"""Render dated GitHub milestones with optional Matplotlib 3.9.4.

The horizontal axis is proportional UTC time; vertical counts use log10.
Source records distinguish commit dates, release publication, and PR opening.
"""
from datetime import datetime, timedelta, timezone
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
          "erebos-4": "#8061AD", "wang-4": "#956144",
          "project-3x4": "#568878", "project-3x3": "#129B78"}
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
    assert by_id["project-3x3"]["shape"] == [status["pattern_rows"], status["pattern_columns"]]
    assert by_id["erebos-4"]["shape"] == [status["baseline_pattern_rows"], status["baseline_pattern_columns"]]
    assert status["status"] == "candidate" and status["new_result_formalized"]
    times = [utc(e["timestamp"]) for e in events]
    assert times == sorted(times)
    for event in events:
        event["x"] = mdates.date2num(utc(event["timestamp"]))
        event["entries"] = event["shape"][0] * event["shape"][1]
    milestones = [event for event in events if event["series"] == "milestone"]
    assert all(a["entries"] > b["entries"] for a,b in zip(milestones,milestones[1:]))
    title = "Ordered binary matrix removal"
    y_ticks = [10, 100, 1000, 10000]
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 14,
        "axes.unicode_minus": False, "svg.fonttype": "path",
        "svg.hashsalt": "ordered-binary-matrix-removal-dated-history",
    })
    fig = plt.figure(figsize=(18, 9.6), facecolor="white")
    ax = fig.add_axes([0.095, 0.235, 0.86, 0.58])
    fig.text(0.06, 0.943, title, fontsize=28, color=INK)
    fig.text(0.06, 0.893, "OpenAI Problem #190", fontsize=15, color=MUTED)
    fig.legend(handles=[
        Line2D([0], [0], color=MUTED, lw=3, marker="o",
               label="Smallest pattern shown"),
        Line2D([0], [0], color=MUTED, marker="o", markerfacecolor="white",
               markeredgewidth=2, linestyle="none", label="Other constructions"),
    ], loc="upper right", bbox_to_anchor=(0.955, 0.916), frameon=False,
        ncol=2, fontsize=13, labelcolor=MUTED, handlelength=1.8, columnspacing=2)

    last_time = utc(events[-1]["timestamp"])
    ax.set_xlim(utc("2026-10-06T00:00:00Z"), last_time + timedelta(days=1.4))
    ax.set_yscale("log")
    ax.set_ylim(6, 10000)
    ax.yaxis.set_major_locator(FixedLocator(y_ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_locator(mdates.DayLocator(tz=timezone.utc))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("Oct %d", tz=timezone.utc))
    ax.tick_params(axis="both", which="both", length=0, pad=11, labelcolor=MUTED)
    ax.set_ylabel("Entries in forbidden pattern (log scale)", fontsize=14,
                  color=MUTED, labelpad=16)
    ax.set_xlabel("GitHub record date · October 2026 (UTC)", fontsize=12, color=MUTED, labelpad=13)
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
    ax.plot([last["x"],mdates.date2num(last_time + timedelta(days=0.9))],
            [last["entries"],last["entries"]], color=COLORS[last["id"]], lw=3)
    for event in events:
        stage = event["series"] != "milestone"
        color = EARLIER if event["series"] == "project_stage" else COLORS[event["id"]]
        ax.scatter(event["x"], event["entries"], s=110,
                   facecolor="white" if stage else color,
                   edgecolor=color if stage else "white", linewidth=2.5, zorder=5)

    # Every point uses the same source-and-size label; the axes carry the dates
    # and entry counts. Leaders separate the closely spaced later records.
    offsets = {
        "openai-66": (12, 14),
        "proveit-5": (-135, 26),
        "erebos-4": (-140, 44),
        "project-15": (-55, 16),
        "project-5": (-102, 26),
        "project-4": (8, 48),
        "wang-4": (-32, 100),
        "project-3x4": (10, 62),
        "project-3x3": (12, 15),
    }
    point_labels = []
    for event in events:
        dx,dy = offsets[event["id"]]
        source = "This work" if event["owner"] == "This project" else event["owner"]
        rows,columns = event["shape"]
        label = f"{source} · {rows}×{columns}"
        point_labels.append(label)
        color = EARLIER if event["series"] == "project_stage" else COLORS[event["id"]]
        ax.annotate(label, xy=(event["x"],event["entries"]), xytext=(dx,dy),
                    textcoords="offset points", fontsize=14, color=color, va="bottom",
                    arrowprops={"arrowstyle":"-", "color":color, "lw":0.8,
                                "shrinkA":5,"shrinkB":7} if dy>25 else None)

    fig.text(0.06, 0.092,
             "Arbitrarily large hosts · 3×3 theorem verified in Lean · Independent mathematical review pending",
             fontsize=12, color=MUTED)
    fig.text(0.06, 0.046,
             "github.com/shea256/ordered-binary-matrix-removal",
             fontsize=12, color="#82898D")
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "pattern-size-history.png", dpi=150,
                metadata={"Software":"Matplotlib", "Title":title})
    fig.savefig(OUT / "pattern-size-history.svg", metadata={
        "Date":None, "Title":title,
        "Description":"Proportional UTC timeline of selected GitHub records, with logarithmic pattern-entry counts. OpenAI 66×66: October 6 commit (paper dated September 25); ProveIt 5×5: October 7 commit; Erebos Labs 4×4: October 9 release; Wang 4×4: October 11 commit; this project 3×4: October 11 PR; this work 3×3: October 12 commit. Hollow points mark later constructions. These are record dates, not asserted discovery or first-publication dates.",
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
        "point_labels":point_labels,
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
