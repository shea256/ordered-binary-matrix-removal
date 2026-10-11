#!/usr/bin/env python3
"""Separate-agent exact checks for the global minus-first candidate.

No candidate/Erebos code imports. This uses recursive axis construction and
enumerates column quadruples, then all matching increasing row quadruples.
All sixteen bits are tested before checking proposed structural conclusions.
Compression is justified by distinct H rows/columns and full block twins.
Finite evidence only; no universal-proof or Lean-build claim.
"""
from collections import Counter
from itertools import combinations, product
from math import prod
from fractions import Fraction
import argparse
import json
import platform

H = ((0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 1))


def modes(h, order='global'):
    kinds = [('W', '-', 0), ('W', '-', 1), ('W', '+', 0),
             ('W', '+', 1), ('V', '+', None), ('V', '-', None)]
    if order == 'global':
        return ([(i, 'W', '-', d) for i in range(1, h+1) for d in (0, 1)]
                + [(i, 'W', '+', d) for i in range(1, h+1) for d in (0, 1)]
                + [(i, 'V', s, None) for i in range(1, h+1) for s in ('+', '-')])
    if order == 'erebos':
        kinds = kinds[4:] + kinds[2:4] + kinds[:2]
    elif order == 'previous':
        kinds = kinds[2:4] + kinds[:2] + kinds[4:]
    else:
        raise ValueError(order)
    return [(i, k, s, d) for i in range(1, h+1) for k, s, d in kinds]


def axes(h, row, order='global', expanded=False):
    m = 2**h
    def visit(i, p):
        if i == h:
            return [('V', i, 'L', p)]
        a, b = ('-', '+') if row else ('+', '-')
        return [('V', i, a, p)] + visit(i+1, 2*p) + visit(i+1, 2*p+1) + [('V', i, b, p)]
    anchors = [('A', t, g) for t in modes(h, order) for g in (0, 1)]
    tree, dummy = visit(0, 0), [('D',)]
    blocks = anchors + (tree+dummy if row else dummy+tree)
    weights = [m if p[0] != 'V' else 2**(h-p[1]) for p in blocks]
    assert sum(weights) == (14*h+2)*m
    if expanded:
        blocks = [p for p, w in zip(blocks, weights) for _ in range(w)]
        weights = [1]*len(blocks)
    return blocks, weights


def role(t, g, x, row):
    i, k, s, d = t
    if x[0] == 'A':
        return False
    if x[0] == 'D':
        return (k == 'W' and g == 1) if row else (k == 'V' and g == 0)
    def at(j):
        return x[1] == j and x[2] in (s, 'L')
    if k == 'V':
        if not row:
            return g == 1 and at(i-1)
        return at((i if g == 0 else i-1) if s == '+' else (i-1 if g == 0 else i))
    if row:
        return g == 0 and at(i) and x[3] % 2 == d
    child = g == (1 if s == '+' else 0)
    return at(i) and x[3] % 2 == d if child else at(i-1)


def entry(r, c):
    if r[0] == c[0] == 'A':
        return int(r[1] == c[1] and r[2] != c[2])
    if r[0] == 'A':
        return int(role(r[1], r[2], c, False))
    if c[0] == 'A':
        return int(role(c[1], c[2], r, True))
    if r[0] == 'D' or c[0] == 'D':
        return 1
    _, i, s, p = r
    _, j, t, q = c
    if i == j and s == t:
        return int(p < q) if s == '-' else int(p <= q)
    if i == j+1 and (s == 'L' or s == t):
        return int(p//2 < q) if t == '-' else int(p//2 <= q)
    return 0


def terminal(c, h):
    return c[0] == 'A' and c[1][0:3] == (h, 'W', '-') and c[2] == 0


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask -= bit


def census(h, order='global', repair=False, expanded=False):
    rows, rw = axes(h, True, order, expanded)
    cols, cw = axes(h, False, order, expanded)
    full = (1 << len(rows))-1
    def value(r, c):
        return 0 if repair and r[0] != 'A' and terminal(c, h) else entry(r, c)
    ones = [sum(value(r, c) << i for i, r in enumerate(rows)) for c in cols]
    zeros = [full ^ mask for mask in ones]
    total = witnesses = 0
    configurations = Counter()
    edit_count = sum(rw[i]*cw[j] for i, r in enumerate(rows) for j, c in enumerate(cols)
                     if value(r, c) != entry(r, c))
    for js in combinations(range(len(cols)), 4):
        candidates = []
        for target in H:
            mask = full
            for j, v in zip(js, target):
                mask &= ones[j] if v else zeros[j]
            if not mask:
                break
            candidates.append(mask)
        if len(candidates) != 4:
            continue
        for a in bits(candidates[0]):
            for b in bits(candidates[1] & (full ^ ((1 << (a+1))-1))):
                for c in bits(candidates[2] & (full ^ ((1 << (b+1))-1))):
                    for d in bits(candidates[3] & (full ^ ((1 << (c+1))-1))):
                        is_ = a, b, c, d
                        R, C = [rows[i] for i in is_], [cols[j] for j in js]
                        weight = prod(rw[i] for i in is_)*prod(cw[j] for j in js)
                        total += weight
                        witnesses += 1
                        conf = (sum(r[0] == 'A' for r in R), sum(c[0] == 'A' for c in C))
                        configurations[str(conf)] += weight
                        if order == 'global' and not repair:
                            assert conf in ((2, 1), (2, 2)), (h, R, C)
                            assert R[2][0:3] == ('V', h, 'L') and R[3][0] == 'D'
                            p = R[2][3]
                            assert C[3] == ('V', h-1, '-', p//2)
                            B = (h, 'W', '-', p % 2)
                            assert R[0] == ('A', B, 0) and R[1] == ('A', B, 1)
                            assert C[0] == ('A', B, 0)
                            if conf == (2, 2):
                                assert C[1] == ('A', B, 1) and C[2] == R[2]
                            else:
                                assert C[1][0:3] == ('V', h, 'L') and C[2] == R[2]
                                assert C[1][3] < p and C[1][3] % 2 == p % 2
    m = 2**h
    expected = 0 if repair else (5*m**6)//2-m**5 if order == 'global' else 128 if h == 1 else ((41 if order == 'erebos' else 33)*m**6-(74 if order == 'erebos' else 58)*m**5)//4
    assert total == expected, (h, order, repair, total, expected)
    assert edit_count == (m*m if repair else 0)
    return {'h': h, 'order': order, 'repair': repair, 'expanded': expanded,
            'copies': total, 'compressed_witnesses': witnesses, 'edits': edit_count,
            'anchor_configurations': dict(sorted(configurations.items()))}


def supports_audit(max_h=7):
    data = []
    for h in range(1, max_h+1):
        ts = modes(h)
        result = {'h': h, 'proper_support_inclusions': 0, 'generic_survivors': 0}
        rr, cc = [], []
        for row in (True, False):
            xs = [x for x in axes(h, row)[0] if x[0] != 'A']
            supports = [{x for x in xs if role(t, g, x, row)} for t in ts for g in (0, 1)]
            for ai, A in enumerate(supports):
                assert A.isdisjoint(supports[ai ^ 1])
                for bi, B in enumerate(supports):
                    assert not A & B or A <= B or B <= A
                    if A < B:
                        assert ai//2 < bi//2
                        result['proper_support_inclusions'] += 1
            (rr if row else cc).extend(supports)
        idx = {x: i for i, x in enumerate(axes(h, False)[0])}
        for bi, B in enumerate(ts):
            for ai in range(bi+1):
                for group in (0, 1):
                    for r in rr[2*bi] - {('D',)}:
                        cs = [c for c in cc[2*ai+group] - {('D',)} if entry(r, c)]
                        ds = [d for d in cc[2*bi+1] - {('D',)} if not entry(r, d)]
                        for c, d in product(cs, ds):
                            if idx[c] >= idx[d]:
                                continue
                            result['generic_survivors'] += 1
                            assert r[0:3] == ('V', h, 'L')
                            assert d == ('V', h-1, '-', r[3]//2)
                            assert c[0:3] == ('V', h, 'L')
                            assert ai == bi and group == 0 and c == r
        data.append(result)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-h', type=int, default=4)
    parser.add_argument('--support-max-h', type=int, default=7)
    args = parser.parse_args()
    report = {'python': platform.python_version(), 'scope': 'Separate-agent finite evidence, no candidate code imports, not peer review or universal certification.'}
    report['global_census'] = [census(h, repair=repair) for h in range(1, args.max_h+1) for repair in (False, True)]
    report['expanded_height_one'] = [census(1, repair=repair, expanded=True) for repair in (False, True)]
    report['baseline_census'] = [census(h, order=order) for h in range(1, min(args.max_h, 3)+1) for order in ('erebos', 'previous')]
    report['support_audit'] = supports_audit(args.support_max_h)
    report['comparison'] = [{'h': h, 'reduction_from_erebos': str(1-Fraction((10*2**h-4), (41*2**h-74)))} for h in range(2, 7)]
    report['limiting_reduction_from_erebos'] = str(Fraction(31, 41))
    print(json.dumps(report, indent=2))
