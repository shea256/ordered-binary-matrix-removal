#!/usr/bin/env python3
"""Fresh-reviewer rebuild and checks for the 3x3 crown candidate (proofs/three-by-three.md).

Written from the prose of Section 2 only. Imports no discovery, host, or checker
code from this track. Standard library only, except the optional ``--sat`` exact
repair-distance search, which needs ``python-sat``.

Checks (all depths 1..H):
  1. Host rebuild: n=(8h+2)2^h, entries from the written tables.
  2. Physical brute-force crown census at h<=3 (every ordered row triple of the
     actual n x n matrix) and collapsed-twin census at all depths; compared with 7m^4.
  3. Every copy matches the Section 5 classification (two families, 4m^4 + 3m^4).
  4. Section 3 facts: class node order, six order comparisons, class monotonicity,
     crossing-support configuration, per-class shape of U supports.
  5. Section 6 frame: for every path/mode the five anchor incidences and the dummy
     incidences equal the prescribed crown entries, with the stated row/column order.
  6. Optional: exact minimum crown repair distance by SAT with lazy copy clauses.

Finite outcomes support, but do not prove, the all-depth written theorem.
"""
import argparse
import json
import sys
import time
from itertools import combinations, product
from pathlib import Path

sys.dont_write_bytecode = True

K = ((0, 1, 1), (1, 0, 1), (1, 1, 0))


# ---------------------------------------------------------------- host rebuild
def mode_order(h):
    order = [('W', i, '-', e) for i in range(1, h + 1) for e in (0, 1)]
    order += [('W', i, '+', e) for i in range(1, h + 1) for e in (0, 1)]
    for i in range(1, h + 1):
        order += [('V', i, '+', None), ('V', i, '-', None)]
    return order


def variable_blocks(h, axis):
    out = []

    def visit(i, p):
        if i == h:
            out.append((h, 'L', p, 1))
            return
        first, last = ('-', '+') if axis == 'row' else ('+', '-')
        out.append((i, first, p, 2 ** (h - i)))
        visit(i + 1, 2 * p)
        visit(i + 1, 2 * p + 1)
        out.append((i, last, p, 2 ** (h - i)))

    visit(0, 0)
    return out


def row_labels(h):
    m = 2 ** h
    labels = []
    for t in mode_order(h):
        labels += [('X', t)] * m
    for (i, s, p, size) in variable_blocks(h, 'row'):
        labels += [('R', i, s, p)] * size
    return labels + [('Rdummy',)] * m


def col_labels(h):
    m = 2 ** h
    labels = [('Cdummy',)] * m
    for (i, s, p, size) in variable_blocks(h, 'column'):
        labels += [('C', i, s, p)] * size
    for t in mode_order(h):
        labels += [('Y', t)] * m
    return labels


def has_sign(label, sigma):
    return label[2] == sigma or label[2] == 'L'


def in_T(t, c, h):
    kind, i, sigma, e = t
    if c[0] == 'Cdummy':
        return kind == 'W'
    _, j, s, q = c
    if kind == 'V':
        return j == i - 1 and has_sign(c, sigma)
    if sigma == '+':
        return j == i and has_sign(c, '+') and q % 2 == e
    if j == i - 1 and has_sign(c, '-'):
        return True
    return e == 0 and i < h and j == i and has_sign(c, '-') and q % 2 == 1


def in_U(t, r, h):
    kind, i, sigma, e = t
    if r[0] == 'Rdummy':
        return kind == 'V'
    _, j, s, p = r
    if kind == 'V':
        return (j == i and has_sign(r, '+')) if sigma == '+' else (j == i - 1 and has_sign(r, '-'))
    return j == i and has_sign(r, sigma) and p % 2 == e


def variable_entry(r, c):
    _, i, s, p = r
    _, j, t, q = c
    if i == j and has_sign(r, '+') and has_sign(c, '+'):
        return int(p <= q)
    if i == j and r[2] == '-' and c[2] == '-':
        return int(p < q)
    if i == j + 1 and has_sign(r, '+') and c[2] == '+':
        return int(p // 2 <= q)
    if i == j + 1 and has_sign(r, '-') and c[2] == '-':
        return int(p // 2 < q)
    return 0


def entry(r, c, h):
    if r[0] == 'X' and c[0] == 'Y':
        return int(r[1] == c[1])
    if r[0] == 'X':
        return int(in_T(r[1], c, h))
    if c[0] == 'Y':
        return int(in_U(c[1], r, h))
    if r[0] == 'Rdummy' or c[0] == 'Cdummy':
        return 1
    return variable_entry(r, c)


def build(h):
    rows, cols = row_labels(h), col_labels(h)
    n = (8 * h + 2) * 2 ** h
    assert len(rows) == n == len(cols)
    cache = {}
    A = []
    for r in rows:
        line = []
        for c in cols:
            key = (r, c)
            if key not in cache:
                cache[key] = entry(r, c, h)
            line.append(cache[key])
        A.append(line)
    return A, rows, cols


# ---------------------------------------------------------------- census
def collapse(A, labels):
    keep, weights = [], []
    for k, line in enumerate(A):
        if keep and line == A[keep[-1]]:
            weights[-1] += 1
        else:
            keep.append(k)
            weights.append(1)
    kept = [A[k] for k in keep]
    assert len({tuple(l) for l in kept}) == len(kept), 'identical lines separated by a different line'
    return kept, weights, [labels[k] for k in keep]


def transpose(A):
    return [list(col) for col in zip(*A)]


def classify(h, r1, r2, r3, c1, c2, c3):
    if r2[0] != 'R' or r2[2] != 'L':
        return 'OTHER'
    p = r2[3]
    t = ('W', h, '-', p % 2)
    if r1 != ('X', t) or c3 != ('Y', t) or r3 != ('Rdummy',) or c2 != ('C', h - 1, '-', p // 2):
        return 'OTHER'
    if c1 == ('C', h - 1, '+', p // 2):
        return 'plus_parent_column'
    if c1[0] == 'C' and c1[2] == 'L' and c1[3] >= p and c1[3] // 2 == p // 2:
        return 'leaf_column'
    return 'OTHER'


def census(h, A, rw, cw, rlabels, clabels):
    n_r, n_c = len(A), len(A[0])
    masks = [sum(v << j for j, v in enumerate(line)) for line in A]
    full = (1 << n_c) - 1
    total, fam, bad = 0, {'plus_parent_column': 0, 'leaf_column': 0, 'OTHER': 0}, []
    for a, b, c in combinations(range(n_r), 3):
        x, y, z = masks[a], masks[b], masks[c]
        m1, m2, m3 = (full ^ x) & y & z, x & (full ^ y) & z, x & y & (full ^ z)
        if not (m1 and m2 and m3):
            continue
        cols1 = [j for j in range(n_c) if m1 >> j & 1]
        cols2 = [j for j in range(n_c) if m2 >> j & 1]
        cols3 = [j for j in range(n_c) if m3 >> j & 1]
        rowmult = rw[a] * rw[b] * rw[c]
        for j2 in cols2:
            for j1 in cols1:
                if j1 >= j2:
                    break
                for j3 in cols3:
                    if j3 <= j2:
                        continue
                    mult = rowmult * cw[j1] * cw[j2] * cw[j3]
                    total += mult
                    key = classify(h, rlabels[a], rlabels[b], rlabels[c], clabels[j1], clabels[j2], clabels[j3])
                    fam[key] += mult
                    if key == 'OTHER':
                        bad.append((rlabels[a], rlabels[b], rlabels[c], clabels[j1], clabels[j2], clabels[j3]))
    return total, fam, bad


def run_census(h, physical):
    A, rows, cols = build(h)
    if physical:
        return census(h, A, [1] * len(rows), [1] * len(cols), rows, cols)
    Aq, rw, rl = collapse(A, rows)
    AqT, cw, cl = collapse(transpose(Aq), cols)
    return census(h, transpose(AqT), rw, cw, rl, cl)


# ---------------------------------------------------------------- Section 3 facts
def check_section3(h):
    A, rows, cols = build(h)
    rpos, cpos = {}, {}
    for k, l in enumerate(rows):
        rpos.setdefault(l, k)
    for k, l in enumerate(cols):
        cpos.setdefault(l, k)
    pi = lambda p: p // 2
    R = lambda i, s, p: rpos[('R', i, 'L' if i == h else s, p)]
    C = lambda i, s, q: cpos[('C', i, 'L' if i == h else s, q)]
    for i in range(h + 1):
        for s in (['L'] if i == h else ['+', '-']):
            for p in range(2 ** i - 1):
                assert R(i, s, p) < R(i, s, p + 1) and C(i, s, p) < C(i, s, p + 1)
    for i in range(1, h + 1):
        for q in range(2 ** i):
            for a in range(2 ** (i - 1)):
                for sigma in (['L'] if i == h else ['+', '-']):
                    assert (C(i - 1, '+', a) < C(i, sigma, q)) == (a <= pi(q))
                    assert (C(i, sigma, q) < C(i - 1, '-', a)) == (pi(q) <= a)
                    assert (C(i - 1, '-', a) < C(i, sigma, q)) == (a < pi(q))
                    assert (R(i, '+', q) < R(i - 1, '+', a)) == (pi(q) <= a)
                    assert (R(i - 1, '-', a) < R(i, '-', q)) == (a <= pi(q))
    for j in range(h):
        for a in range(2 ** j):
            for b in range(2 ** j):
                assert (C(j, '+', a) < C(j, '-', b)) == (a <= b)
    classes_c, classes_r = {}, {}
    for (i, s, q, _) in variable_blocks(h, 'column'):
        classes_c.setdefault((i, s), []).append(cpos[('C', i, s, q)])
    for (i, s, p, _) in variable_blocks(h, 'row'):
        classes_r.setdefault((i, s), []).append(rpos[('R', i, s, p)])
    for r in (k for k, l in enumerate(rows) if l[0] != 'X'):
        for cl in classes_c.values():
            vals = [A[r][c] for c in cl]
            assert vals == sorted(vals)
    for c in (k for k, l in enumerate(cols) if l[0] != 'Y'):
        for cl in classes_r.values():
            vals = [A[r][c] for r in cl]
            assert vals == sorted(vals, reverse=True)
    modes = mode_order(h)
    varcols = [l for l in dict.fromkeys(cols) if l[0] == 'C']
    T = {t: {c for c in varcols if in_T(t, c, h)} for t in modes}
    crossings = 0
    for ia, ib in combinations(range(len(modes)), 2):
        a, b = modes[ia], modes[ib]
        inter, onlya, onlyb = T[a] & T[b], T[a] - T[b], T[b] - T[a]
        if not (inter and onlya and onlyb):
            continue
        found = False
        for u, v, w in product(onlyb, onlya, inter):
            if cpos[u] < cpos[v] < cpos[w]:
                found = True
                i = a[1]
                assert a == ('W', i, '-', 0) and i < h, (a, b)
                assert b in (('W', i + 1, '-', 0), ('W', i + 1, '-', 1), ('V', i + 1, '-', None)), (a, b)
                assert v[1:3] == (i - 1, '-'), v
                assert w[1:3] == (i, '-') and w[3] % 2 == 1, w
                assert (u[1:3] == (i, '-') and u[3] % 2 == 0) or (
                    b == ('W', i + 1, '-', 0) and i + 1 < h and u[1:3] == (i + 1, '-') and u[3] % 2 == 1), u
        crossings += found
    varrows = [l for l in dict.fromkeys(rows) if l[0] == 'R']
    for t in modes:
        for (i, s) in classes_r:
            cl = [l for l in varrows if l[1] == i and l[2] == s]
            inside = [l for l in cl if in_U(t, l, h)]
            if inside and len(inside) != len(cl):
                assert len({l[3] % 2 for l in inside}) == 1 and 2 * len(inside) == len(cl), (t, i, s)
    return crossings


# ---------------------------------------------------------------- Section 6 frames
def check_frames(h):
    """For each leaf path and each mode, the crown frame rows (X_t, r1, r2) / columns
    (c1, c2, Y_t) are ordered and the anchor- and dummy-incident entries match K."""
    rows, cols = row_labels(h), col_labels(h)
    rpos, cpos = {}, {}
    for k, l in enumerate(rows):
        rpos.setdefault(l, k)
    for k, l in enumerate(cols):
        cpos.setdefault(l, k)

    def Rb(i, s, p):
        return ('R', i, 'L' if i == h else s, p)

    def Cb(i, s, q):
        return ('C', i, 'L' if i == h else s, q)

    frames = 0
    for z in range(2 ** h):
        node = lambda i: z >> (h - i)
        for i in range(1, h + 1):
            p, a, e = node(i), node(i - 1), node(i) % 2
            items = [(('V', i, '+', None), Rb(i, '+', p), Rb(i - 1, '+', a), ('Cdummy',), Cb(i - 1, '+', a)),
                     (('V', i, '-', None), Rb(i - 1, '-', a), Rb(i, '-', p), ('Cdummy',), Cb(i - 1, '-', a)),
                     (('W', i, '+', e), Rb(i, '+', p), ('Rdummy',), Cb(i - 1, '+', a), Cb(i, '+', p)),
                     (('W', i, '-', e), Rb(i, '-', p), ('Rdummy',), Cb(i, '-', p), Cb(i - 1, '-', a))]
            for t, r1, r2, c1, c2 in items:
                rs, cs = [('X', t), r1, r2], [c1, c2, ('Y', t)]
                assert rpos[rs[0]] < rpos[rs[1]] < rpos[rs[2]], (t, rs)
                assert cpos[cs[0]] < cpos[cs[1]] < cpos[cs[2]], (t, cs)
                for j, k in product(range(3), repeat=2):
                    anchor_or_dummy = j == 0 or k == 2 or rs[j][0] == 'Rdummy' or cs[k][0] == 'Cdummy'
                    if anchor_or_dummy:
                        assert entry(rs[j], cs[k], h) == K[j][k], (t, rs, cs, j, k)
                frames += 1
    # root cells
    assert entry(Rb(0, '+', 0), Cb(0, '+', 0), h) == 1 and entry(Rb(0, '-', 0), Cb(0, '-', 0), h) == 0
    return frames


# ---------------------------------------------------------------- optional SAT
def min_repair_sat(h, budgets):
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Cadical153
    A, rows, cols = build(h)
    n = len(A)
    var = lambda r, c: r * n + c + 1

    def find_copies(B, limit=200):
        masks = [sum(v << j for j, v in enumerate(line)) for line in B]
        full = (1 << n) - 1
        out = []
        for a, b, c in combinations(range(n), 3):
            x, y, z = masks[a], masks[b], masks[c]
            m1, m2, m3 = (full ^ x) & y & z, x & (full ^ y) & z, x & y & (full ^ z)
            if not (m1 and m2 and m3):
                continue
            c1s = [j for j in range(n) if m1 >> j & 1]
            c2s = [j for j in range(n) if m2 >> j & 1]
            c3s = [j for j in range(n) if m3 >> j & 1]
            for j2 in c2s:
                for j1 in c1s:
                    if j1 >= j2:
                        break
                    for j3 in c3s:
                        if j3 > j2:
                            out.append(((a, b, c), (j1, j2, j3)))
                            if len(out) >= limit:
                                return out
                            break
        return out

    results = []
    for budget in budgets:
        t0 = time.time()
        clauses, top, dvars = [], n * n, []
        for r in range(n):
            for c in range(n):
                top += 1
                dvars.append(top)
                x = var(r, c)
                if A[r][c] == 1:
                    clauses += [[-top, -x], [top, x]]
                else:
                    clauses += [[-top, x], [top, -x]]
        card = CardEnc.atmost(lits=dvars, bound=budget, top_id=top, encoding=EncType.seqcounter)
        solver = Cadical153(bootstrap_with=clauses + card.clauses)
        rounds, edits = 0, None
        while True:
            if not solver.solve():
                break
            model = solver.get_model()
            B = [[1 if model[var(r, c) - 1] > 0 else 0 for c in range(n)] for r in range(n)]
            rounds += 1
            copies = find_copies(B)
            if not copies:
                edits = [(rows[r], cols[c], A[r][c]) for r in range(n) for c in range(n) if B[r][c] != A[r][c]]
                break
            for rs, cs in copies:
                solver.add_clause([-var(rs[i], cs[j]) if K[i][j] else var(rs[i], cs[j])
                                   for i in range(3) for j in range(3)])
        solver.delete()
        rec = {'h': h, 'n': n, 'budget': budget, 'rounds': rounds, 'seconds': round(time.time() - t0, 1),
               'result': 'UNSAT' if edits is None else 'SAT', 'edits': None if edits is None else [list(map(str, e)) for e in edits]}
        results.append(rec)
        print(json.dumps(rec), flush=True)
        if edits is not None:
            break
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-depth', type=int, default=6)
    ap.add_argument('--physical-depth', type=int, default=3)
    ap.add_argument('--sat', action='store_true', help='exact repair distance at h=1 (0..4) and h=2 (15,16); needs python-sat')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    records = []
    for h in range(1, args.max_depth + 1):
        t0 = time.time()
        m = 2 ** h
        total, fam, bad = run_census(h, physical=False)
        rec = {'h': h, 'n': (8 * h + 2) * m, 'copies': total, 'claimed': 7 * m ** 4,
               'families': {k: v for k, v in fam.items() if k != 'OTHER'}, 'noncanonical': len(bad)}
        if h <= args.physical_depth:
            ptotal, pfam, pbad = run_census(h, physical=True)
            rec['physical_copies'] = ptotal
            assert ptotal == total and pfam == fam and not pbad
        rec['crossing_mode_pairs'] = check_section3(h)
        rec['frames'] = check_frames(h)
        rec['seconds'] = round(time.time() - t0, 1)
        assert total == 7 * m ** 4 and not bad
        assert fam['plus_parent_column'] == 4 * m ** 4 and fam['leaf_column'] == 3 * m ** 4
        assert rec['frames'] == 4 * h * m
        records.append(rec)
        print(json.dumps(rec), flush=True)
    report = {'status': 'passed', 'pattern': K, 'records': records,
              'scope': 'Fresh-reviewer rebuild from the written host specification; finite checks only, '
                       'not a Lean certificate or human peer review.'}
    if args.sat:
        report['exact_repair_distance'] = min_repair_sat(1, range(0, 5)) + min_repair_sat(2, [15, 16])
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'max_depth': args.max_depth, 'sat': args.sat}))


if __name__ == '__main__':
    main()
