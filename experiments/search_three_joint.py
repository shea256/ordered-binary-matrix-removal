#!/usr/bin/env python3
"""Joint CEGAR search over Boolean entries and total anchor orders.

All nonanchor blocks keep their original orders. Anchor blocks can move
independently between them and can appear in any relative order. Copies
use distinct blocks; UNSAT therefore remains meaningful with nonuniform
physical fills after a separate certificate and averaging argument.
"""
import argparse
from dataclasses import asdict
from itertools import combinations
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
from host import Position, modes, nonanchors, nonanchor_entry, role
from search_three_interior import decode, distinct_copy, trunk


def simplify(clause):
    if any(x is True for x in clause):
        return None
    out = {x for x in clause if x is not False}
    if any(-x in out for x in out):
        return None
    return sorted(out)


def neg(x):
    return not x if isinstance(x, bool) else -x


def problem(e, ts, depth=3, full=False):
    axes = {name: (nonanchors(depth, name) if full else trunk(name, depth))
            + [Position('anchor', mode=tuple(t), group=0,
                weight=2**(depth if full else depth+2)) for t in ts] for name in ('row', 'column')}
    H = decode(e['pattern'])
    ar, ac = e['anchor_row'], e['anchor_column']
    ri, ci = [i for i in range(3) if i != ar], [j for j in range(3) if j != ac]
    variables = []
    def fresh(description):
        variables.append(description)
        return len(variables)
    matrix = []
    for i, r in enumerate(axes['row']):
        line = []
        for j, c in enumerate(axes['column']):
            if r.kind == c.kind == 'anchor':
                v = bool(H[ar][ac]) if r.mode == c.mode else None
            elif r.kind == 'anchor':
                k = role(c, r.mode, 'column')
                v = bool(H[ar][ci[k-1]]) if k else None
            elif c.kind == 'anchor':
                k = role(r, c.mode, 'row')
                v = bool(H[ri[k-1]][ac]) if k else None
            else:
                v = bool(nonanchor_entry(r, c))
            line.append(fresh({'entry': [i, j]}) if v is None else v)
        matrix.append(line)
    orders, clauses = {}, []
    for name, xs in axes.items():
        slot = ar if name == 'row' else ac
        table = [[False]*len(xs) for _ in xs]
        for i, j in combinations(range(len(xs)), 2):
            a, b = xs[i], xs[j]
            if a.kind != 'anchor' and b.kind != 'anchor':
                v = True
            elif a.kind != 'anchor' and (k := role(a, b.mode, name)):
                v = k <= slot
            else:
                v = fresh({'order': [name, i, j]})
            table[i][j], table[j][i] = v, neg(v)
        for i, j, k in combinations(range(len(xs)), 3):
            for literals in ((neg(table[i][j]), neg(table[j][k]), table[i][k]),
                             (table[i][j], table[j][k], neg(table[i][k]))):
                clause = simplify(literals)
                if clause is not None:
                    clauses.append(clause)
        orders[name] = table
    return axes, variables, matrix, orders, clauses


def copy_clause(H, witness, matrix, orders):
    rs, cs = witness['rows'], witness['columns']
    literals = [neg(matrix[r][c]) if H[i][j] else matrix[r][c]
                for i, r in enumerate(rs) for j, c in enumerate(cs)]
    for name, xs in (('row', rs), ('column', cs)):
        literals += [neg(orders[name][a][b]) for a, b in zip(xs, xs[1:])]
    return simplify(literals)


def unlocalized_copy(H, matrix, rows, cols, zero_row, h):
    """Find a copy whose designated body zero is outside the terminal set."""
    full = (1 << len(cols)) - 1
    masks = [sum(bit << j for j, bit in enumerate(line)) for line in matrix]
    for ix in combinations(range(len(rows)), 3):
        js, start = [], 0
        for stage, signature in enumerate(zip(*H)):
            mask = full
            for i, bit in zip(ix, signature):
                mask &= masks[i] if bit else full ^ masks[i]
            if stage == 1:
                r = rows[ix[zero_row]]
                if r.kind == 'variable' and r.sign == 'L':
                    for j, c in enumerate(cols):
                        if c.kind == 'variable' and c.sign == '-' and c.depth == h-1 and c.node == r.node//2:
                            mask &= ~(1 << j)
            mask = (mask >> start) << start
            if not mask:
                break
            j = (mask & -mask).bit_length()-1
            js.append(j)
            start = j+1
        if len(js) == 3:
            return {'rows': list(ix), 'columns': js}
    return None


def run(e, ts, depth=3, max_rounds=2000, full=False):
    import z3
    axes, descriptions, matrix, orders, base = problem(e, ts, depth, full)
    H = decode(e['pattern'])
    vs = [z3.Bool('v'+str(k+1)) for k in range(len(descriptions))]
    solver = z3.Solver()
    solver.set(timeout=20000)
    def add(clause, label):
        solver.assert_and_track(z3.Or(*[vs[abs(lit)-1] if lit > 0 else z3.Not(vs[abs(lit)-1])
                                       for lit in clause]), z3.Bool(label))
    for i, clause in enumerate(base):
        add(clause, 'b'+str(i))
    cuts = []
    start = time.monotonic()
    result = {'encoding': e, 'modes': ts, 'depth': depth,
              'variables': len(vs), 'base_clauses': len(base), 'solver': z3.get_version_string(),
              'full': full, 'scope': 'Finite completion; not an all-depth theorem or a repair-distance certificate.'}
    for step in range(max_rounds):
        status = solver.check()
        if status != z3.sat:
            result.update(status=str(status), rounds=step, seconds=time.monotonic()-start)
            if status == z3.unsat:
                core = {str(v) for v in solver.unsat_core()}
                result['base_core'] = [i for i in range(len(base)) if 'b'+str(i) in core]
                result['cuts'] = [c for i, c in enumerate(cuts) if 'c'+str(i) in core]
            return result
        model = solver.model()
        assignment = [bool(z3.is_true(model.eval(v, model_completion=True))) for v in vs]
        def value(v):
            return v if isinstance(v, bool) else assignment[v-1] if v>0 else not assignment[-v-1]
        perms = {}
        for name, xs in axes.items():
            perms[name] = sorted(range(len(xs)), key=lambda i: sum(value(v) for v in orders[name][i]), reverse=True)
            assert all(value(orders[name][a][b]) for a, b in combinations(perms[name], 2))
        A = [[int(value(matrix[r][c])) for c in perms['column']] for r in perms['row']]
        witness = (unlocalized_copy(H, A, [axes['row'][i] for i in perms['row']],
                     [axes['column'][j] for j in perms['column']],
                     1 if e['anchor_row']==0 else 0, depth) if full else distinct_copy(H, A))
        if witness is None:
            result.update(status='sat', rounds=step, seconds=time.monotonic()-start,
                          assignment=[int(x) for x in assignment], permutations=perms)
            return result
        witness = {'rows': [perms['row'][i] for i in witness['rows']],
                   'columns': [perms['column'][j] for j in witness['columns']]}
        clause = copy_clause(H, witness, matrix, orders)
        assert clause is not None
        cuts.append(dict(witness, clause=clause))
        add(clause, 'c'+str(step))
        if step and step % 100 == 0:
            print(json.dumps({'pattern': e['pattern'], 'round': step,
                              'seconds': round(time.monotonic()-start, 2)}), flush=True)
    result.update(status='round_limit', rounds=max_rounds, seconds=time.monotonic()-start)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pattern', choices=('011101110', '101110011'), required=True)
    ap.add_argument('--levels', type=int, default=2)
    ap.add_argument('--depth', type=int, default=3)
    ap.add_argument('--modes', help='JSON list of modes, overriding levels')
    ap.add_argument('--max-rounds', type=int, default=2000)
    ap.add_argument('--full', action='store_true', help='Include leaves and permit copies with the localized body zero')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    e = {'pattern': args.pattern, 'anchor_row': 0 if args.pattern == '011101110' else 2, 'anchor_column': 2}
    ts = json.loads(args.modes) if args.modes else modes(args.levels)
    result = run(e, ts, args.depth, args.max_rounds, args.full)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('assignment', 'permutations', 'cuts', 'base_core')}, indent=2))


if __name__ == '__main__':
    main()
