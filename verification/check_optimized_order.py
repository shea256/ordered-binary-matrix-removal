#!/usr/bin/env python3
"""Exact finite audit of the global minus-first order and the Erebos baseline.

Reuses the previously audited literal entry table, not its copy counter. The
column-quadruple/row-DP census below assumes neither localization nor a formula.
Finite evidence does not establish the all-depth theorem or optimal repair.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
import json
from math import prod

import check_four_literal as literal


def axes(h, axis, order="optimized", expanded=False):
    blocks = literal.axes(h, axis, expanded=expanded)

    def key(x):
        if x.kind != "anchor":
            return (1,)
        i, kind, sign, parity = x.mode
        if order == "optimized":
            family = 0 if kind == "W" and sign == "-" else 1 if kind == "W" else 2
            return (0, family, i, parity, sign, x.group)
        if order == "erebos":
            k = (("V", "+", -1), ("V", "-", -1), ("W", "+", 0),
                 ("W", "+", 1), ("W", "-", 0), ("W", "-", 1)).index((kind, sign, parity))
            return (0, i, k, x.group)
        if order == "previous":
            return (0, i, literal.TYPES.index((kind, sign, parity)), x.group)
        if order == "within_depth_minus_first":
            k = (("W", "-", 0), ("W", "-", 1), ("W", "+", 0),
                 ("W", "+", 1), ("V", "+", -1), ("V", "-", -1)).index((kind, sign, parity))
            return (0, i, k, x.group)
        if isinstance(order, tuple):
            return (0, i, order.index((kind, sign, parity)), x.group)
        raise ValueError(order)

    return sorted(blocks, key=key)


def repaired_entry(r, c, h):
    """Erebos terminal-anchor repair, applied to our reordered physical host."""
    if r.kind != "anchor" and c.kind == "anchor":
        i, kind, sign, parity = c.mode
        if (i, kind, sign, c.group) == (h, "W", "-", 0):
            return 0
    return literal.entry(r, c)


def census(h, order="optimized", repaired=False, expanded=False):
    rows, cols = axes(h, "row", order, expanded), axes(h, "column", order, expanded)
    entry = (lambda r, c: repaired_entry(r, c, h)) if repaired else literal.entry
    all_rows = (1 << len(rows)) - 1
    masks = [sum(entry(r, c) << i for i, r in enumerate(rows)) for c in cols]
    total = 0
    classes = Counter()
    escaped = 0
    for js in combinations(range(len(cols)), 4):
        candidates = []
        for signature in literal.H:
            mask = all_rows
            for j, bit in zip(js, signature):
                mask &= masks[j] if bit else all_rows ^ masks[j]
            if not mask:
                break
            candidates.append(mask)
        if len(candidates) != 4:
            continue
        ways = [1, 0, 0, 0, 0]
        outside = [1, 0, 0, 0, 0]
        for i, r in enumerate(rows):
            for k in range(3, -1, -1):
                if candidates[k] & (1 << i):
                    ways[k + 1] += ways[k] * r.weight
                    if k != 2 or not literal.target(r, cols[js[3]], h):
                        outside[k + 1] += outside[k] * r.weight
        weight = prod(cols[j].weight for j in js)
        total += ways[4] * weight
        escaped += outside[4] * weight
        classes[str(sum(cols[j].kind == "anchor" for j in js))] += ways[4] * weight
    edits = sum(r.weight * c.weight for r in rows for c in cols
                if entry(r, c) != literal.entry(r, c))
    return {"depth": h, "order": order, "expanded": expanded, "repaired": repaired,
            "n": sum(r.weight for r in rows), "copies": total,
            "anchor_column_counts": {k: v for k, v in sorted(classes.items()) if v},
            "copies_outside_zero_set": escaped, "edits": edits}


def intrinsic_count(h):
    """Enumerate the two order-independent families by actual leaf indices."""
    m = 2**h
    balanced = sum(2 * m**5 for p in range(m))
    unbalanced = sum(2 * m**4 for p in range(m) for q in range(p) if q % 2 == p % 2)
    return balanced, unbalanced


def main():
    records = []
    for order in ("erebos", "previous", "within_depth_minus_first", "optimized"):
        for h in range(1, 5):
            r = census(h, order)
            m = 2**h
            expected = {
                "erebos": 128 if h == 1 else (41*m**6 - 74*m**5)//4,
                "previous": 128 if h == 1 else (33*m**6 - 58*m**5)//4,
                "within_depth_minus_first": 128 if h == 1 else (7*m**6)//2 - 5*m**5,
                "optimized": (5*m**6)//2 - m**5,
            }[order]
            assert r["copies"] == expected, r
            assert r["copies_outside_zero_set"] == 0, r
            records.append(r)
    repairs = [census(h, repaired=True) for h in range(1, 5)]
    expanded = [census(1, expanded=True), census(1, repaired=True, expanded=True)]
    assert expanded[0]["copies"] == 128
    for r in repairs + expanded[1:]:
        assert r["copies"] == 0 and r["edits"] == 4**r["depth"], r
    intrinsic = []
    for h in range(1, 11):
        b, u = intrinsic_count(h)
        m = 2**h
        assert b + u == (5*m**6)//2 - m**5
        intrinsic.append({"depth": h, "balanced": b, "unbalanced": u})
    # This finite search concerns depth-preserving permutations only. It does
    # not prove the all-depth optimum over arbitrary whole-mode permutations.
    small_search = []
    for order in permutations(literal.TYPES[:4]):
        mode_order = order + literal.TYPES[4:]
        r = census(2, mode_order)
        assert r["copies"] >= 9216
        small_search.append({"order": mode_order, "copies": r["copies"],
                             "outside_zero_set": r["copies_outside_zero_set"]})
    ratio = Fraction(10, 41)
    return {"pattern": literal.H, "scope": "Exact finite evidence, not an all-depth certificate or peer review.",
            "comparison_censuses": records, "terminal_anchor_repairs": repairs,
            "expanded_depth_one": expanded, "intrinsic_counts": intrinsic,
            "depth_two_24_orders": small_search,
            "limiting_copy_ratio_to_erebos": str(ratio),
            "limiting_fraction_fewer": str(1-ratio)}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
