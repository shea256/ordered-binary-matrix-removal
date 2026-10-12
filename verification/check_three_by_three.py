#!/usr/bin/env python3
"""Literal second implementation of the 3x3 host, census, and repair sampler.

Uses no discovery code, SAT solver, or third-party packages. This is a
same-agent second pass, not independent peer review or Lean verification.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
H = ((0, 1, 1), (1, 0, 1), (1, 1, 0))


def modes(h):
    return ([('W', i, '-', d) for i in range(1, h+1) for d in (0, 1)]
            + [('W', i, '+', d) for i in range(1, h+1) for d in (0, 1)]
            + [('V', i, s, -1) for i in range(1, h+1) for s in ('+', '-')])


def axes(h, name):
    def key(v):
        _, i, s, p = v
        path = tuple(1 + ((p >> j) & 1) for j in reversed(range(i)))
        return path + ((1,) if s == 'L' else (0,) if s == ('-' if name == 'row' else '+') else (3,))
    variables = [('B', i, s, p) for i in range(h) for s in ('+', '-') for p in range(2**i)]
    variables += [('B', h, 'L', p) for p in range(2**h)]
    variables.sort(key=key)
    anchors = [('A', t) for t in modes(h)]
    return anchors + variables + [('D',)] if name == 'row' else [('D',)] + variables + anchors


def weight(v, h):
    return 2**(h-v[1]) if v[0] == 'B' else 2**h


def body(r, c):
    if r[0] == 'D' or c[0] == 'D':
        return 1
    _, i, s, p = r
    _, j, t, q = c
    if i == j:
        if s in ('+', 'L') and t in ('+', 'L'):
            return int(p <= q)
        if s == t == '-':
            return int(p < q)
    if i == j+1 and s in (t, 'L'):
        return int(p//2 <= q) if t == '+' else int(p//2 < q)
    return 0


def entry(r, c, omit=None):
    if r[0] == c[0] == 'A':
        return int(r[1] == c[1])
    if c[0] == 'A':
        kind, level, sign, parity = c[1]
        if r[0] == 'D':
            return int(kind == 'V' and omit != 'vertical_dummy')
        _, i, s, p = r
        if s not in (sign, 'L'):
            return 0
        if kind == 'V':
            return int(i == (level if sign == '+' else level-1))
        return int(i == level and p % 2 == parity)
    if r[0] != 'A':
        return body(r, c)
    kind, level, sign, parity = r[1]
    if c[0] == 'D':
        return int(kind == 'W' and omit != 'horizontal_dummy')
    _, j, t, q = c
    if kind == 'V':
        return int(j == level-1 and t == sign)
    if sign == '+':
        return int(j == level and t in ('+', 'L') and q % 2 == parity)
    return int((j == level-1 and t == '-') or
               (omit != 'odd_child' and parity == 0 and j == level and t == '-' and q % 2 == 1))


def census(h, physical=False, omit=None):
    rows, cols = axes(h, 'row'), axes(h, 'column')
    if physical:
        rows = [r for r in rows for _ in range(weight(r, h))]
        cols = [c for c in cols for _ in range(weight(c, h))]
    rw = [1 if physical else weight(r, h) for r in rows]
    cw = [1 if physical else weight(c, h) for c in cols]
    A = [[entry(r, c, omit) for c in cols] for r in rows]
    full = (1 << len(cols))-1
    masks = [sum(v << j for j, v in enumerate(line)) for line in A]
    count, good, localized, leaf_family, parent_family = 0, 0, 0, 0, 0
    for ix in combinations(range(len(rows)), 3):
        x, y, z = [masks[i] for i in ix]
        candidates = [(full ^ x) & y & z, x & (full ^ y) & z, x & y & (full ^ z)]
        if not all(candidates):
            continue
        first = [j for j in range(len(cols)) if candidates[0] & (1 << j)]
        middle = [j for j in range(len(cols)) if candidates[1] & (1 << j)]
        last = [j for j in range(len(cols)) if candidates[2] & (1 << j)]
        multiplier = rw[ix[0]]*rw[ix[1]]*rw[ix[2]]
        xrow, r, d = [rows[i] for i in ix]
        valid_row = (r[0] == 'B' and r[2] == 'L' and d == ('D',)
                     and xrow == ('A', ('W', h, '-', r[3] % 2)))
        for j in middle:
            left, right = [k for k in first if k < j], [k for k in last if j < k]
            subtotal = multiplier*cw[j]*sum(cw[k] for k in left)*sum(cw[k] for k in right)
            count += subtotal
            valid_zero = r[0] == 'B' and r[2] == 'L' and cols[j] == ('B', h-1, '-', r[3]//2)
            if valid_zero:
                localized += subtotal
            if not (valid_row and valid_zero):
                continue
            right_good = sum(cw[k] for k in right if cols[k] == xrow)
            for k in left:
                c = cols[k]
                if c == ('B', h-1, '+', r[3]//2):
                    ways = multiplier*cw[j]*cw[k]*right_good
                    good += ways
                    parent_family += ways
                elif c[0] == 'B' and c[2] == 'L' and r[3] <= c[3] and c[3]//2 == r[3]//2:
                    ways = multiplier*cw[j]*cw[k]*right_good
                    good += ways
                    leaf_family += ways
    n = sum(rw)
    assert n == sum(cw) == (8*h+2)*2**h
    return {'h': h, 'n': n, 'copies': count, 'noncanonical_copies': count-good,
            'unlocalized_copies': count-localized, 'leaf_column': leaf_family,
            'plus_parent_column': parent_family}


def repair_sampler(h):
    rows, cols = axes(h, 'row'), axes(h, 'column')
    rid, cid = {r: i for i, r in enumerate(rows)}, {c: j for j, c in enumerate(cols)}
    m = 2**h
    frequency = Counter()
    frames = 0
    for z, u, v in product(range(m), repeat=3):
        def variable(i, s, seed):
            return (('B', i, 'L' if i == h else s, z//(2**(h-i))), seed % (2**(h-i)))
        rp, rm = [[variable(i, s, u) for i in range(h+1)] for s in ('+', '-')]
        cp, cm = [[variable(i, s, v) for i in range(h+1)] for s in ('+', '-')]
        dr, dc = (('D',), u), (('D',), v)
        assert rp[-1] == rm[-1] and cp[-1] == cm[-1]
        guards = {(rp[0], cp[0]), (rm[0], cm[0])}
        assert entry(rp[0][0], cp[0][0]) == 1 and entry(rm[0][0], cm[0][0]) == 0
        for i in range(h+1):
            cells = {(rp[i], dc), (rm[i], dc), (dr, cp[i]), (dr, cm[i])}
            assert all(entry(r[0], c[0]) == 1 for r, c in cells)
            guards.update(cells)
        for i in range(1, h+1):
            d = (z//2**(h-i)) % 2
            items = [(('V', i, '+', -1), rp[i], rp[i-1], dc, cp[i-1]),
                     (('V', i, '-', -1), rm[i-1], rm[i], dc, cm[i-1]),
                     (('W', i, '+', d), rp[i], dr, cp[i-1], cp[i]),
                     (('W', i, '-', d), rm[i], dr, cm[i], cm[i-1])]
            for t, a, b, c, dcol in items:
                rs, cs = [(('A', t), u), a, b], [c, dcol, (('A', t), v)]
                assert all(rid[rs[j][0]] < rid[rs[j+1][0]] for j in range(2))
                assert all(cid[cs[j][0]] < cid[cs[j+1][0]] for j in range(2))
                for j, k in product(range(3), repeat=2):
                    if j == 0 or k == 2:
                        assert entry(rs[j][0], cs[k][0]) == H[j][k]
                        guards.add((rs[j], cs[k]))
                frames += 1
        for r, c in guards:
            assert r[0][0] != 'B' or c[0][0] != 'B' or r[0][1] == c[0][1] == 0
            assert 0 <= r[1] < weight(r[0], h) and 0 <= c[1] < weight(c[0], h)
            frequency[r, c] += 1
    assert max(frequency.values()) <= m
    # Protecting a leaf diagonal instead would have a larger event fiber.
    assert sum(z == 0 for z, u, v in product(range(m), repeat=3)) == m*m > m
    return {'h': h, 'seeds': m**3, 'frames': frames,
            'maximum_guard_frequency': max(frequency.values()), 'bound': m,
            'distinct_guard_cells': len(frequency)}


def boolean_propagation():
    P = ((1, 0), (1, 1))
    survivors = []
    for bp, bm, cp, cm in product((0, 1), repeat=4):
        bodies = [((1, bp), (1, 1)), ((1, 0), (1, bm)),
                  ((bp, cp), (1, 1)), ((cm, bm), (1, 1))]
        if all(body != P for body in bodies):
            survivors.append((bp, bm, cp, cm))
    assert survivors == [(1, 0, 1, 0)]
    return survivors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-depth', type=int, default=7)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    results = []
    for h in range(1, args.max_depth+1):
        result = census(h)
        assert result['copies'] == 7*2**(4*h)
        assert result['noncanonical_copies'] == result['unlocalized_copies'] == 0
        assert result['leaf_column'] == 3*2**(4*h)
        assert result['plus_parent_column'] == 4*2**(4*h)
        results.append(result)
        print(json.dumps(result), flush=True)
    assert census(1, physical=True) == results[0]
    controls = {key: census(3, omit=key) for key in ('vertical_dummy', 'horizontal_dummy', 'odd_child')}
    assert all(r['unlocalized_copies'] > 0 for r in controls.values())
    report = {'status': 'passed', 'pattern': H, 'records': results,
              'physical_depth_one': census(1, physical=True),
              'repair_sampler': [repair_sampler(h) for h in range(1, 5)],
              'boolean_propagation': boolean_propagation(), 'negative_controls': controls,
              'scope': 'Separate same-agent implementation; finite checks do not prove universal claims or replace Lean/peer review.'}
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'checks': 'census, physical expansion, repair sampler, propagation, negative controls'}))


if __name__ == '__main__':
    main()
