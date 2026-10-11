#!/usr/bin/env python3
"""Exact finite checks of a nonuniform 3x4 candidate; not an all-depth proof."""
import argparse
from collections import defaultdict
import json
from math import prod
from pathlib import Path
import sys
import time
sys.dont_write_bytecode = True
from search_asymmetric_templates import axes, value
from search_asymmetric_completion import copy_batch

H = [[1,0,0,1], [1,0,1,0], [0,1,1,1]]


def entry(r, c):
    bit = value(r, c, H, (0,0,0,0,0))
    if r.kind == 'anchor' and c.kind != 'anchor' and r.mode[0] == 'W':
        if c.kind == 'dummy':
            return 1
        if (r.mode[2:] == ('-', 0) and c.kind == 'variable'
                and c.depth == r.mode[1] and c.sign == '-' and c.node % 2 == 1):
            return 1
    return bit


def census(h):
    start = time.monotonic()
    rows, cols = axes(h, 'row', full=True), axes(h, 'column', full=True)
    A = [[entry(r, c) for c in cols] for r in rows]
    # H has pairwise distinct rows and columns, so no twin block can be reused.
    cap = 10_000_000
    copies = copy_batch(H, A, limit=cap)
    assert len(copies) < cap, 'Census cap reached; do not report an incomplete count.'
    by_anchors, by_mode = defaultdict(int), defaultdict(int)
    witnesses = {}
    bad = []
    for w in copies:
        rs, cs = [rows[i] for i in w['rows']], [cols[j] for j in w['columns']]
        multiplicity = prod(x.weight for x in rs+cs)
        config = str((sum(r.kind == 'anchor' for r in rs), sum(c.kind == 'anchor' for c in cs)))
        by_anchors[config] += multiplicity
        mode = str(rs[0].mode) if rs[0].kind == 'anchor' else 'none'
        by_mode[mode] += multiplicity
        witnesses.setdefault(config, {'rows':[vars(r) for r in rs], 'columns':[vars(c) for c in cs]})
        r,c = rs[1],cs[3]
        if not (r.kind == c.kind == 'variable' and r.sign == 'L' and c.sign == '-'
                and c.depth == h-1 and r.node//2 == c.node):
            bad.append(w)
    return {'h':h, 'm':2**h, 'n':sum(r.weight for r in rows), 'quotient_copies':len(copies),
            'copies':sum(by_anchors.values()), 'by_anchor_counts':dict(by_anchors),
            'by_first_mode':dict(by_mode), 'example_for_each_configuration':witnesses,
            'bad_localization_witnesses':bad[:10], 'seconds':time.monotonic()-start}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-depth', type=int, default=6)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    results = []
    for h in range(1, args.max_depth+1):
        result = census(h)
        results.append(result)
        print(json.dumps({k:result[k] for k in ('h','copies','quotient_copies','by_anchor_counts','seconds')}),flush=True)
        assert result['bad_localization_witnesses'] == []
    Path(args.output).write_text(json.dumps({'pattern':H,
        'scope':'Finite evidence for a nonuniform candidate; universal theorem needs a written proof.',
        'results':results},indent=2)+'\n')


if __name__ == '__main__':
    main()
