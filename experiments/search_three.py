#!/usr/bin/env python3
"""Exact 3x3 screen in fixed-depth trunks of the current tree host.

This searches occurrences of all 512 patterns in a particular host, not
all possible removal constructions. Repeated twin blocks are permitted.
"""
import itertools
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from host import entry, nonanchor_entry, nonanchors
from refine_anchor import axis, crown
from search_four import search

H4 = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]]


def decode(word):
    return [[int(word[3*i+j]) for j in range(3)] for i in range(3)]


def encode(H):
    return ''.join(str(v) for row in H for v in row)


def find_copy(H, rows, cols, matrix):
    """Row enumeration and greedy ordered column subsequence search."""
    masks = [sum(v << j for j, v in enumerate(row)) for row in matrix]
    full = (1 << len(cols)) - 1
    nr = len(H)
    choices = (itertools.combinations if len(set(map(tuple, H))) == nr
               else itertools.combinations_with_replacement)
    checked = 0
    for ix in choices(range(len(rows)), nr):
        if any(ix.count(i) > rows[i].weight for i in set(ix)):
            continue
        checked += 1
        js, start, used = [], 0, 0
        for signature in zip(*H):
            mask = full
            for v, i in zip(signature, ix):
                mask &= masks[i] if v else full ^ masks[i]
            mask = (mask >> start) << start
            if not mask:
                break
            j = (mask & -mask).bit_length() - 1
            used = used + 1 if js and j == js[-1] else 1
            js.append(j)
            start = j if used < cols[j].weight else j + 1
        if len(js) == len(H[0]):
            return {'rows': list(ix), 'columns': js}, checked
    return None, checked


def trunk(h, with_anchors):
    def make(name):
        xs = axis(h, 2, name) if with_anchors else nonanchors(h, name)
        return [x for x in xs if x.kind != 'variable' or x.depth < h]
    rows, cols = make('row'), make('column')
    matrix = [[entry(r, c, crown(2)) for c in cols] for r in rows]
    return rows, cols, matrix


def run():
    h = 4
    rows, cols, matrix = trunk(h, True)
    cases = []
    for bits in itertools.product((0, 1), repeat=9):
        word = ''.join(map(str, bits))
        witness, checked = find_copy(decode(word), rows, cols, matrix)
        cases.append({'pattern': word, 'witness': witness,
                      'row_choices_examined': checked})
    missing = [c['pattern'] for c in cases if c['witness'] is None]
    assert missing == ['011101110', '011110101', '111100010']

    deletions = []
    for nr, nc in ((3, 3), (3, 4), (4, 3)):
        for ri in itertools.combinations(range(4), nr):
            for cj in itertools.combinations(range(4), nc):
                H = [[H4[i][j] for j in cj] for i in ri]
                witness, _ = find_copy(H, rows, cols, matrix)
                assert witness is not None
                deletions.append({'kept_rows': ri, 'kept_columns': cj,
                                  'pattern': H, 'witness': witness})

    nr, nc, nm = trunk(h, False)
    one_anchor = []
    for a, r1, r2, c1, c2 in itertools.product((0, 1), repeat=5):
        H = [[a, c1, c2], [r1, 1, 0], [r2, 1, 1]]
        witness, checked = find_copy(H, nr, nc, nm)
        one_anchor.append({'pattern': encode(H), 'witness': witness,
                           'row_choices_examined': checked})
    assert [x['pattern'] for x in one_anchor if not x['witness']] == [
        '010110011', '101110011']

    full_counts = []
    for word in missing:
        H = decode(word)
        counts = []
        for depth in range(1, 6):
            result = search(H, axis(depth, 2, 'row'), axis(depth, 2, 'column'),
                            lambda r, c: entry(r, c, crown(2)), depth)
            counts.append({'h': depth, 'copies': result['copies'],
                           'row_choices': result['row_choices']})
        full_counts.append({'pattern': word, 'counts': counts})
    return {'h': h, 'host_axes': {'rows': [vars(x) for x in rows],
                                 'columns': [vars(x) for x in cols]},
            'all_3x3_patterns': cases, 'deletions': deletions,
            'nonanchor_axes': {'rows': [vars(x) for x in nr],
                               'columns': [vars(x) for x in nc]},
            'one_anchor_borders': one_anchor,
            'full_counts_for_trunk_exceptions': full_counts,
            'scope': 'Finite discovery evidence. All-depth limitations and forced-bit certificates are separate; no 3x3 removal theorem or global minimality claim.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
