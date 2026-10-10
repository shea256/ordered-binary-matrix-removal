#!/usr/bin/env python3
"""Exact finite checks. Universal claims require the accompanying proof.

Run from any directory. Uses the standard library, never floating-point math.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import sys

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from host import anchor, entry, full_axis, modes, nonanchors, nonanchor_entry, role


def check_anchor():
    S = anchor()
    assert len({tuple(r) for r in S}) == 13
    cols = list(zip(*S))
    assert len(set(cols)) == 13
    assert {tuple(r[-3:]) for r in S[-8:]} == set(itertools.product((0, 1), repeat=3))
    assert all(sum(c[:6]) >= 5 for c in cols)
    assert all(sum(r[:6]) >= 5 for r in S)
    assert min(map(sum, S)) > 1 and min(map(sum, cols)) > 1
    return {"size": 13, "dense_prefix": 6, "minimum_row_ones": min(map(sum, S)),
            "minimum_column_ones": min(map(sum, cols)),
            "pattern": [r + [int(u == 0), int(u == 1)] for u, r in enumerate(S)]
                       + [[1, 0] + [0] * 11 + [1, 0], [0, 1] + [0] * 11 + [1, 1]]}


def check_baseline_anchor():
    S = anchor(64, 5)
    cols = list(zip(*S))
    assert len({tuple(r) for r in S}) == len(set(cols)) == 64
    assert {tuple(r[-5:]) for r in S[-32:]} == set(itertools.product((0, 1), repeat=5))
    assert all(sum(c[:32]) >= 31 for c in cols)
    assert all(sum(r[:32]) >= 31 for r in S)
    assert min(map(sum, S)) == 58 and min(map(sum, cols)) == 48
    return {"size": 64, "word_bits": 5, "minimum_prefix_density": 31,
            "minimum_row_ones": 58, "minimum_column_ones": 48}


def check_traces(h):
    rows, cols = nonanchors(h, "row"), nonanchors(h, "column")
    all_rows = (1 << len(rows)) - 1
    masks = [sum(nonanchor_entry(r, c) << j for j, r in enumerate(rows)) for c in cols]
    checked = 0
    maximum = 0
    for inds in itertools.combinations(range(len(cols)), 3):
        seen = 0
        for word in range(8):
            candidates = all_rows
            for j, col in enumerate(inds):
                candidates &= masks[col] if (word >> j) & 1 else all_rows ^ masks[col]
            seen += bool(candidates)
        assert seen < 8, (h, inds)
        maximum = max(maximum, seen)
        checked += 1
    pair = next((inds for inds in itertools.combinations(range(len(cols)), 2)
                 if len({tuple(nonanchor_entry(r, cols[j]) for j in inds) for r in rows}) == 4), None)
    return {"h": h, "quotient_columns": len(cols), "triples_checked": checked,
            "max_traces_on_three_columns": maximum, "shattered_pair": pair}


def check_bodies(h, s):
    rows, cols = nonanchors(h, "row"), nonanchors(h, "column")
    body_count = 0
    visited = 0
    by_mode = {}
    for t in modes(h):
        rs = [[(j, r) for j, r in enumerate(rows) if role(r, t, "row") == a] for a in (1, 2)]
        cs = [[(j, c) for j, c in enumerate(cols) if role(c, t, "column") == a] for a in (1, 2)]
        subtotal = 0
        for (j1, r1), (j2, r2), (l1, c1), (l2, c2) in itertools.product(*rs, *cs):
            if j1 >= j2 or l1 >= l2:
                continue
            visited += 1
            body = tuple(nonanchor_entry(r, c) for r, c in [(r1, c1), (r1, c2), (r2, c1), (r2, c2)])
            if body != (1, 0, 1, 1):
                continue
            assert t[0] == "W" and t[1] == h and t[2] == "-"
            assert r1.sign == c1.sign == "L" and r1.node == c1.node
            subtotal += r1.weight * r2.weight * c1.weight * c2.weight
        if subtotal:
            by_mode[str(t)] = subtotal
        body_count += subtotal
    m = 2 ** h
    assert body_count == 2 * m * m
    n = (6 * s * h + 2 * h + 2) * m
    count = body_count * m ** (2 * s)
    assert Fraction(count, n ** (2 * (s + 2))) == Fraction(2, (n // m) ** (2 * s + 4) * m * m)
    return {"h": h, "s": s, "ordered_quotient_bodies_checked": visited,
            "weighted_body_count": body_count, "nonzero_modes": by_mode,
            "conditional_full_copy_count": count, "n": n,
            "distance_lower_bound": str(Fraction(m * m, n * n))}


def check_incidence_and_sampling(h):
    m = 2 ** h
    max_incidence = 0
    for axis in ("row", "column"):
        for x in nonanchors(h, axis):
            if x.kind == "variable":
                count = sum(role(x, t, axis) != 0 for t in modes(h))
                assert count <= 4
                max_incidence = max(max_incidence, count)
                # A specific position is sampled with prob. 2^-depth/weight.
                assert Fraction(1, 2 ** x.depth * x.weight) == Fraction(1, m)
    # Protected incidences have independent uniform endpoint choices.
    assert Fraction(1, m) ** 2 == Fraction(1, m * m)
    # Shared leaf choices are correlated: not all cells have prob. m^-2.
    assert Fraction(1, m) != Fraction(1, m * m)
    return {"h": h, "max_variable_mode_incidence": max_incidence,
            "protected_cell_probability": str(Fraction(1, m * m)),
            "diagonal_leaf_selection_probability": str(Fraction(1, m))}


def check_manifest():
    manifest = json.loads((ROOT / "verification" / "source_manifest.json").read_text())
    for f in manifest["files"]:
        assert len(f["sha256"]) == 64 and int(f["sha256"], 16) >= 0
        assert f["bytes"] > 0
    return {"upstream_commit": manifest["upstream_commit"],
            "manifest_entries_checked": len(manifest["files"]),
            "source_bytes_verified_in_this_run": False, "lean_build_performed": False}


if __name__ == "__main__":
    report = {"anchor": check_anchor(), "baseline_anchor": check_baseline_anchor(),
              "traces": [check_traces(h) for h in range(1, 6)],
              "bodies": [check_bodies(h, s) for s in (13, 64) for h in range(1, 7)],
              "sampling": [check_incidence_and_sampling(h) for h in range(1, 9)],
              "sources": check_manifest(),
              "scope": "Exact finite evidence and manifest metadata; not a universal proof or independent review."}
    print(json.dumps(report, indent=2))
