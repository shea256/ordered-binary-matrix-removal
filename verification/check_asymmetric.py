#!/usr/bin/env python3
"""Independently check the uniform 3x4 template witness certificates.

Standard library only. Uses the earlier independent literal tree evaluator,
never the discovery code or SAT solver. This is not independent peer review.
"""
from collections import Counter
from itertools import product
import json
from math import comb, prod
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from check_three import anchor, body, dummy, key, role, var

ROOT = Path(__file__).resolve().parents[1]


def axis(levels, name):
    modes = ([('W', i, '-', p) for i in range(1, levels+1) for p in (0, 1)]
             + [('W', i, '+', p) for i in range(1, levels+1) for p in (0, 1)]
             + [('V', i, s, -1) for i in range(1, levels+1) for s in ('+', '-')])
    anchors = [anchor(t, j) for t in modes for j in range(1 if name == 'row' else 2)]
    tail = [var(i, s, p) for i in range(levels) for s in ('+', '-') for p in range(2**i)]
    tail.append(dummy())
    return anchors + sorted(tail, key=lambda x: key(x, name))


def weight(x, h, name):
    if x['kind'] == 'variable':
        return 2**(h-x['depth'])
    return 2**h * (2 if x['kind'] == 'anchor' and name == 'row' else 1)


def entry(r, c, H, fill, background):
    if r['kind'] == c['kind'] == 'anchor':
        j = c['group']
        return H[0][j] if r['mode'] == c['mode'] else fill[3+j]
    if r['kind'] == 'anchor':
        j = role(c, r['mode'], 'column')
        return H[0][j+1] if j else fill[2]
    if c['kind'] == 'anchor':
        i = role(r, c['mode'], 'row')
        return H[i][c['group']] if i else fill[c['group']]
    if r['kind'] == 'dummy' or c['kind'] == 'dummy':
        return 1
    supported = (r['depth'] == c['depth'] and r['sign'] == c['sign']) or (
        r['depth'] == c['depth']+1 and r['sign'] in (c['sign'], 'L'))
    return body(r, c) if supported else background


def decode(word):
    assert len(word) == 12 and set(word) <= {'0', '1'}
    return [[int(word[4*i+j]) for j in range(4)] for i in range(3)]


def main():
    cert = json.loads((ROOT/'verification/reference/asymmetric-template-certificates.json').read_text())
    assert (cert['schema'], cert['mode_levels'], cert['variable_depth_max'], cert['order']) == (1, 4, 3, 'global')
    assert cert['survivors'] == []
    fills = list(product((0, 1), repeat=5))
    assert cert['fills'] == [list(x) for x in fills]
    rows, cols = axis(4, 'row'), axis(4, 'column')
    patterns = {''.join(map(str, [a,b,c,d,x,y,1,0,z,w,1,1]))
                for a,b,c,d,x,y,z,w in product((0, 1), repeat=8)}
    expected = set(product((0, 1), patterns))
    seen, witnesses, min_counts = set(), 0, {}
    for record in cert['records']:
        identity = record['background'], record['pattern']
        assert identity in expected and identity not in seen
        seen.add(identity)
        H = decode(record['pattern'])
        covered = set()
        for witness in record['witnesses']:
            ix, jx = witness['rows'], witness['columns']
            assert len(ix) == 3 and len(jx) == 4
            assert ix == sorted(ix) and jx == sorted(jx)
            assert all(0 <= i < len(rows) for i in ix)
            assert all(0 <= j < len(cols) for j in jx)
            # Check block multiplicities, including repeated rows/columns.
            for h in (5, 6, 10):
                count = prod(comb(weight(positions[i], h, name), k)
                             for positions, indices, name in ((rows, ix, 'row'), (cols, jx, 'column'))
                             for i, k in Counter(indices).items())
                assert count >= (2**h//32)**7
                min_counts[h] = min(min_counts.get(h, count), count)
            matches = [f for f, fill in enumerate(fills)
                       if all(entry(rows[ri], cols[cj], H, fill, record['background']) == H[i][j]
                              for i, ri in enumerate(ix) for j, cj in enumerate(jx))]
            assert matches and matches == witness['fills']
            covered.update(matches)
            witnesses += 1
        assert covered == set(range(32))
    assert seen == expected
    print(json.dumps({'status': 'passed', 'patterns': len(patterns), 'backgrounds': 2,
                      'fills_per_pattern': 32, 'templates_covered': len(seen)*32,
                      'literal_witnesses': witnesses, 'mode_levels': 4, 'maximum_variable_depth': 3,
                      'minimum_witness_copy_counts_at_checked_depths': min_counts,
                      'all_depth_implication': 'See proofs/asymmetric-limitations.md; fixed witnesses persist for h >= 5.',
                      'scope': 'Uniform prefix-anchor template limitation at the inherited certified distance; no global 3x4 minimality.'}, indent=2))


if __name__ == '__main__':
    main()
