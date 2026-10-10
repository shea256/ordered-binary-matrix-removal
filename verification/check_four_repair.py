#!/usr/bin/env python3
"""Flipping the new hitting set creates copies: hitting is not repairing."""
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
from host import entry
from refine_anchor import axis, crown

H = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]]


def check(h):
    rs, cs = axis(h, 2, 'row'), axis(h, 2, 'column')
    mode = ('V', h, '-', -1)
    ar = [next(x for x in rs if x.kind == 'anchor' and
               x.mode == mode and x.group == g) for g in range(2)]
    ac = [next(x for x in cs if x.kind == 'anchor' and
               x.mode == mode and x.group == g) for g in range(2)]

    def flipped(r, c):
        hit = (r.kind == c.kind == 'variable' and r.depth == h and
               c.depth == h-1 and c.sign == '-' and c.node == r.node // 2)
        if hit:
            assert entry(r, c, crown(2)) == 0
            return 1
        return entry(r, c, crown(2))

    for p in range(2**h):
        b = p // 2
        R = ar + [next(x for x in rs if x.kind == 'variable' and
                       (x.depth, x.sign, x.node) == (h-1, '-', b)),
                  next(x for x in rs if x.kind == 'variable' and
                       x.depth == h and x.node == p)]
        C = ac + [next(x for x in cs if x.kind == 'dummy'),
                  next(x for x in cs if x.kind == 'variable' and
                       (x.depth, x.sign, x.node) == (h-1, '-', b))]
        assert [[flipped(r, c) for c in C] for r in R] == H
        assert [rs.index(r) for r in R] == sorted(rs.index(r) for r in R)
        assert [cs.index(c) for c in C] == sorted(cs.index(c) for c in C)
    return {'h': h, 'leaf_choices_checked': 2**h,
            'every_choice_creates_a_V_minus_copy': True}


if __name__ == '__main__':
    print(json.dumps({'flipped_parent_zero_set': [check(h) for h in range(1, 9)],
                      'scope': 'Exact finite boundary check; all-depth explanation in proofs/four-by-four.md, Section 7.'}, indent=2))
