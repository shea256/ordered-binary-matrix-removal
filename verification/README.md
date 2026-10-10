# Verification scope

`check_four.py` checks the current 4×4 candidate. It exhaustively examines
3,693,411 quotient row quadruples and all matching ordered column choices
through depth 4, with exact twin-block multiplicities and no assumed
localization. The copy counts are 128; 18,944; 1,687,552; and 123,207,680.
Every copy has the claimed anchor configuration and fixed zero-cell location.
A separate node-pair sum agrees with the closed formula through depth 8.

The checker also covers 3,166 strict tree-order comparisons, 156,576
nonanchor column triples, 28,944 role-support pairs, 34,952 free path-bit
assignments, and exact sampling marginals through depth 8. It includes
counterexamples to reusing the old leaf-diagonal hitting set and to reversing
the minus parity modes. `check_four_repair.py` checks all 510 leaf choices
through depth 8: flipping the new zero-cell hitting set creates new copies,
so eliminating the original copies is not a valid repair argument.

These scripts reuse the existing host implementation and some earlier
checkers. The separate count calculation and same-agent second pass are
not independent mathematical review. The universal claims rest on the
written proof in `proofs/four-by-four.md`.

`check_refinement.py` retains the earlier 5×5 checks: all 5,813,724
quotient row triples in full anchor searches through depth 6; all 1,567,588
quotient row quintuples in full pattern searches through depth 2; 156,576
nonanchor column triples; and 28,944 role-support pairs through depth 8.
It also reruns exact mode counts, sampling marginals, path assignments, and
terminal threshold checks. It includes the old-order failure and witnesses
for all 16 nonanchor 2×2 patterns. The exhaustive full-pattern searches do
not assume the anchor rigidity theorem.

The retained `check_compression.py` checks anchor properties, 156,576 quotient triples,
weighted mode counts through depth 6, sampling marginals, and source manifest
metadata. `check_adversarial.py` uses a separate threshold/path calculation
without importing the host: 74,898 threshold cases and 34,952 path assignments.
Both were written by the same agent. Neither is independent peer review.

`reference/` contains deterministic outputs regenerated for this package.
`upstream-audit.json` is the historical same-agent audit from the originating
workspace: 78 source hashes and 61 implementation modules scanned. It is not
a Lean build. `fetch_upstream.py` plus `check_sources.py` reproduce the pinned
byte checks online. The cache is ignored, and default offline checks do not
pretend to rehash absent source files.

Finite tests cannot prove the all-depth classification, localization, or
arbitrary repair bound. Those obligations are the manuscript's mathematical argument.
