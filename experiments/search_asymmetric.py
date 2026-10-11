#!/usr/bin/env python3
"""Explore a one-row/two-column anchor around the propagation body P.

The separation oracle uses actual ordered copies. A single-mode partial host
leaves all undesignated anchor incidences free. SAT search is finite evidence;
an independently checked UNSAT certificate is needed for a limitation theorem.
"""
import argparse
from collections import Counter
from dataclasses import asdict
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
from host import Position, nonanchors, nonanchor_entry, role
from search_three import find_copy


def patterns():
    for a, b, c, d, x, y, z, w in product((0, 1), repeat=8):
        yield [[a, b, c, d], [x, y, 1, 0], [z, w, 1, 1]]


def word(H):
    return ''.join(str(x) for row in H for x in row)


def body_entry(r, c, background=0):
    if r.kind == 'dummy' or c.kind == 'dummy':
        return 1
    supported = (r.depth == c.depth and r.sign == c.sign) or (
        r.depth == c.depth + 1 and r.sign in (c.sign, 'L'))
    return nonanchor_entry(r, c) if supported else background


def tree_trunk(axis, depth=3):
    return [x for x in nonanchors(depth+2, axis)
            if x.kind != 'variable' or x.depth <= depth]


def partial_host(H, mode, depth=3, background=0):
    rows = [Position('anchor', mode=mode, group=0, weight=2**(depth+2))] + tree_trunk('row', depth)
    cols = [Position('anchor', mode=mode, group=j, weight=2**(depth+2)) for j in range(2)] + tree_trunk('column', depth)
    fixed, free = [], []
    for i, r in enumerate(rows):
        line = []
        for j, c in enumerate(cols):
            if i == 0 and j < 2:
                bit = H[0][j]
            elif i == 0:
                k = role(c, mode, 'column')
                bit = H[0][k+1] if k else None
            elif j < 2:
                k = role(r, mode, 'row')
                bit = H[k][j] if k else None
            else:
                bit = body_entry(r, c, background)
            if bit is None:
                free.append((i, j))
            line.append(bit)
        fixed.append(line)
    return rows, cols, fixed, free


def distinct_copy(H, matrix):
    """No twin reuse: an UNSAT result can apply to arbitrary physical fills."""
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
        if len(js) == 4:
            return {'rows': list(ix), 'columns': js}
    return None


def solve_partial(H, mode, max_rounds=500, depth=3, background=0):
    import z3
    rows, cols, fixed, free = partial_host(H, mode, depth, background)
    variables = [z3.Bool('x'+str(k)) for k in range(len(free))]
    ids = {cell: k for k, cell in enumerate(free)}
    solver = z3.Solver()
    solver.set(timeout=10000)
    cuts = []
    start = time.monotonic()
    for step in range(max_rounds):
        result = solver.check()
        if result != z3.sat:
            return {'pattern': H, 'mode': mode, 'status': str(result),
                    'free_cells': free, 'cuts': cuts, 'seconds': time.monotonic()-start}
        model = solver.model()
        values = [int(z3.is_true(model.eval(x, model_completion=True))) for x in variables]
        matrix = [[v if v is not None else values[ids[i, j]] for j, v in enumerate(row)]
                  for i, row in enumerate(fixed)]
        witness = distinct_copy(H, matrix)
        if witness is None:
            return {'pattern': H, 'mode': mode, 'status': 'sat', 'free_cells': free,
                    'assignment': values, 'cuts': cuts, 'seconds': time.monotonic()-start}
        literals = {}
        for i, ri in enumerate(witness['rows']):
            for j, cj in enumerate(witness['columns']):
                if (ri, cj) in ids:
                    literals[ids[ri, cj]] = 1-H[i][j]
        clause = sorted((k+1 if bit else -k-1) for k, bit in literals.items())
        cuts.append({'witness': witness, 'clause': clause})
        solver.add(z3.Or(*[variables[k] if bit else z3.Not(variables[k])
                           for k, bit in literals.items()]))
    return {'pattern': H, 'mode': mode, 'status': 'round_limit', 'free_cells': free,
            'cuts': cuts, 'seconds': time.monotonic()-start}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    ap.add_argument('--max-rounds', type=int, default=500)
    ap.add_argument('--only', help='Twelve-bit pattern to focus on')
    ap.add_argument('--mode', choices=('plus', 'minus', 'vplus', 'vminus'), default='plus')
    ap.add_argument('--background', type=int, choices=(0, 1), default=0)
    args = ap.parse_args()
    rows, cols = tree_trunk('row'), tree_trunk('column')
    matrix = [[body_entry(r,c,args.background) for c in cols] for r in rows]
    screens, checks = [], []
    mode = {'plus': ('W', 2, '+', 0), 'minus': ('W', 2, '-', 0),
            'vplus': ('V', 2, '+', -1), 'vminus': ('V', 2, '-', -1)}[args.mode]
    for H in patterns():
        if args.only and word(H) != args.only:
            continue
        witness, count = find_copy(H, rows, cols, matrix)
        screens.append({'pattern': H, 'witness': witness, 'row_choices': count})
        if witness is not None:
            continue
        result = solve_partial(H, mode, args.max_rounds, background=args.background)
        checks.append(result)
        print(json.dumps({'pattern': word(H), 'status': result['status'],
                          'cuts': len(result['cuts']), 'seconds': round(result['seconds'], 3)}), flush=True)
    report = {'scope': 'Finite discovery; arbitrary unused anchor incidences in a single prescribed mode. No universal removal theorem.',
              'background': args.background,
              'nonanchor_rows': [asdict(x) for x in rows], 'nonanchor_columns': [asdict(x) for x in cols],
              'nonanchor_screen': screens, 'partial_completions': checks}
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'screened': len(screens), 'nonanchor_witnesses': sum(x['witness'] is not None for x in screens),
                      'completion_status': dict(Counter(x['status'] for x in checks))}), flush=True)


if __name__ == '__main__':
    main()
