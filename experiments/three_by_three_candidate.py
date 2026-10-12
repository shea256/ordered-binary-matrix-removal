#!/usr/bin/env python3
"""Exact census for the 3x3 crown candidate. Not a universal proof or Lean.

Rows have prefix anchors; columns have suffix anchors. The new column
signature has an extra one on dummy rows for every vertical mode.
"""
import argparse
from collections import defaultdict
from itertools import combinations
import json
from math import prod
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
from host import Position, modes, nonanchors, nonanchor_entry, role

H = ((0, 1, 1), (1, 0, 1), (1, 1, 0))


def axis(h, name):
    ts = sorted(modes(h), key=lambda t: (
        0 if t[0] == 'W' and t[2] == '-' else 1 if t[0] == 'W' else 2,
        t[1], t[3], t[2]))
    anchors = [Position('anchor', mode=t, group=0, weight=2**h) for t in ts]
    body = nonanchors(h, name)
    return anchors + body if name == 'row' else body + anchors


def entry(r, c, omit_vertical_dummy=False, omit_horizontal_dummy=False, omit_odd=False):
    if r.kind == c.kind == 'anchor':
        return int(r.mode == c.mode)
    if c.kind == 'anchor':
        return int(role(r, c.mode, 'row') == 1 or
                   (not omit_vertical_dummy and r.kind == 'dummy' and c.mode[0] == 'V'))
    if r.kind != 'anchor':
        return nonanchor_entry(r, c)
    kind, i, sign, parity = r.mode
    if c.kind == 'dummy':
        return int(kind == 'W' and not omit_horizontal_dummy)
    if kind == 'V':
        return int(c.depth == i-1 and c.sign == sign)
    if sign == '+':
        return int(c.depth == i and c.sign in ('+', 'L') and c.node % 2 == parity)
    return int((c.depth == i-1 and c.sign == '-') or
               (not omit_odd and parity == 0 and c.depth == i and c.sign == '-' and c.node % 2 == 1))


def iter_copies(rows, cols, value=entry):
    A = [[value(r, c) for c in cols] for r in rows]
    full = (1 << len(cols))-1
    masks = [sum(v << j for j, v in enumerate(row)) for row in A]
    for ix in combinations(range(len(rows)), 3):
        x, y, z = [masks[i] for i in ix]
        possible = [(full ^ x) & y & z, x & (full ^ y) & z, x & y & (full ^ z)]
        if not all(possible):
            continue
        def visit(stage, start, chosen):
            if stage == 3:
                yield {'rows': list(ix), 'columns': chosen}
                return
            mask = (possible[stage] >> start) << start
            while mask:
                bit = mask & -mask
                j = bit.bit_length()-1
                mask -= bit
                yield from visit(stage+1, j+1, chosen+[j])
        yield from visit(0, 0, [])


def canonical(rs, cs, h):
    x, r, d = rs
    c, z, y = cs
    if not (x.kind == y.kind == 'anchor' and x.mode == y.mode
            and x.mode == ('W', h, '-', r.node % 2)
            and r.kind == 'variable' and r.sign == 'L'
            and d.kind == 'dummy'
            and z.kind == 'variable' and z.sign == '-' and z.depth == h-1 and z.node == r.node//2):
        return False
    return ((c.kind == 'variable' and c.sign == 'L' and c.node >= r.node and c.node//2 == r.node//2)
            or (c.kind == 'variable' and c.sign == '+' and c.depth == h-1 and c.node == r.node//2))


def census(h):
    start = time.monotonic()
    rows, cols = axis(h, 'row'), axis(h, 'column')
    total, quotient = 0, 0
    families = defaultdict(int)
    bad = []
    for w in iter_copies(rows, cols):
        rs, cs = [rows[i] for i in w['rows']], [cols[j] for j in w['columns']]
        multiplicity = prod(p.weight for p in rs+cs)
        total += multiplicity
        quotient += 1
        families['leaf_column' if cs[0].sign == 'L' else 'plus_parent_column'] += multiplicity
        if not canonical(rs, cs, h):
            bad.append(w)
    m, n = 2**h, sum(r.weight for r in rows)
    assert n == sum(c.weight for c in cols) == (8*h+2)*m
    assert not bad, bad[:1]
    assert total == 7*m**4
    assert families == {'leaf_column': 3*m**4, 'plus_parent_column': 4*m**4}
    return {'h': h, 'm': m, 'n': n, 'copies': total, 'quotient_copies': quotient,
            'families': dict(families), 'noncanonical_copies': len(bad),
            'seconds': time.monotonic()-start}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-depth', type=int, default=7)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    records = []
    for h in range(1, args.max_depth+1):
        rec = census(h)
        records.append(rec)
        print(json.dumps(rec), flush=True)
    Path(args.output).write_text(json.dumps({'pattern': H,
        'scope': 'Exact finite census. Written all-depth proof is separate; not checked in Lean.',
        'records': records}, indent=2)+'\n')


if __name__ == '__main__':
    main()
