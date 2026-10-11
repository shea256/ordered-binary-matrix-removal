#!/usr/bin/env python3
"""Separate-agent finite checks; no discovery/candidate code imports.

Recursive axes and explicit column-quadruple/row-triple census differ from
the candidate's sorted-coordinate axes and weighted subsequence DP.
Finite evidence only: all-depth arguments are in the companion review.
"""
from collections import Counter
from itertools import combinations
from math import prod
import argparse
import json
import platform

H = ((1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 1, 1))


def modes(h):
    return ([(i, 'W', '-', d) for i in range(1, h+1) for d in (0, 1)]
            + [(i, 'W', '+', d) for i in range(1, h+1) for d in (0, 1)]
            + [(i, 'V', s, -1) for i in range(1, h+1) for s in ('+', '-')])


def axis(h, row, expanded=False):
    def visit(i, p):
        if i == h:
            return [('X', i, 'L', p)]
        left, right = ('-', '+') if row else ('+', '-')
        return ([('X', i, left, p)] + visit(i+1, 2*p)
                + visit(i+1, 2*p+1) + [('X', i, right, p)])
    anchors = [('A', t, g) for t in modes(h) for g in ((0,) if row else (0, 1))]
    tree, dummy = visit(0, 0), [('D',)]
    xs = anchors + (tree+dummy if row else dummy+tree)
    m = 2**h
    weights = [2**(h-x[1]) if x[0] == 'X' else 2*m if row and x[0] == 'A' else m for x in xs]
    assert sum(weights) == (14*h+2)*m
    if expanded:
        xs = [x for x, w in zip(xs, weights) for _ in range(w)]
        weights = [1]*len(xs)
    return xs, weights


def row_role(t, g, r):
    i, kind, sign, parity = t
    if r[0] == 'D':
        return kind == 'W' and g == 1
    if r[0] != 'X':
        return False
    if kind == 'W':
        return g == 0 and r[1] == i and r[2] in (sign, 'L') and r[3] % 2 == parity
    depth = (i if g == 0 else i-1) if sign == '+' else (i-1 if g == 0 else i)
    return r[1] == depth and r[2] in (sign, 'L')


def top(t, c):
    i, kind, sign, parity = t
    if c[0] == 'D':
        return kind == 'W'
    if c[0] != 'X':
        return False
    _, j, s, q = c
    if kind == 'V':
        return j == i-1 and s == sign
    if sign == '+':
        return j == i and s in ('+', 'L') and q % 2 == parity
    return s == '-' and (j == i-1 or j == i and parity == 0 and q % 2 == 1)


def body(r, c):
    if r[0] == 'D' or c[0] == 'D':
        return 1
    _, i, s, p = r
    _, j, t, q = c
    if i == j and s == t:
        return int(p < q) if s == '-' else int(p <= q)
    if i == j+1 and (s == 'L' or s == t):
        return int(p//2 < q) if t == '-' else int(p//2 <= q)
    return 0


def entry(r, c):
    if r[0] == c[0] == 'A':
        return int(r[1] == c[1] and c[2] == 0)
    if r[0] == 'A':
        return int(top(r[1], c))
    if c[0] == 'A':
        return int(row_role(c[1], c[2], r))
    return body(r, c)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask -= bit


def census(h, expanded=False):
    rs, rw = axis(h, True, expanded)
    cs, cw = axis(h, False, expanded)
    full = (1 << len(rs))-1
    ones = [sum(entry(r, c) << i for i, r in enumerate(rs)) for c in cs]
    zeros = [full ^ x for x in ones]
    counts = Counter()
    witnesses = 0
    for js in combinations(range(len(cs)), 4):
        possible = []
        for signature in H:
            mask = full
            for j, bit in zip(js, signature):
                mask &= ones[j] if bit else zeros[j]
            if not mask:
                break
            possible.append(mask)
        if len(possible) != 3:
            continue
        for a in bits(possible[0]):
            for b in bits(possible[1] >> (a+1)):
                b += a+1
                for c in bits(possible[2] >> (b+1)):
                    c += b+1
                    ix = a, b, c
                    R, C = [rs[i] for i in ix], [cs[j] for j in js]
                    conf = sum(x[0] == 'A' for x in R), sum(x[0] == 'A' for x in C)
                    assert conf in ((1, 1), (1, 2)), (h, R, C)
                    assert R[0][1][:3] == (h, 'W', '-')
                    assert R[1][:3] == ('X', h, 'L') and R[2] == ('D',)
                    assert C[3] == ('X', h-1, '-', R[1][3]//2)
                    counts[str(conf)] += prod(rw[i] for i in ix)*prod(cw[j] for j in js)
                    witnesses += 1
    return {'h': h, 'expanded': expanded, 'copies': sum(counts.values()),
            'literal_quotient_witnesses': witnesses, 'anchor_counts': dict(counts)}


def structural(h):
    rs = [x for x in axis(h, True)[0] if x[0] != 'A']
    cs = [x for x in axis(h, False)[0] if x[0] != 'A']
    ts = modes(h)
    supports = [{x for x in cs if top(t, x)} for t in ts]
    variable = {x for x in cs if x[0] == 'X'}
    crossing = 0
    for a, A in enumerate(ts):
        for b in range(a+1, len(ts)):
            B = ts[b]
            SA, SB = supports[a], supports[b]
            if SA & SB & variable and (SA-SB) & variable and SB-SA:
                crossing += 1
                assert A == (A[0], 'W', '-', 0) and A[0] < h
                assert B[0] == A[0]+1 and B[2] == '-' and B[1] in ('W', 'V')
    role_supports = [{x for x in rs if row_role(t, g, x)} for t in ts for g in (0, 1)]
    assert all(not A & B or A <= B or B <= A for A in role_supports for B in role_supports)
    terminal = vertical_dummy = 0
    for t in ts:
        for r in rs:
            if not row_role(t, 0, r):
                continue
            for j, c in enumerate(cs):
                if top(t, c) or not body(r, c):
                    continue
                for d in cs[j+1:]:
                    if not top(t, d) or body(r, d):
                        continue
                    if t[1] == 'V':
                        assert c == ('D',)
                        assert all(x == ('D',) for x in rs[rs.index(r)+1:] if body(x, d))
                        vertical_dummy += 1
                    else:
                        assert t[:3] == (h, 'W', '-')
                        assert r[:3] == ('X', h, 'L') and d == ('X', h-1, '-', r[3]//2)
                        assert all(x == ('D',) for x in rs[rs.index(r)+1:] if body(x, d))
                        terminal += 1
    return {'h': h, 'crossing_anchor_support_pairs': crossing,
            'terminal_generic_triples': terminal, 'vertical_dummy_generic_triples': vertical_dummy}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--census-height', type=int, default=4)
    p.add_argument('--structural-height', type=int, default=7)
    args = p.parse_args()
    print(json.dumps({'python': platform.python_version(),
                      'scope': 'Separate-agent finite checks, not human peer review or formal verification.',
                      'census': [census(h) for h in range(1, args.census_height+1)],
                      'expanded_height_one': census(1, True),
                      'structural': [structural(h) for h in range(1, args.structural_height+1)]}, indent=2))
