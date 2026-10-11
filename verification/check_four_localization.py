#!/usr/bin/env python3
"""Reproduce separate-agent localization checks; imports no candidate code.

The host helpers are independently transcribed from the manuscript, matching
the earlier reviewer-four-localization.py. Finite evidence, not a Lean build
or a proof of the unbounded theorem.
"""
import argparse
import json
import platform
from itertools import product


def modes(h):
    return [(i, k, s, d) for i in range(1, h + 1)
            for k, s, d in [('W', '+', 0), ('W', '+', 1),
                            ('W', '-', 0), ('W', '-', 1),
                            ('V', '+', None), ('V', '-', None)]]


def axis(h, row):
    def visit(i, p):
        if i == h:
            return [(i, 'L', p)]
        first, last = ('-', '+') if row else ('+', '-')
        return ([(i, first, p)] + visit(i + 1, p * 2)
                + visit(i + 1, p * 2 + 1) + [(i, last, p)])
    xs = visit(0, 0)
    return xs + [('dummy',)] if row else [('dummy',)] + xs


def supports(h, t, row):
    i, k, s, d = t
    def whole(j):
        return {(j, 'L' if j == h else s, p) for p in range(2 ** j)}
    def half(j):
        return {(j, 'L' if j == h else s, p) for p in range(d, 2 ** j, 2)}
    dummy = {('dummy',)}
    if k == 'V':
        if not row:
            return dummy, whole(i - 1)
        return (whole(i), whole(i - 1)) if s == '+' else (whole(i - 1), whole(i))
    if row:
        return half(i), dummy
    return (whole(i - 1), half(i)) if s == '+' else (half(i), whole(i - 1))


def val(r, c):
    if r == ('dummy',) or c == ('dummy',):
        return 1
    i, s, p = r
    j, t, q = c
    if i == j:
        if s == t and s in ('+', 'L'):
            return int(p <= q)
        if s == t == '-':
            return int(p < q)
    if i == j + 1:
        if s in ('+', 'L') and t == '+':
            return int(p // 2 <= q)
        if s in ('-', 'L') and t == '-':
            return int(p // 2 < q)
    return 0


def run_generic():
    records = []
    for h in range(1, 8):
        ts = modes(h)
        idx = {x: i for i, x in enumerate(axis(h, False))}
        rr = [supports(h, t, True) for t in ts]
        cr = [supports(h, t, False) for t in ts]
        antecedent = survivors = 0
        for bi, B in enumerate(ts):
            for ai in range(bi + 1):
                for group in (0, 1):
                    for r in rr[bi][0] - {('dummy',)}:
                        cs = [c for c in cr[ai][group] - {('dummy',)} if val(r, c)]
                        ds = [d for d in cr[bi][1] - {('dummy',)} if not val(r, d)]
                        for c, d in product(cs, ds):
                            antecedent += 1
                            if idx[c] >= idx[d]:
                                continue
                            survivors += 1
                            assert (r[0] == h and d[:2] == (h - 1, '-')
                                    and d[2] == r[2] // 2
                                    and (c[0] == h or c[:2] == (h - 1, '+'))), (h, B, ts[ai], group, r, c, d)
        records.append({'h': h, 'one_zero_triples': antecedent, 'ordered_survivors': survivors})
    h = 3
    B, A = (2, 'W', '-', 0), (2, 'W', '-', 1)
    r, c, d = (2, '-', 2), (2, '-', 3), (1, '-', 1)
    assert r in supports(h, B, True)[0] and d in supports(h, B, False)[1]
    assert c in supports(h, A, False)[0] and val(r, c) == 1 and val(r, d) == 0
    assert axis(h, False).index(c) < axis(h, False).index(d)
    assert modes(h).index(A) > modes(h).index(B) and r[0] < h
    return {'records': records, 'missing_mode_order_counterexample':
            {'h': h, 'A': A, 'B': B, 'r': r, 'c': c, 'd': d}}


def run_bounds():
    checks = 0
    for h in range(7):
        m = 2 ** h
        def key(v):
            k, x = v
            if k == 2 * h:
                return 2 * x + 1, 2, 0, k, x
            i = k // 2
            size = 2 ** (h - i)
            p = x // size
            return ((2 * p * size, 1, i, k, x) if k % 2 == 0
                    else (2 * (p + 1) * size, 0, h - i, k, x))
        xs = sorted(product(range(2 * h + 1), range(m)), key=key)
        for i, (ck, cx) in enumerate(xs):
            cp = cx // 2 ** (h - ck // 2)
            for dk, dx in xs[i + 1:]:
                dp = dx // 2 ** (h - dk // 2)
                if ck // 2 == dk // 2:
                    assert cp <= dp
                    if ck % 2 == 1 and dk % 2 == 0:
                        assert cp < dp
                if ck // 2 == dk // 2 + 1:
                    assert cp // 2 <= dp
                    if dk % 2 == 0:
                        assert cp // 2 < dp
                if dk // 2 == ck // 2 + 1:
                    assert cp <= dp // 2
                    if ck % 2 == 1:
                        assert cp < dp // 2
                checks += 1
    return {'depths': [0, 6], 'ordered_actual_position_pairs': checks,
            'all_six_implications_passed': True}


def run_zeros():
    records = []
    for h in range(11):
        m = 2 ** h
        zeros = [(p, q) for p in range(m) for q in range(m)
                 if h >= 1 and q // 2 == p // 2]
        codes = [(p, q % 2) for p, q in zeros]
        assert len(codes) == len(set(codes))
        assert len(zeros) <= 2 * m
        assert len(zeros) == (2 * m if h else 0)
        for p, q in zeros:
            assert val((h, 'L', p), (h - 1, '-', q // 2)) == 0
        records.append({'h': h, 'zero_cells': len(zeros), 'distinct_codes': len(set(codes))})
    # The LastRow class-intersection argument, stripped of node thresholds.
    shape_cases = 0
    for h in range(1, 101):
        d = 2 * h - 1
        for q in (2 * h, 2 * h - 2):
            for s in range(2 * h + 1):
                def possible(row, col):
                    return (row == col or row == col + 2
                            or (row == 2 * h and col + 1 == 2 * h))
                if possible(s, q) and possible(s, d):
                    shape_cases += 1
                    assert s == 2 * h
    return {'records': records, 'last_row_class_intersections': shape_cases,
            'class_intersection_depths': [1, 100]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', choices=['generic', 'bounds', 'zeros', 'all'], default='all')
    args = parser.parse_args()
    report = {'python': platform.python_version(),
              'scope': 'Separate-agent exact finite checks; no candidate-package imports, Lean build, or universal certification.'}
    for name, fn in [('generic', run_generic), ('bounds', run_bounds), ('zeros', run_zeros)]:
        if args.check in (name, 'all'):
            report[name] = fn()
    print(json.dumps(report, indent=2))
