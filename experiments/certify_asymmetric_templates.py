#!/usr/bin/env python3
"""Find a compact covering set of literal copies for uniform 3x4 templates.

Each witness may cover several of the 32 fills. This is certificate discovery;
verification/check_asymmetric.py independently rebuilds and checks its output.
"""
import argparse
from itertools import product
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from search_asymmetric import patterns, word
from search_asymmetric_templates import axes, value
from search_three import find_copy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    rows, cols = axes(4, 'row'), axes(4, 'column')
    fills = list(product((0, 1), repeat=5))
    records, survivors = [], []
    for background in (0, 1):
        for H in patterns():
            covered, witnesses = set(), []
            for f, fill in enumerate(fills):
                if f in covered:
                    continue
                A = [[value(r, c, H, fill, background) for c in cols] for r in rows]
                witness, _ = find_copy(H, rows, cols, A)
                if witness is None:
                    survivors.append({'background': background, 'pattern': word(H), 'fill': fill})
                    continue
                matches = [k for k, other in enumerate(fills)
                           if all(value(rows[ri], cols[cj], H, other, background) == H[i][j]
                                  for i, ri in enumerate(witness['rows'])
                                  for j, cj in enumerate(witness['columns']))]
                covered.update(matches)
                witnesses.append(dict(witness, fills=matches))
            records.append({'background': background, 'pattern': word(H), 'witnesses': witnesses})
        print(json.dumps({'background': background, 'survivors': len(survivors),
                          'witnesses': sum(len(x['witnesses']) for x in records)}), flush=True)
    report = {'schema': 1, 'mode_levels': 4, 'variable_depth_max': 3,
              'order': 'global', 'fills': fills, 'records': records, 'survivors': survivors}
    Path(args.output).write_text(json.dumps(report, separators=(',', ':'))+'\n')
    if survivors:
        raise SystemExit('Some templates have no certificate in this trunk.')


if __name__ == '__main__':
    main()
