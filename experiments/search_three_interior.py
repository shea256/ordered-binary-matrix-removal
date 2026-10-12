#!/usr/bin/env python3
"""Exact discovery for one-anchor 3x3 frames with interior placements.

The nonanchor body and mode roles are inherited. An anchor may occupy any
gap among persistent nonleaf blocks, provided all prescribed role blocks
have their designated order relative to it. This is a restricted family,
not a search over every ordered-matrix removal construction.
"""
import argparse
from dataclasses import asdict
from itertools import combinations, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from host import Position, nonanchors, nonanchor_entry, role
from search_three import find_copy


def trunk(name, depth=3):
    return [x for x in nonanchors(depth + 2, name)
            if x.kind != 'variable' or x.depth <= depth]


def encodings():
    for ar, ac in product(range(3), repeat=2):
        ri, ci = [i for i in range(3) if i != ar], [j for j in range(3) if j != ac]
        for border in product((0, 1), repeat=5):
            H = [[None] * 3 for _ in range(3)]
            for i, row in enumerate(((1, 0), (1, 1))):
                for j, bit in enumerate(row):
                    H[ri[i]][ci[j]] = bit
            for (i, j), bit in zip([(ar, j) for j in range(3)] + [(i, ac) for i in ri], border):
                H[i][j] = bit
            yield {'anchor_row': ar, 'anchor_column': ac,
                   'pattern': ''.join(str(b) for row in H for b in row)}


def decode(word):
    return [[int(b) for b in word[i:i+3]] for i in (0, 3, 6)]


def gaps(xs, mode, name, slot):
    """All projected block gaps consistent with whole role incidences."""
    return [g for g in range(len(xs) + 1)
            if all(not (k := role(x, mode, name)) or ((i < g) == (k <= slot))
                   for i, x in enumerate(xs))]


def screen(depth=3):
    rows, cols = trunk('row', depth), trunk('column', depth)
    matrix = [[nonanchor_entry(r, c) for c in cols] for r in rows]
    cache, cases = {}, []
    modes = [('V', 2, '+', -1), ('V', 2, '-', -1),
             ('W', 2, '+', 0), ('W', 2, '+', 1),
             ('W', 2, '-', 0), ('W', 2, '-', 1)]
    for e in encodings():
        word = e['pattern']
        if word not in cache:
            cache[word] = find_copy(decode(word), rows, cols, matrix)[0]
        item = dict(e, nonanchor_witness=cache[word])
        if cache[word] is None:
            item['placements'] = [{'mode': t,
                'row_gaps': gaps(rows, t, 'row', e['anchor_row']),
                'column_gaps': gaps(cols, t, 'column', e['anchor_column'])}
                for t in modes]
        cases.append(item)
    return {'scope': 'Finite exact discovery; arbitrary-depth implications require the written lifting argument.',
            'depth': depth, 'rows': [asdict(x) for x in rows],
            'columns': [asdict(x) for x in cols], 'cases': cases}


def frame(e, mode, row_gap, column_gap, depth=3):
    rows, cols = trunk('row', depth), trunk('column', depth)
    a = Position('anchor', mode=tuple(mode), group=0, weight=2**(depth+2))
    rows.insert(row_gap, a)
    cols.insert(column_gap, a)
    H = decode(e['pattern'])
    ar, ac = e['anchor_row'], e['anchor_column']
    ri, ci = [i for i in range(3) if i != ar], [j for j in range(3) if j != ac]
    fixed, free = [], []
    for i, r in enumerate(rows):
        line = []
        for j, c in enumerate(cols):
            if r.kind == c.kind == 'anchor':
                v = H[ar][ac]
            elif r.kind == 'anchor':
                k = role(c, mode, 'column')
                v = H[ar][ci[k-1]] if k else None
            elif c.kind == 'anchor':
                k = role(r, mode, 'row')
                v = H[ri[k-1]][ac] if k else None
            else:
                v = nonanchor_entry(r, c)
            if v is None:
                free.append((i, j))
            line.append(v)
        fixed.append(line)
    return rows, cols, fixed, free


def distinct_copy(H, matrix):
    full = (1 << len(matrix[0])) - 1
    masks = [sum(bit << j for j, bit in enumerate(row)) for row in matrix]
    for ix in combinations(range(len(matrix)), 3):
        js, start = [], 0
        for signature in zip(*H):
            mask = full
            for i, bit in zip(ix, signature):
                mask &= masks[i] if bit else full ^ masks[i]
            mask = (mask >> start) << start
            if not mask:
                break
            j = (mask & -mask).bit_length() - 1
            js.append(j)
            start = j + 1
        if len(js) == 3:
            return {'rows': list(ix), 'columns': js}
    return None


def solve(e, mode, row_gap, column_gap, depth=3, max_rounds=1000):
    import z3
    _, _, fixed, free = frame(e, mode, row_gap, column_gap, depth)
    ids = {tuple(ij): k for k, ij in enumerate(free)}
    variables = [z3.Bool('x' + str(k)) for k in range(len(free))]
    solver = z3.Solver()
    solver.set(timeout=10000)
    cuts = []
    H = decode(e['pattern'])
    for step in range(max_rounds):
        status = solver.check()
        if status != z3.sat:
            if status == z3.unsat:
                core = {str(x) for x in solver.unsat_core()}
                cuts = [c for i, c in enumerate(cuts) if 'cut' + str(i) in core]
            return {'status': str(status), 'cuts': cuts, 'rounds': step}
        model = solver.model()
        assignment = [int(z3.is_true(model.eval(v, model_completion=True))) for v in variables]
        A = [[v if v is not None else assignment[ids[i, j]] for j, v in enumerate(row)]
             for i, row in enumerate(fixed)]
        witness = distinct_copy(H, A)
        if witness is None:
            return {'status': 'sat', 'assignment': assignment, 'rounds': step}
        literals = {ids[ri, cj]: 1-H[i][j]
                    for i, ri in enumerate(witness['rows'])
                    for j, cj in enumerate(witness['columns']) if (ri, cj) in ids}
        clause = sorted(k+1 if bit else -k-1 for k, bit in literals.items())
        cuts.append(dict(witness, clause=clause))
        solver.assert_and_track(z3.Or(*[variables[k] if bit else z3.Not(variables[k])
                                       for k, bit in literals.items()]), z3.Bool('cut'+str(step)))
    return {'status': 'round_limit', 'rounds': max_rounds}


def complete(report):
    """A single mode excluding every legal gap suffices to reject a frame."""
    for e in report['cases']:
        if e['nonanchor_witness'] is not None:
            e['classification'] = 'nonanchor_copy'
            continue
        bad = next((p for p in e['placements'] if not p['row_gaps'] or not p['column_gaps']), None)
        if bad is not None:
            e['classification'] = 'incompatible_role_order'
            e['blocking_mode'] = bad['mode']
            continue
        trials = []
        for placement in sorted(e['placements'], key=lambda p: len(p['row_gaps'])*len(p['column_gaps'])):
            cases = []
            for rg, cg in product(placement['row_gaps'], placement['column_gaps']):
                result = solve(e, placement['mode'], rg, cg, report['depth'])
                cases.append(dict(result, row_gap=rg, column_gap=cg))
            trials.append({'mode': placement['mode'], 'cases': cases})
            if all(c['status'] == 'unsat' for c in cases):
                e['classification'] = 'forced_copy'
                e['obstruction'] = trials[-1]
                break
        else:
            e['classification'] = 'survives_single_mode_screen'
        e['search_trials'] = trials
        print(json.dumps({k: e[k] for k in ('anchor_row', 'anchor_column', 'pattern', 'classification')},
                         sort_keys=True), flush=True)
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--depth', type=int, default=3)
    ap.add_argument('--output', required=True)
    ap.add_argument('--complete', action='store_true')
    args = ap.parse_args()
    report = screen(args.depth)
    if args.complete:
        report = complete(report)
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n')
    survivors = [c for c in report['cases'] if c['nonanchor_witness'] is None]
    feasible = [c for c in survivors if all(p['row_gaps'] and p['column_gaps'] for p in c['placements'])]
    print(json.dumps({'encodings': len(report['cases']), 'nonanchor_exceptions': len(survivors),
                      'placement_feasible_exceptions': len(feasible),
                      'survivors': [{k: e[k] for k in ('anchor_row', 'anchor_column', 'pattern')}
                                    for e in feasible]}, indent=2))


if __name__ == '__main__':
    main()
