#!/usr/bin/env python3
"""Check 3x3 limitation certificates using a separate literal host evaluator.

No imports from the discovery code and no SAT solver are needed. This is
same-agent verification, not independent mathematical peer review.
"""
from collections import Counter
from fractions import Fraction
import itertools
import json
from math import comb, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES = [('W', '+', 0), ('W', '+', 1), ('W', '-', 0),
         ('W', '-', 1), ('V', '+', -1), ('V', '-', -1)]


def var(i, sign, node):
    return {'kind': 'variable', 'depth': i, 'sign': sign, 'node': node}


def dummy():
    return {'kind': 'dummy'}


def anchor(mode, group=0):
    return {'kind': 'anchor', 'mode': mode, 'group': group}


def key(x, name):
    if x['kind'] == 'anchor':
        kind, i, sign, parity = x['mode']
        return (0, i, TYPES.index((kind, sign, parity)), x.get('group', 0))
    if x['kind'] == 'dummy':
        return (2,) if name == 'row' else (1,)
    i, p = x['depth'], x['node']
    path = tuple(1 + ((p >> j) & 1) for j in reversed(range(i)))
    before = '-' if name == 'row' else '+'
    tail = 1 if x['sign'] == 'L' else 0 if x['sign'] == before else 3
    return ((1,) if name == 'row' else (2,)) + path + (tail,)


def weight(x, h):
    return 2**h if x['kind'] != 'variable' else 2**(h-x['depth'])


def role(x, t, name):
    kind, i, sign, parity = t
    if x['kind'] == 'dummy':
        return 2 if kind == 'W' and name == 'row' else 1 if kind == 'V' and name == 'column' else 0
    if x['kind'] != 'variable' or x['sign'] not in (sign, 'L'):
        return 0
    depth, p = x['depth'], x['node']
    if kind == 'V':
        if name == 'column':
            return 2 if depth == i-1 else 0
        if sign == '+':
            return 1 if depth == i else 2 if depth == i-1 else 0
        return 1 if depth == i-1 else 2 if depth == i else 0
    if name == 'row':
        return 1 if depth == i and p % 2 == parity else 0
    child = depth == i and p % 2 == parity
    parent = depth == i-1
    return (1 if parent else 2 if child else 0) if sign == '+' else (1 if child else 2 if parent else 0)


def body(r, c, coarse=False):
    if r['kind'] == 'dummy' or c['kind'] == 'dummy':
        return 1
    i, j, p, q = r['depth'], c['depth'], r['node'], c['node']
    if i == j:
        if r['sign'] in ('+', 'L') and c['sign'] in ('+', 'L'):
            return int(p <= q)
        if r['sign'] == c['sign'] == '-':
            return int(p // 2 < q // 2) if coarse else int(p < q)
    if i == j+1 and r['sign'] in (c['sign'], 'L'):
        if c['sign'] == '+':
            return int(p // 2 <= q)
        if c['sign'] == '-':
            return int(p // 2 < q)
    return 0


def value(r, c):
    if r['kind'] == c['kind'] == 'anchor':
        return int(r['group'] != c['group']) if r['mode'] == c['mode'] else 0
    if r['kind'] == 'anchor':
        return int(role(c, r['mode'], 'column') == r['group']+1)
    if c['kind'] == 'anchor':
        return int(role(r, c['mode'], 'row') == c['group']+1)
    return body(r, c)


def check_occurrence(H, axes, witness, h):
    chosen = {}
    count = 1
    for name in ('rows', 'columns'):
        positions = [axes[name][i] for i in witness[name]]
        keys = [key(x, 'row' if name == 'rows' else 'column') for x in positions]
        assert keys == sorted(keys)
        for index, times in Counter(witness[name]).items():
            w = weight(axes[name][index], h)
            assert w >= times
            count *= comb(w, times)
        assert all(x['kind'] != 'variable' or x['depth'] < h for x in positions)
        chosen[name] = positions
    assert [[value(r, c) for c in chosen['columns']] for r in chosen['rows']] == H
    return count


def decode(word):
    return [[int(word[3*i+j]) for j in range(3)] for i in range(3)]


def forced_bit_cases():
    K = [[0, 1, 0], [1, 1, 0], [0, 1, 1]]
    Q = [[1, 0, 1], [1, 1, 0], [0, 1, 1]]
    plus = ('W', 2, '+', 0)
    minus = ('W', 2, '-', 0)
    return [
        (K, plus, 1, [anchor(plus), var(2, '+', 1), dummy()],
         [anchor(plus), var(1, '+', 0), var(2, '+', 0)],
         (var(2, '+', 1), anchor(plus))),
        (K, plus, 0, [var(2, '+', 1), var(2, '+', 2), dummy()],
         [anchor(plus), dummy(), var(0, '+', 0)],
         (var(2, '+', 1), anchor(plus))),
        (Q, minus, 0, [anchor(minus), var(2, '-', 0), dummy()],
         [anchor(minus), var(2, '-', 1), var(1, '-', 0)],
         (anchor(minus), var(2, '-', 1))),
        (Q, minus, 1, [anchor(minus), var(3, '-', 0), var(2, '-', 1)],
         [var(2, '-', 1), var(2, '-', 2), var(1, '-', 1)],
         (anchor(minus), var(2, '-', 1))),
    ]


def check_forced_bits():
    cases = []
    for H, t, bit, rs, cs, free in forced_bit_cases():
        def forced(r, c):
            if (r, c) == free:
                return bit
            if r['kind'] == c['kind'] == 'anchor':
                assert r['mode'] == c['mode'] == t
                return H[0][0]
            if r['kind'] == 'anchor':
                j = role(c, t, 'column')
                assert j  # Every other anchor incidence is prescribed.
                return H[0][j]
            if c['kind'] == 'anchor':
                i = role(r, t, 'row')
                assert i
                return H[i][0]
            return body(r, c)
        assert [[forced(r, c) for c in cs] for r in rs] == H
        for xs, name in ((rs, 'row'), (cs, 'column')):
            assert [key(x, name) for x in xs] == sorted(key(x, name) for x in xs)
        # These templates have distinct blocks on each axis.
        coefficient = Fraction(prod(weight(x, 4) for x in rs+cs), 16**6)
        cases.append({'pattern': ''.join(map(str, sum(H, []))), 'free_bit': bit,
                      'mode': t, 'rows': rs, 'columns': cs,
                      'coefficient_for_constant_bit': str(coefficient)})
    assert [c['coefficient_for_constant_bit'] for c in cases] == ['1/32', '1/16', '1/32', '1/1024']
    return cases


def check_leaf_family(h):
    m = 2**h
    rows = [[var(h, 'L', p) for p in range(m//8)],
            [var(h-1, '-', p) for p in range(m//8, 3*m//16)],
            [var(h-1, '+', p) for p in range(3*m//16, m//4)]]
    cols = [[var(h-1, '-', q) for q in range(m//4, 5*m//16)],
            [var(h-1, '+', q) for q in range(5*m//16, 3*m//8)],
            [var(h, 'L', q) for q in range(7*m//8, m)]]
    H = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]
    for groups, name in ((rows, 'row'), (cols, 'column')):
        for i in range(2):
            assert max(key(x, name) for x in groups[i]) < min(key(x, name) for x in groups[i+1])
        assert all(sum(weight(x, h) for x in group) == m//8 for group in groups)
    for i, j in itertools.product(range(3), repeat=2):
        assert all(body(r, c) == H[i][j] for r in rows[i] for c in cols[j])
    return {'h': h, 'certified_copies': (m//8)**6,
            'coefficient_of_m_to_six': '1/262144'}


def check_coarsening():
    rows = [var(1, '-', 0), var(2, '-', 0)]
    cols = [dummy(), var(1, '-', 1)]
    assert [[body(r, c, True) for c in cols] for r in rows] == [[1, 0], [1, 1]]
    t = ('V', 2, '-', -1)
    assert [role(x, t, 'row') for x in rows] == [1, 2]
    assert [role(x, t, 'column') for x in cols] == [1, 2]
    return {'mode': t, 'body_rows': rows, 'body_columns': cols,
            'scope': 'A fixed nonleaf designated P body defeats all 32 borders after the tested coarsening.'}


def main():
    data = json.loads((ROOT/'verification/three-search-report.json').read_text())
    assert len(data['all_3x3_patterns']) == 512
    assert {x['pattern'] for x in data['all_3x3_patterns']} == {format(i, '09b') for i in range(512)}
    assert len(data['one_anchor_borders']) == 32
    assert {x['pattern'] for x in data['one_anchor_borders']} == {
        ''.join(map(str, [a, c1, c2, r1, 1, 0, r2, 1, 1]))
        for a, r1, r2, c1, c2 in itertools.product((0, 1), repeat=5)}
    positive = [x for x in data['all_3x3_patterns'] if x['witness']]
    borders = [x for x in data['one_anchor_borders'] if x['witness']]
    assert len(positive) == 509 and len(borders) == 30 and len(data['deletions']) == 24
    checked = 0
    for h in (4, 5, 8):
        for item in positive:
            check_occurrence(decode(item['pattern']), data['host_axes'], item['witness'], h)
            checked += 1
        for item in borders:
            check_occurrence(decode(item['pattern']), data['nonanchor_axes'], item['witness'], h)
            checked += 1
        for item in data['deletions']:
            check_occurrence(item['pattern'], data['host_axes'], item['witness'], h)
            checked += 1
    counts = data['full_counts_for_trunk_exceptions']
    assert [[x['copies'] for x in item['counts']] for item in counts] == [
        [0]*5, [0]*5, [0, 48, 1120, 81088, 5720448]]
    return {'verified_fixed_depth_witnesses_including_lifts': checked,
            'distinct_3x3_patterns_with_trunk_witnesses': 509,
            'direct_deletions_with_witnesses': 24,
            'one_anchor_borders_with_nonanchor_witnesses': 30,
            'remaining_two_borders': check_forced_bits(),
            'leaf_family': [check_leaf_family(h) for h in range(4, 9)],
            'coarsening_counterexample': check_coarsening(),
            'scope': 'Certificates for limitations of specified hosts/encodings, not a global lower bound of four. Same-agent exact verification; no independent peer review.'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
