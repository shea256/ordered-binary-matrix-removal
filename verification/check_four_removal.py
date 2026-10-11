#!/usr/bin/env python3
"""Separate-agent finite repair/count audit; imports no candidate code.

Host entries and recursive orders are transcribed directly from the manuscript.
This checks the inherited three-seed sampler rather than the manuscript's
larger product sampler. It is finite evidence, not a Lean build or a universal
arbitrary-repair proof.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import platform

H = ((0, 1, 1, 0), (1, 0, 0, 1),
     (1, 0, 1, 0), (0, 1, 1, 1))


def modes(h):
    return [(i, k, s, d) for i in range(1, h + 1)
            for k, s, d in [('W', '+', 0), ('W', '+', 1),
                            ('W', '-', 0), ('W', '-', 1),
                            ('V', '+', None), ('V', '-', None)]]


def run_height(h):
    m = 2 ** h
    ts = modes(h)

    def variable(i, s, x):
        return ('V', i, 'L' if i == h else s, x)

    def axes(row):
        def visit(i, p):
            b = 2 ** (h - i)
            if i == h:
                return [variable(i, 'L', p)]
            first, last = ('-', '+') if row else ('+', '-')
            a = [variable(i, first, x) for x in range(p*b, (p+1)*b)]
            c = [variable(i, last, x) for x in range(p*b, (p+1)*b)]
            return a + visit(i+1, 2*p) + visit(i+1, 2*p+1) + c
        anchors = [('A', t, j, x) for t in ts for j in range(2) for x in range(m)]
        dummy = [('D', x) for x in range(m)]
        tree = visit(0, 0)
        return anchors + (tree + dummy if row else dummy + tree)

    rows, cols = axes(True), axes(False)
    ri, ci = {r: i for i, r in enumerate(rows)}, {c: i for i, c in enumerate(cols)}
    assert len(rows) == len(set(rows)) == len(cols) == len(set(cols)) == (14*h+2)*m

    def node(v):
        return v[3] // 2 ** (h-v[1])

    def at(v, i, s):
        return v[0] == 'V' and v[1] == i and (i == h or v[2] == s)

    def role(t, group, v, row):
        i, k, s, d = t
        if v[0] == 'A':
            return False
        if v[0] == 'D':
            return (k == 'W' and group == 1) if row else (k == 'V' and group == 0)
        if k == 'V':
            if not row:
                return group == 1 and at(v, i-1, s)
            depth = (i if group == 0 else i-1) if s == '+' else (i-1 if group == 0 else i)
            return at(v, depth, s)
        if row:
            return group == 0 and at(v, i, s) and node(v) % 2 == d
        child = group == (1 if s == '+' else 0)
        return (at(v, i, s) and node(v) % 2 == d) if child else at(v, i-1, s)

    def entry(r, c):
        if r[0] == c[0] == 'A':
            return int(r[1] == c[1] and r[2] != c[2])
        if r[0] == 'A':
            return int(role(r[1], r[2], c, False))
        if c[0] == 'A':
            return int(role(c[1], c[2], r, True))
        if r[0] == 'D' or c[0] == 'D':
            return 1
        i, s, p = r[1], r[2], node(r)
        j, t, q = c[1], c[2], node(c)
        if i == j and s == t:
            return int(p < q) if s == '-' else int(p <= q)
        if i == j+1 and (s == 'L' or s == t):
            return int(p//2 < q) if t == '-' else int(p//2 <= q)
        return 0

    frequency, values = Counter(), Counter()
    frame_count = 0
    for z, u, v in product(range(m), repeat=3):
        def path(i, s, seed):
            b = 2 ** (h-i)
            return variable(i, s, (z//b)*b + seed % b)
        xp = [path(i, '+', u) for i in range(h+1)]
        xm = [path(i, '-', u) for i in range(h+1)]
        yp = [path(i, '+', v) for i in range(h+1)]
        ym = [path(i, '-', v) for i in range(h+1)]
        xd, yd = ('D', u), ('D', v)
        assert xp[-1] == xm[-1] and yp[-1] == ym[-1]
        assert entry(xp[0], yp[0]) == 1 and entry(xm[0], ym[0]) == 0
        guards = {(xp[0], yp[0]), (xm[0], ym[0])}
        for i in range(h+1):
            cells = {(xp[i], yd), (xm[i], yd), (xd, yp[i]), (xd, ym[i])}
            assert all(entry(r, c) == 1 for r, c in cells)
            guards.update(cells)
        for i in range(1, h+1):
            d = (z // 2 ** (h-i)) % 2
            frames = [((i, 'V', '+', None), xp[i], xp[i-1], yd, yp[i-1]),
                      ((i, 'V', '-', None), xm[i-1], xm[i], yd, ym[i-1]),
                      ((i, 'W', '+', d), xp[i], xd, yp[i-1], yp[i]),
                      ((i, 'W', '-', d), xm[i], xd, ym[i], ym[i-1])]
            for t, r0, r1, c0, c1 in frames:
                rs = [('A', t, 0, u), ('A', t, 1, u), r0, r1]
                cs = [('A', t, 0, v), ('A', t, 1, v), c0, c1]
                assert all(ri[rs[j]] < ri[rs[j+1]] for j in range(3))
                assert all(ci[cs[j]] < ci[cs[j+1]] for j in range(3))
                for a, b in product(range(4), repeat=2):
                    if a < 2 or b < 2:
                        assert entry(rs[a], cs[b]) == H[a][b], (h, z, u, v, t, a, b)
                        guards.add((rs[a], cs[b]))
                frame_count += 1
        for r, c in guards:
            protected = r[0] != 'V' or c[0] != 'V' or r[1] == c[1] == 0
            assert protected
            def chosen(p, seed):
                if p[0] == 'A':
                    return p[3] == seed
                if p[0] == 'D':
                    return p[1] == seed
                b = 2 ** (h-p[1])
                return p[3] == (z//b)*b + seed % b
            assert chosen(r, u) and chosen(c, v)
            frequency[r, c] += 1
            values[entry(r, c)] += 1
    assert max(frequency.values()) <= m
    # The unprotected common-leaf diagonal really has a larger event fiber.
    leaf_diagonal_frequency = sum(z == 0 for z, u, v in product(range(m), repeat=3))
    assert leaf_diagonal_frequency == m*m > m
    assert Fraction(2*m*((14*h+2)*m)**6, ((14*h+2)*m)**8) == Fraction(2, (14*h+2)**2*m)
    assert Fraction(m*m, ((14*h+2)*m)**2) == Fraction(1, (14*h+2)**2)
    return {'h': h, 'seeds': m**3, 'frames_checked': frame_count,
            'distinct_guard_cells': len(frequency), 'guard_incidences': sum(frequency.values()),
            'maximum_guard_frequency': max(frequency.values()), 'required_upper_bound': m,
            'zero_guard_incidences': values[0], 'one_guard_incidences': values[1],
            'unprotected_leaf_diagonal_frequency': leaf_diagonal_frequency}


if __name__ == '__main__':
    print(json.dumps({'python': platform.python_version(),
                      'scope': 'Finite source-independent host/sampler audit, not universal certification.',
                      'records': [run_height(h) for h in range(1, 5)]}, indent=2))
