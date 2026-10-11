# Verification scope


The **current 3×4 main theorem is checked in Lean**, with arbitrarily small
ε and arbitrarily large hosts for the same ε. Run
`python3 scripts/run_rectangular_formal_checks.py` with the pinned toolchain.
The [new audit](reference/rectangular-formal-audit.json) covers all
73 project modules and their compiled declarations;
[formal/README.md](../formal/README.md) describes the precise scope.
The [semantic review](reviews/three-by-four-formal.md) is separate AI review,
not independent mathematical peer review. Exact all-depth enumeration,
repair equality, and minimality are outside this certificate.

## Current 3×4 candidate

[check_three_by_four.py](check_three_by_four.py) independently constructs the
host and performs a complete weighted census through h=6, physical h=1,
role-signature checks and adverse entry variants.
[check_three_by_four_reviewer.py](check_three_by_four_reviewer.py) was written
by a separate agent, with full census through h=4 and structural checks
through h=7. [Review](reviews/three-by-four.md).

The [3×4 proof](../proofs/three-by-four.md) supplies the universal argument.
The main theorem is Lean verified; independent mathematical peer review remains pending.
The [uniform-template certificate](../proofs/asymmetric-limitations.md)
covers 16,384 templates outside the successful nonuniform family.

## Historical verification


### Earlier refinement: global mode order

[check_optimized_order.py](check_optimized_order.py) compares four mode orders
through h=4 with a full column-quadruple/row-DP census, and checks the explicit
terminal-anchor repair. It reuses the historical literal entry table, not its
copy counter. [check_optimized_order_reviewer.py](check_optimized_order_reviewer.py)
was written by a separate AI reviewer with no candidate-code imports; it builds
axes recursively and enumerates all matching row quadruples. It also checks the
support and generic localization cases through h=7. Both include expanded h=1
physical checks. Reports are in [reference](reference/optimized-order-report.json)
and [reviewer reference](reference/optimized-order-reviewer-report.json).

The written proof is [optimized-order.md](../proofs/optimized-order.md).
The new order, exact count, exact repair equality, and restricted optimum are
not yet formalized in Lean. Historical formal and Python reports below remain
valid for their original host orders and must not be reinterpreted as proving
the new refinement. Separate AI review is not mathematical peer review.


`check_four.py` checks the earlier 4×4 candidate. It exhaustively examines
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

## Separate-agent audits and Lean development

[check_four_literal.py](check_four_literal.py) imports no candidate-package
code. It constructs variable order using binary-interval endpoints, counts
all copies by a column dynamic program through h=4, and expands all actual
positions at h=1. It checks protected frequencies for an alternate
three-seed sampler through h=3 and includes two negative controls:
reversing minus parity order and flipping the original zero set.

[check_four_reviewer.py](check_four_reviewer.py) was written by the
user-authorized separate reviewer. It checks supports, the precise earlier
minus-half restriction, relaxed unbalanced configurations, every possible
last row, and weighted unbalanced counts through h=7. It assumes the
already-classified unbalanced sector; it is not a full census.
Only the runtime-version output field was removed for portable reference
comparison. The original review used Python 3.9.25.

Both new reports are compared by `scripts/run_checks.py`. Their implementations
are separate from the old host code, but this is not independent peer review.
The [review report](reviews/four-separate-agent.md) found no material error;
the [assurance checkpoint](reviews/four-assurance.md) summarizes its scope.

The historical H4 part of the [Lean project](../formal/README.md) verifies its concrete host,
all-depth anchor classification, fixed-zero localization, dummy last row,
zero-set size bound, coarse copy count, arbitrary-repair lower bound, and
the unconditional every-c,C removal theorem.
The historical audit checks every H4 project declaration and replays each H4 module
into its imported Lean environment; it does not freshly replay Mathlib. The
archived receipt binds the exact sources. The default Python suite checks
that binding but does not run Lean. The sharper exact copy count and canonical
sampler lower bound remain unformalized.

The [localization review](reviews/four-localization.md) and its separate
[checker](check_four_localization.py) cover the weaker generic localization
premises through h=7, 419,513 ordered position pairs for column bounds,
the zero code through h=10, and last-row class intersections through h=100.
Its [output](reference/four-localization-report.json) is finite evidence;
the Lean theorems supply the all-depth proofs for this checkpoint.

## End-to-end removal checkpoint

[Main.lean](../formal/OrderedRemoval/Main.lean) closes the qualitative theorem
using the sufficient coarse count, unrestricted binary repair bound, and
real-valued decay. [four-removal.md](reviews/four-removal.md) records the
separate-agent semantic review and its original snapshot hashes.

[check_four_removal.py](check_four_removal.py) imports no candidate code. It
reconstructs all three-seed paths through h=4, checks all four frames per edge
and both binary labels, confirms guard containment and maximum cell frequency
m, and includes the unprotected leaf-diagonal frequency m² as a negative
control. It also checks normalization with exact fractions. The ninth default
check compares its output with [four-removal-report.json](reference/four-removal-report.json),
ignoring only the Python-version metadata. This finite audit is distinct from
the universal Lean proof and from independent mathematical peer review.
