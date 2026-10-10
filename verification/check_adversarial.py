#!/usr/bin/env python3
"""Second-pass checks using integer thresholds and Boolean constraints.

This script does not import the host implementation. It is same-agent
verification, not independent peer review or a kernel-checked theorem.
"""
from itertools import product
from pathlib import Path
import json


def anchor_check():
    report = json.loads((Path(__file__).parent / "reference" / "compression-report.json").read_text())
    H = report["anchor"]["pattern"]
    S = [r[:13] for r in H[:13]]
    expected = [[int(i != j) for j in range(13)] for i in range(13)]
    for word in range(8):
        expected[5 + word][10:] = [int(bool(word & mask)) for mask in (4, 2, 1)]
    assert S == expected
    assert all(len(r) == 15 for r in H) and len(H) == 15
    assert H[13] == [1, 0] + [0] * 11 + [1, 0]
    assert H[14] == [0, 1] + [0] * 11 + [1, 1]
    assert all(H[i][-2:] == [int(i == 0), int(i == 1)] for i in range(13))
    assert all(sum(S[i][j] for i in range(6)) > 4 for j in range(13))
    assert all(sum(row[:6]) > 4 for row in S)
    return {"explicit_pattern_matches_independent_formula": True}


def threshold_cases():
    checked = 0
    for h in range(1, 7):
        m = 2 ** h
        for q, plus, minus in product(range(m), range(m // 2), range(m // 2)):
            # Convert floor(p/2)<=plus and floor(p/2)<minus to cutoffs on p.
            cutoffs = (q, 2 * plus + 1, 2 * minus - 1)
            traces = {tuple(int(p <= t) for t in cutoffs) for p in range(m)}
            assert all(all(a <= b for a, b in zip(x, y))
                       or all(b <= a for a, b in zip(x, y)) for x in traces for y in traces)
            assert not ({(1, 1, 0), (1, 0, 1)} <= traces)
            checked += 1
    return {"exceptional_triangle_threshold_cases": checked, "maximum_h": 6}


def propagation_cases():
    summaries = []
    for h in range(1, 5):
        # At each level two row-transition bits, plus two diagonal bits;
        # at the final level the signs share a single diagonal bit.
        variables = 4 * h - 1
        valid = 0
        for values in product((0, 1), repeat=variables):
            old_plus, old_minus = 1, 0
            allowed = True
            for i in range(h):
                offset = 4 * i
                b_plus, b_minus = values[offset:offset + 2]
                if i == h - 1:
                    c_plus = c_minus = values[offset + 2]
                else:
                    c_plus, c_minus = values[offset + 2:offset + 4]
                # Four bodies, retaining fixed dummy ones. These constraints
                # inspect P directly rather than relying on derived inequalities.
                bodies = ((1, b_plus, 1, old_plus), (1, old_minus, 1, b_minus),
                          (b_plus, c_plus, 1, 1), (c_minus, b_minus, 1, 1))
                if (1, 0, 1, 1) in bodies:
                    allowed = False
                    break
                old_plus, old_minus = c_plus, c_minus
            valid += allowed
        assert valid == 0
        summaries.append({"h": h, "free_binary_assignments": 2 ** variables,
                          "H_free_path_assignments": valid})
    return summaries


def two_column_counterexample():
    # Depth two; columns root-plus node 0 and child-plus node 0.
    # Rows root-plus 0, child-plus 0, leaf 0, leaf 2.
    matrix = [[1, 0], [1, 1], [0, 1], [0, 0]]
    assert set(map(tuple, matrix)) == set(product((0, 1), repeat=2))
    return {"h": 2, "rows": matrix, "all_four_words": True}


if __name__ == "__main__":
    print(json.dumps({"anchor": anchor_check(), "thresholds": threshold_cases(),
                      "arbitrary_path_edits": propagation_cases(),
                      "failed_two_column_attack": two_column_counterexample(),
                      "scope": "Same-agent exact finite second pass; universal proof is in proofs/compressed-pattern.md."}, indent=2))
