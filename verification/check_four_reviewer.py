#!/usr/bin/env python3
"""Separate-agent finite audit, independently transcribed from the written host.

This checks relaxed unbalanced configurations; it is neither a full H census
nor a universal theorem. It imports no code from the candidate package.
"""
from collections import Counter
import json


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


def audit(h):
    ts = modes(h)
    rs, cs = axis(h, True), axis(h, False)
    ri, ci = {x: i for i, x in enumerate(rs)}, {x: i for i, x in enumerate(cs)}
    rowroles = [supports(h, t, True) for t in ts]
    colroles = [supports(h, t, False) for t in ts]
    column_ones = {c: {r for r in rs if val(r, c)} for c in cs}
    later_rows = {r: set(rs[ri[r] + 1:]) for r in rs}
    def weight(x):
        return 2 ** h if x == ('dummy',) else 2 ** (h - x[0])
    support_pairs = 0
    for roles in (rowroles, colroles):
        for a, ss in enumerate(roles):
            assert not (ss[0] & ss[1])
            for b, tt in enumerate(roles):
                for s in ss:
                    for t in tt:
                        support_pairs += 1
                        assert not s & t or s <= t or t <= s
                        if s < t:
                            assert a < b, (h, ts[a], ts[b], s, t)

    # Check the exact earlier-support statement used at lines 327--329.
    minus_support_cases = 0
    for bi, (i, k, sign, d) in enumerate(ts):
        if k != 'W' or sign != '-' or i == h:
            continue
        own = {(i, '-', p) for p in range(2 ** i)}
        for ai in range(bi + 1):
            for group, support in enumerate(colroles[ai], 1):
                if support & own:
                    minus_support_cases += 1
                    j, ak, ass, e = ts[ai]
                    assert (j, ak, ass, group) == (i, 'W', '-', 1)
                    assert e <= d

    # Relax an unbalanced copy: retain the first two anchor rows, c1,
    # r3, c3, c4 and their H entries, plus K != dummy (derived from the
    # opposite r3 entries at c2,c3); omit c2 and r4 otherwise. Thus any
    # counterexample to localization here is at least a proof-obligation
    # witness, although it need not extend to a full H copy.
    configurations = Counter()
    full_families = Counter()
    complete_unbalanced = 0
    for bi, t in enumerate(ts):
        i, k, sign, d = t
        # The opposite group orientation always makes (r3,c4) one.
        for r in rowroles[bi][1]:
            for c4 in colroles[bi][0]:
                assert val(r, c4) == 1
        rrole, crole = rowroles[bi][0], colroles[bi][1]
        for ai in range(bi + 1):
            for group, support in enumerate(colroles[ai], 1):
                if ai == bi and group != 1:
                    continue  # Same mode forces first row into group 1.
                c3s = support - crole - {('dummy',)}
                c4s = crole - support
                for r in rrole:
                    ones = [c for c in c3s if val(r, c)]
                    if not ones:
                        continue
                    for c4 in c4s:
                        if val(r, c4):
                            continue
                        for c3 in ones:
                            if ci[c3] >= ci[c4]:
                                continue
                            configurations[k + sign] += 1
                            assert (k, sign, i) == ('W', '-', h), (h, t, ts[ai], r, c3, c4)
                            assert r[0] == h and c4 == (h - 1, '-', r[2] // 2)
                            assert c3[0] == h or c3[:2] == (h - 1, '+')
                            # Now restore c2 and every possible later r4.
                            for c2 in c3s:
                                if ci[c2] >= ci[c3] or val(r, c2):
                                    continue
                                possible_r4 = (later_rows[r] - rrole) & column_ones[c2] & column_ones[c3] & column_ones[c4]
                                for r4 in possible_r4:
                                    assert r4 == ('dummy',), (h, t, ts[ai], r, r4, c2, c3, c4)
                                    complete_unbalanced += 1
                                    if c3[0] == h:
                                        family = 'leaf_plus' if ts[ai][2] == '+' else 'leaf_minus'
                                    else:
                                        family = 'parent_full' if ts[ai][0] == h else 'parent_half'
                                    full_families[family] += (2 ** (3 * h)) * weight(r) * weight(r4) * weight(c2) * weight(c3) * weight(c4)
    m = 2 ** h
    total_unbalanced = sum(full_families.values())
    expected = 0 if h == 1 else (25 * m ** 6 - 58 * m ** 5) // 4
    assert total_unbalanced == expected, (h, total_unbalanced, expected)
    return {'h': h, 'role_support_pairs': support_pairs,
            'earlier_minus_support_cases': minus_support_cases,
            'relaxed_unbalanced_configurations': dict(configurations),
            'complete_unbalanced_quotient_configurations': complete_unbalanced,
            'weighted_unbalanced_families': dict(full_families),
            'weighted_unbalanced_total': total_unbalanced}


if __name__ == '__main__':
    print(json.dumps({'checks': [audit(h) for h in range(1, 8)],
                      'scope': 'Separate-agent finite support/localization audit; no full-copy census or universal certification.'}, indent=2))
