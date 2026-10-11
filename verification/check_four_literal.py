#!/usr/bin/env python3
"""Fresh literal reconstruction for the 4x4 audit; no research-code imports.

Coordinates are built by sorting tree-interval endpoints, not by the original
recursive traversal. Copies are counted by an ordered-column dynamic program.
The expanded depth-one matrix includes every actual position separately.
This is exact finite evidence, not a universal theorem or peer review.
"""
from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
import json
from math import prod

H = ((0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 1))
TYPES = (("W", "+", 0), ("W", "+", 1), ("W", "-", 0),
         ("W", "-", 1), ("V", "+", -1), ("V", "-", -1))


@dataclass(frozen=True)
class Block:
    kind: str
    depth: int = -1
    sign: str = ""
    node: int = -1
    mode: tuple = ()
    group: int = -1
    weight: int = 1


def axes(h, name, expanded=False, reverse_minus=False):
    m = 2**h
    kinds = list(TYPES)
    if reverse_minus:
        kinds[2], kinds[3] = kinds[3], kinds[2]
    anchors = [Block("anchor", mode=(i, k, s, d), group=g, weight=m)
               for i in range(1, h+1) for k, s, d in kinds for g in (0, 1)]
    variables = [Block("variable", i, sign, p, weight=2**(h-i))
                 for i in range(h+1) for sign in (("L",) if i == h else ("+", "-"))
                 for p in range(2**i)]

    def interval_key(x):
        width = 2**(h-x.depth)
        if x.sign == "L":
            return (2*x.node+1, 0, 0)
        before = x.sign == ("-" if name == "row" else "+")
        return ((2*x.node*width, 1, x.depth) if before else
                (2*(x.node+1)*width, 0, -x.depth))

    variables.sort(key=interval_key)
    dummy = [Block("dummy", weight=m)]
    result = anchors + (variables+dummy if name == "row" else dummy+variables)
    assert sum(x.weight for x in result) == (14*h+2)*m
    if expanded:
        return [Block(x.kind, x.depth, x.sign, x.node, x.mode, x.group)
                for x in result for _ in range(x.weight)]
    return result


def in_role(x, mode, name, j):
    i, kind, sign, parity = mode
    if x.kind == "dummy":
        return (kind, name, j) in (("W", "row", 1), ("V", "column", 0))
    if x.kind != "variable":
        return False
    same_sign = x.sign in (sign, "L")
    if kind == "V":
        level = i-1 if name == "column" else i if (sign == "+") == (j == 0) else i-1
        return same_sign and x.depth == level and (name != "column" or j == 1)
    child = name == "row" or (j == 1) == (sign == "+")
    if name == "row" and j != 0:
        return False
    return (same_sign and x.depth == (i if child else i-1)
            and (not child or x.node % 2 == parity))


def entry(r, c):
    if r.kind == c.kind == "anchor":
        return int(r.mode == c.mode and r.group != c.group)
    if r.kind == "anchor":
        return int(in_role(c, r.mode, "column", r.group))
    if c.kind == "anchor":
        return int(in_role(r, c.mode, "row", c.group))
    if r.kind == "dummy" or c.kind == "dummy":
        return 1
    i, j, p, q = r.depth, c.depth, r.node, c.node
    predicates = (
        i == j and r.sign in ("+", "L") and c.sign in ("+", "L") and p <= q,
        i == j and r.sign == c.sign == "-" and p < q,
        i == j+1 and r.sign in ("+", "L") and c.sign == "+" and p//2 <= q,
        i == j+1 and r.sign in ("-", "L") and c.sign == "-" and p//2 < q,
    )
    return int(any(predicates))


def target(r, c, h):
    return (r.kind == c.kind == "variable" and r.depth == h
            and c.depth == h-1 and c.sign == "-" and c.node == r.node//2)


def count_columns(candidates, cols):
    ways = [1, 0, 0, 0, 0]
    for j, c in enumerate(cols):
        for k in range(3, -1, -1):
            if candidates[k] & (1 << j):
                ways[k+1] += ways[k]*c.weight
    return ways[4]


def census(h, expanded=False, reverse_minus=False, flip_target=False):
    rows = axes(h, "row", expanded, reverse_minus)
    cols = axes(h, "column", expanded, reverse_minus)
    full = (1 << len(cols))-1
    masks = [sum((1 if flip_target and target(r, c, h) else entry(r, c)) << j
                 for j, c in enumerate(cols)) for r in rows]
    anchor_mask = sum(1 << j for j, c in enumerate(cols) if c.kind == "anchor")
    classes = Counter()
    violations = wrong_last_row = choices = total = 0
    for ix in combinations(range(len(rows)), 4):
        choices += 1
        candidates = []
        for signature in zip(*H):
            mask = full
            for i, bit in zip(ix, signature):
                mask &= masks[i] if bit else full ^ masks[i]
            if not mask:
                break
            candidates.append(mask)
        if len(candidates) != 4:
            continue
        R = [rows[i] for i in ix]
        weight = prod(r.weight for r in R)
        count = count_columns(candidates, cols)*weight
        if not count:
            continue
        total += count
        a = sum(r.kind == "anchor" for r in R)
        for b in range(5):
            restricted = [mask & (anchor_mask if k < b else full ^ anchor_mask)
                          for k, mask in enumerate(candidates)]
            if all(restricted):
                classes[f"{a},{b}"] += count_columns(restricted, cols)*weight
        allowed = sum(1 << j for j, c in enumerate(cols) if target(R[2], c, h))
        forbidden = candidates[:3] + [candidates[3] & (full ^ allowed)]
        violations += count_columns(forbidden, cols)*weight
        if R[3].kind != "dummy":
            wrong_last_row += count
    assert sum(classes.values()) == total
    return {"depth": h, "expanded": expanded, "axis_blocks": len(rows),
            "row_choices": choices, "copies": total,
            "anchor_configurations": dict(sorted(classes.items())),
            "copies_outside_zero_set": violations, "copies_without_dummy_last_row": wrong_last_row}


def three_seed_guards(h):
    """All protected-cell frequencies under a compact common-seed sampler."""
    m = 2**h
    row_blocks, col_blocks = axes(h, "row"), axes(h, "column")

    def selected(blocks, z, u):
        result = []
        for index, x in enumerate(blocks):
            if x.kind != "variable" or x.node == z//x.weight:
                result.append((index, u % x.weight))
        return result

    counts = Counter()
    leaf_counts = Counter()
    for z, u, v in product(range(m), repeat=3):
        rs = selected(row_blocks, z, u)
        cs = selected(col_blocks, z, v)
        for (ri, ro), (ci, co) in product(rs, cs):
            r, c = row_blocks[ri], col_blocks[ci]
            protected = (r.kind in ("anchor", "dummy") or c.kind in ("anchor", "dummy")
                         or (r.depth == c.depth == 0 and r.kind == c.kind == "variable"))
            if protected:
                counts[(ri, ro, ci, co)] += 1
            if r.kind == c.kind == "variable" and r.depth == c.depth == h:
                assert r.node == c.node
                leaf_counts[r.node] += 1
    # Also verify every protected actual cell is represented, not just cells
    # visited by the sampler.
    expected = sum(r.weight*c.weight for r, c in product(row_blocks, col_blocks)
                   if r.kind in ("anchor", "dummy") or c.kind in ("anchor", "dummy")
                   or (r.depth == c.depth == 0 and r.kind == c.kind == "variable"))
    assert len(counts) == expected and set(counts.values()) == {m}
    assert len(leaf_counts) == m and set(leaf_counts.values()) == {m*m}
    return {"depth": h, "samples": m**3, "protected_actual_cells": expected,
            "frequency_of_each_protected_cell": m, "diagonal_leaf_frequency": m*m}


def main():
    tests = [census(h) for h in range(1, 5)] + [census(1, expanded=True)]
    for item in tests:
        h, m = item["depth"], 2**item["depth"]
        expected = 128 if h == 1 else (33*m**6-58*m**5)//4
        assert item["copies"] == expected
        assert item["copies_outside_zero_set"] == item["copies_without_dummy_last_row"] == 0
        assert set(item["anchor_configurations"]) <= {"2,1", "2,2"}
    bad_order = census(3, reverse_minus=True)
    bad_repair = census(1, expanded=True, flip_target=True)
    assert bad_order["copies_outside_zero_set"] > 0
    assert bad_repair["copies_outside_zero_set"] > 0
    assert bad_repair["copies_without_dummy_last_row"] > 0
    return {"literal_censuses": tests,
            "three_seed_guard_frequencies": [three_seed_guards(h) for h in range(1, 4)],
            "negative_controls": {"reversed_minus_order": bad_order, "flip_original_zero_set": bad_repair},
            "scope": "Separate literal implementation and exact finite audit; no universal theorem or independent peer review."}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
