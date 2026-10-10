# Executed attempts — OPENAI-190

Date: 2026-10-10. Full proof draft:
[compressed-pattern.md](proofs/compressed-pattern.md).

## Attack 1: compress the shattering witness and anchor — candidate

The baseline bounds variable row support by three column classes and
deduces five-column nonshattering. That discards class geometry. The
actual support graph consists of two paths ending in one triangle on
the shared leaves and the two preceding signs. If three classes were
shattered, all three pairs would have to be supported. This forces that
terminal triangle. On it the leaf traces are three nested initial
interval tests of the leaf node p. They cannot supply two incomparable
words with a leaf-coordinate one. Same-class columns cannot be separated
against suffix monotonicity. Thus three-column nonshattering holds at
every depth, including h=1 and duplicate columns.

Replace the 32-word, five-column rectangle with the eight three-bit
words in a 13-by-13 off-diagonal-one anchor: rows 6 through 13,
columns 11 through 13. Row 6 is the all-zero word, allowing the first
six rows still to have at most one zero per column. The first six
columns retain at most one zero per row. Both prefix densities are
five, strictly exceeding the maximum four mode incidences of a variable
position. Rows/columns remain distinct and each has at least nine ones.

An alleged S copy with at most five anchor rows and ten anchor columns
would have an entirely non-anchor eight-by-three word rectangle.
Otherwise at least six anchor positions occur on one axis. Prefix
density excludes variable positions on the opposite axis; twins allow
only one dummy; common-one intersections force the remaining anchors
into one mode. Unit-vector signatures exclude the dummy and the other
axis's non-anchors. This asymmetric initial threshold, with six-position
dense prefixes, is the new rigidity proof.

With s=13 the forbidden pattern has k=15 and the host n=(80h+2)2^h.
Repair distance remains at least (80h+2)^-2; exact density is
2(80h+2)^-30 4^-h. Dividing by epsilon_h^C tends to zero for every
C>0, so the local lemma reaches the final nonpolynomial removal theorem.
No universal theorem is inferred from finite tests alone.

Executed exact checks: all 156,576 triples of quotient non-anchor
columns across h=1,...,5 miss a word; all anchor conditions pass;
all ordered mode bodies at h=1,...,6 localize to the leaf diagonal.
The quotient preserves identical-entry blocks with exact integer
multiplicities; it is not a finite host substituted for the asymptotic
construction. See [compression-report.json](verification/reference/compression-report.json).

## Attack 2: reduce to two nonshattered columns — failed, rigorous limitation

At depth h=2 choose a root-plus node-0 column and a level-1 plus node-0
column. A root-plus row, level-1 plus node-0 row, leaf-0 row and leaf-2
row realize respectively 10,11,01,00. The explicit counterexample is
checked in [check_adversarial.py](verification/check_adversarial.py).
At h>2 use level-2 plus rows 0 and 2 in place of the leaf rows.

Therefore the concrete non-anchor host has VC dimension two for h>=2,
and the three-column lemma cannot be strengthened to two columns for
this host. This rules out that specific shattering compression step;
it does not establish a lower bound of 15 on forbidden-pattern size,
nor rule out a different anchor or different construction.

## Attack 3: exact copy counts — executed, baseline-derived refinement

Once localization is proved, every original body is a W_{h,d}^- body
with the same row/column leaf p, parent column node floor(p/2) and dummy
row. The count is exactly 2m^2 bodies, not merely a loose upper bound.
There are m^{2s} independent anchor choices, so for both the original
s=64 and replacement s=13 constructions

\[
 N_H(A_h)=2m^{2s+2},\qquad
 N_H(A_h)/n^{2s+4}=2d^{-2s-4}m^{-2}.
\]

This stronger count also applies to the original 66-by-66 pattern. It
must not be marketed as evidence that the new construction has a new
exponential mechanism. The theorem improvement is the fixed pattern
size; host overhead and the sampling exponential constant improve as
consequences. Exact counts were recalculated at depths 1 through 6
for both s values.

## Adversarial second pass

An alternate checker, without importing the host implementation,
reconstructs the entire 15-by-15 pattern from an independent integer
formula, checks 74,898 terminal-triangle threshold configurations, and
enumerates all 34,952 binary assignments of the free entries in path
constraints at depths 1 through 4. None allows P-avoidance while
preserving the protected roots and dummy incidences. Intermediate
variable entries may take arbitrary values in these checks.

The sampling audit explicitly checks that shared diagonal leaf cells
have selection probability 1/m, rather than 1/m^2. The latter value
is used only for protected anchor/dummy and root cells. Treating all
sampled variable entries as independent would invalidate the proof.
Finite probabilities are represented by exact Fractions.

Flipping the m original diagonal-leaf ones removes all old copies but
creates W_{h,d}^+ copies, so original-copy hitting cannot stand in for
the m^2 repair-distance argument. The full proof describes these new
copies explicitly.

This second pass was performed by the same agent. It is not independent
peer review, and finite enumerations are not a machine-checked universal
proof. The all-depth mathematical proof is the essential certificate.
