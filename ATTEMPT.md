# Executed attempts — OPENAI-190

Date: 2026-10-10. Current proof draft: [four-by-four.md](proofs/four-by-four.md).
Earlier attempts are retained below. The third refinement gives the current
4×4 candidate by localizing complete copies without a rigid anchor.

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


## Second refinement: executed attacks

### 1. Replace full shattering by a crown — successful local candidate lemma

The three-column proof uses only 110,101,011. Any three columns supporting
these traces must be in distinct classes, every pair must be adjacent in
the support graph, and the terminal triangle cannot supply both traces
with leaf coordinate one. Thus the entire nonanchor host excludes J_3-I_3.
All 156,576 quotient column triples through depth 5 satisfy this stronger
condition. A dense-prefix replacement first suggests an 8×8 anchor, but
its four-incidence threshold wastes information about how role supports
intersect. The final proof replaces that density argument entirely.

### 2. Reorder modes to make a 3×3 anchor rigid — candidate theorem

Every nonanchor role is a whole level/sign class, a parity half of one
class, or the dummy class. The supports are laminar. Strict containment
means a half-class in its full class. Column containers occur a level
later; row containers can occur in V_i at the same level as W_i. Therefore
put all W_i modes before V_i modes, with levels still increasing.
Now every strict container comes later on both axes.

For an S_3 copy, let a,b count its initial anchor positions. If both are
at least two, off-diagonal incidences plus aligned mode order force them
into one mode, then exclude all remaining nonanchors. If one count is at
least two and the other at most one, the required 11 and 01 signatures
would force an earlier support to contain a later one properly. If both
counts are at most one, a remaining anchor puts the last two opposite
positions in one nonanchor class, where the off-diagonal 2×2 pattern is
impossible. With no anchors, crown exclusion applies. This is an all-depth
rigidity proof with no six-row density prefix and no full shattering cube.

The original V-before-W order actually fails: at h=2, take the group-2
anchor row of W_{2,1}^+, followed by leaf rows 0 and 3. Take group-1 anchor
columns of V_2^+ and W_{2,1}^+, followed by leaf column 1. These form S_3
in increasing order. The new order reverses the first two columns, blocking
this witness. Its full position data is stored in the new report.

Executed exhaustive searches checked all 5,813,724 quotient row triples
through depth 6 and all compatible ordered column triples. The only S_3
copies were the 6h designated mode anchors, with weighted count 6h m^6.
A separate full-H embedding search at depths 1 and 2 checked all 1,567,588
quotient row quintuples and counted exactly 512 and 131,072 weighted copies.
It uses ordered-column dynamic programming and does not assume rigidity.
The original mode-body checker independently recovers 2m^8 for s=3.

The final quantitative implication is k=5, n=(20h+2)2^h, distance at least
(20h+2)^−2, and density 2(20h+2)^−10 4^−h. Its ratio to epsilon^C tends to
zero for every fixed C>0. The proof includes all edit directions.

### 3. Shrink the anchor to 2×2 — blocked for pure-anchor rigidity

Exhaustively enumerating the expanded nonanchor host at h=2 finds **all
16 binary 2×2 patterns**, with explicit ordered row/column witnesses.
Consequently no choice of a 2×2 anchor can have all its copies confined
to designated anchor blocks in this unchanged host. This rules out that
particular next step, not a different 4×4 obstruction or a weaker
localization proof. No global minimality theorem is claimed.

### Verification boundary

`check_refinement.py` also compares concrete role supports to a separately
encoded whole/half-class descriptor table through depth 8, and reruns the
exact arbitrary-path and sampling checks. An initial assertion in the
support-order checker had its inequality direction reversed; correcting
the checker made it agree with the explicitly stated containing-later
condition. This was a checker bug, not evidence against that condition.

All calculations are exact. The written all-depth argument is distinct
from this finite evidence. No independent agent/reviewer or Lean kernel
has verified the new result.

## Third refinement: 4×4 without pure anchor rigidity

### 1. Allow unintended anchor copies — executed

Set S=((0,1),(1,0)) and retain the two role signatures and P body. The full
pattern is H=((0,1,1,0),(1,0,0,1),(1,0,1,0),(0,1,1,1)). Reuse the W-before-V
order. This cannot make S rigid: the previous all-16-patterns check rules
that out. A full-pattern search is needed instead of an anchor-only search.

Exact weighted searches found 128; 18,944; 1,687,552 copies at depths 1,2,3,
with no wholly nonleaf witness. Those counts exceed the designated-mode
formula 2m^6 starting at depth 2. Classifying copies by their selected
anchor counts identifies a new configuration: two anchor rows and one
anchor column. The proof excludes all other counts except the designated
(2,2) case using crown exclusion and ordered role supports.

### 2. Retain the old leaf-diagonal hitting set — failed

A depth-two H copy has no leaf column: its last three columns are
C_1^+(0), C_1^+(1), C_1^−(1), and its last two rows are leaf 2 and a dummy.
Its first row is group 1 of W_{2,0}^+, second row group 2 of W_{2,0}^−,
and first column group 1 of W_{2,0}^− (group indices here start at one).
It matches H exactly and is missed by every diagonal-leaf cell.
The complete coordinates are preserved in `verification/reference/four-report.json`.
This invalidates reusing the old hitting-set claim for the smaller pattern.

### 3. Localize a fixed zero instead — candidate theorem

The (2,1) case still forces row 3 to be leaf p and column 4 into
C_{h-1}^−(floor(p/2)), where the entry is zero. Row 4 is dummy. The same
statement holds in the (2,2) case. There are only 2m cells of this form.
The proof splits by the second anchor row's mode; the W− nonleaf case
uses the order of its two parity modes to rule out the required strict
inequality p<q. This is proved in the all-depth draft, separately from tests.

For leaf p=2b+d, every unbalanced copy has three size-m anchors, one size-m
dummy row, and two choices for its last column. The first anchor and the
middle column pair have four possible families, contributing
(11−d)b+4 floor(b/2) pairs. Summing gives (25/4)m^6−(29/2)m^5 extra copies
for h≥2; adding the 2m^6 balanced copies yields (33/4)m^6−(29/2)m^5.
At h=1 there are no extra copies. The distance proof uses designated copies
only and therefore survives the failure of pure anchor rigidity.

The resulting quantitative implication is k=4, n=(14h+2)2^h, arbitrary
repair distance at least (14h+2)^−2, and density bounded by
(33/4)(14h+2)^−8 4^−h. The latter divided by epsilon^C tends to zero
for every fixed C>0. It is the fixed forbidden pattern that shrinks; the
qualitative obstruction and exponential-in-depth mechanism are inherited.

### Boundary and second-pass checks

A full embedding census through h=4 checks 3,693,411 quotient row quadruples
and all matching column quadruples without assuming localization. Exact
counts and every additional-copy family agree with a separate node-pair
sum, also checked through h=8. Crown exclusion, role containment, strict
tree orders, arbitrary path bits, and protected probabilities pass.

Reversing the two W− parity modes gives a wholly nonleaf copy at h=3:
rows are W_{2,1}^− group 1, W_{2,0}^− group 2, R_2^−(2), and dummy;
columns are W_{2,0}^− group 1, C_2^−(1), C_2^−(3), C_1^−(1).
The same fixed-depth blocks persist at every h≥3, with m^8/128 weighted
copies, violating the intended zero-cell localization and density bound
for large h. Thus the specified parity order is a substantive requirement.

A same-agent review corrected the direction of both inequalities in the
aligned-mode chain in Lemma 3; the corrected chain forces the same equality.
No independent peer review or universal machine-checked proof is claimed.
No claim that 4×4 is globally minimal is made.
