#!/usr/bin/env python3
"""Finite transcription of Wang's pinned 4x4 mode order, not a Lean audit."""
import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import check_optimized_order as audit


def wang_axes(h, axis, order=None, expanded=False):
    def key(x):
        if x.kind != 'anchor':
            return (1,)
        i, kind, sign, parity = x.mode
        if kind == 'W' and sign == '-':
            return (0, 0, i, parity, x.group)
        rank = [('V', '+', -1), ('V', '-', -1), ('W', '+', 0), ('W', '+', 1)].index((kind, sign, parity))
        return (0, 1, i, rank, x.group)
    return sorted(audit.literal.axes(h, axis, expanded=expanded), key=key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    original_axes = audit.axes
    try:
        audit.axes = wang_axes
        results = [audit.census(h, 'wang_source_order') for h in range(1, 4)]
    finally:
        audit.axes = original_axes
    assert [r['copies'] for r in results] == [128, 9216, 622592]
    report = {'source_commit': '8c503f7a7a0f42c53621dcd0bdaf753e2580aa3e', 'records': results,
              'scope': 'Literal finite transcription of Wang manuscript mode order; no fresh Lean build or all-depth independent audit.'}
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'counts': [r['copies'] for r in results]}))


if __name__ == '__main__':
    main()
