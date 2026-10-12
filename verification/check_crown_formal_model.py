#!/usr/bin/env python3
"""Compare executed Lean host/order definitions with the literal Python model.

This is a finite semantic cross-check, separate from the all-depth Lean proof.
The Lean host doubles each anchor block, but leaves the body and dummies intact.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
import check_three_by_three as literal

ROOT = Path(__file__).resolve().parents[1]


def decode(code, h):
    m = 2**h
    if code[0] == 0:
        _, t, g, x = code
        i, k = t//6+1, t % 6
        mode = ('V', i, '+' if k == 0 else '-', -1) if k < 2 else (
            'W', i, '+' if k < 4 else '-', k % 2)
        return (('A', mode), g*m+x)
    if code[0] == 1:
        _, cls, x = code
        i = cls//2
        width = 2**(h-i)
        return (('B', i, 'L' if i == h else ('+' if cls % 2 == 0 else '-'),
                 x//width), x % width)
    assert code[0] == 2
    return (('D',), code[1])


def expected_axis(h, name):
    return [(block, offset) for block in literal.axes(h, name)
            for offset in range(literal.weight(block, h)*(2 if block[0] == 'A' else 1))]


def count_crowns(matrix):
    n = len(matrix)
    masks = [sum(bit << j for j, bit in enumerate(row)) for row in matrix]
    full, count = (1 << n)-1, 0
    for i, j, k in combinations(range(n), 3):
        r, s, t = masks[i], masks[j], masks[k]
        a, b, c = (full ^ r) & s & t, r & (full ^ s) & t, r & s & (full ^ t)
        if not (a and b and c):
            continue
        # Sum the number of left/right choices for every possible middle column.
        while b:
            middle = b & -b
            b ^= middle
            count += bin(a & (middle-1)).count('1') * bin(c & ~(2*middle-1)).count('1')
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = subprocess.run(['lake', 'env', 'lean', '../verification/export_crown_host.lean'],
                            cwd=ROOT/'formal', text=True, capture_output=True)
    if result.returncode:
        print(result.stdout, end='')
        print(result.stderr, end='', file=sys.stderr)
    result.check_returncode()
    exported = [json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
    assert [item['h'] for item in exported] == [0, 1, 2, 3]
    records = []
    for item in exported:
        h = item['h']
        rows = [decode(p, h) for p in item['rows']]
        cols = [decode(p, h) for p in item['columns']]
        assert rows == expected_axis(h, 'row')
        assert cols == expected_axis(h, 'column')
        n = len(rows)
        assert n == len(cols) == (14*h+2)*2**h
        matrix = item['entries']
        assert len(matrix) == n and all(len(row) == n for row in matrix)
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                assert matrix[i][j] == literal.entry(r[0], c[0]), (h, i, j, r, c)
        record = {'h': h, 'n': n, 'entries_checked': n*n, 'both_axis_orders_match': True}
        if h <= 2:
            copies = count_crowns(matrix)
            assert copies == (0 if h == 0 else 28*2**(4*h))
            record['physically_enumerated_copies'] = copies
        records.append(record)
        print(json.dumps(record), flush=True)
    paths = [Path(__file__), ROOT/'verification/export_crown_host.lean',
             ROOT/'verification/check_three_by_three.py',
             ROOT/'formal/OrderedRemoval/Crown/Host.lean',
             ROOT/'formal/OrderedRemoval/Crown/OrderedHost.lean']
    report = {'status': 'passed', 'scope': 'Finite same-agent Lean/Python semantic cross-check; '
              'the all-depth theorem is certified separately.',
              'records': records, 'export_sha256': hashlib.sha256(result.stdout.encode()).hexdigest(),
              'sources': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in paths}}
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
