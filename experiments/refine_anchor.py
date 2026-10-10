#!/usr/bin/env python3
"""Exact ordered-anchor search. Weighted twins represented once.

The new mode order places W before V at each depth. No original source is
modified; the previous host remains available for regression comparison.
"""
import argparse
import itertools
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from host import Position, entry, modes, nonanchors


def refined_modes(h):
    return sorted(modes(h), key=lambda t: (t[1], t[0] == 'V', t[2] == '-', t[3]))


def crown(s):
    return [[int(i != j) for j in range(s)] for i in range(s)]


def axis(h, s, name, reordered=True):
    ts = refined_modes(h) if reordered else modes(h)
    return [Position('anchor', mode=t, group=g, weight=2**h)
            for t in ts for g in range(s)] + nonanchors(h, name)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def check_three(h, reordered=True, stop_on_failure=True):
    S = crown(3)
    rows, cols = axis(h, 3, 'row', reordered), axis(h, 3, 'column', reordered)
    masks = [sum(entry(r, c, S) << j for j, c in enumerate(cols)) for r in rows]
    full = (1 << len(cols)) - 1
    count, weighted, triples = 0, 0, 0
    for ix in itertools.combinations(range(len(rows)), 3):
        triples += 1
        x, y, z = (masks[i] for i in ix)
        # Column signatures of J_3-I_3 in their required order.
        a, b, c = ((full ^ x) & y & z, x & (full ^ y) & z, x & y & (full ^ z))
        if not (a and b and c):
            continue
        for j in bits(a):
            for k in bits(b >> (j+1)):
                k += j+1
                for l in bits(c >> (k+1)):
                    l += k+1
                    selected = [rows[i] for i in ix] + [cols[q] for q in (j,k,l)]
                    canonical = (all(p.kind == 'anchor' for p in selected)
                                 and len({p.mode for p in selected}) == 1)
                    if not canonical:
                        witness = {'h': h, 'reordered': reordered,
                                   'rows': [vars(rows[i]) for i in ix],
                                   'cols': [vars(cols[q]) for q in (j,k,l)]}
                        if stop_on_failure:
                            return {'unexpected_copy': witness}
                        raise AssertionError(witness)
                    count += 1
                    weight = 1
                    for p in selected:
                        weight *= p.weight
                    weighted += weight
    assert count == 6*h
    assert weighted == 6*h*(2**h)**6
    return {'h': h, 'reordered': reordered, 'quotient_rows': len(rows),
            'row_triples_checked': triples, 'canonical_quotient_copies': count,
            'weighted_anchor_copies': weighted, 'unexpected_copies': 0}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--max-depth', type=int, default=5)
    p.add_argument('--original-order', action='store_true')
    args = p.parse_args()
    print(json.dumps([check_three(h, not args.original_order)
                      for h in range(1, args.max_depth+1)], indent=2))
