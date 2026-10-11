# Separate-agent semantic review of the 3×4 formalization

Reviewer: `/root/four_proof_reviewer`. Date: October 11, 2026.
The coordinator archived the reviewer's returned report below. This is
separate AI review, not independent mathematical peer review.
The source snapshot is in [three-by-four-formal-review-snapshots.json](../reference/three-by-four-formal-review-snapshots.json).

## Verdict

Reviewed all 24 new `OrderedRemoval/Rectangular` modules through
`Complete.lean`, against `proofs/three-by-four.md`. No required mathematical
source corrections remain in the reviewed snapshot.

The formal model represents H=`1001/1010/0111`, with independent ordered
row and column selections. The two consecutive, identical row-anchor
subgroups correctly represent one block of size 2m; column-anchor groups
remain distinct. The revised mode order, dummy entries, and nonterminal
odd-child additions agree with the manuscript.

The localization chain covers arbitrary copies rather than assuming an
anchor configuration. Its support arguments exclude zero or multiple anchor
rows and zero anchor columns, and its remaining cases force the distinguished
zero to a leaf and its own parent-minus column. Boundary distinctions at the
shared leaf level are preserved. The resulting injection gives the coarse
bound 2mn⁵, retaining the factor 2 in normalized density. This is not an
exact enumeration.

The repair theorem quantifies over every binary repaired matrix, including
repairs that change anchors. The guarded-path argument forces a copy from
agreement on protected cells; it does not merely hit copies of the original
host. The formal sampler differs from the manuscript's uniform choice within
a 2m-sized row block: it samples representatives from the m-sized subgroups,
and the designated completion uses one subgroup. Its selected-position
marginal is 1/m, rather than 1/(2m). The guard-cell probability nevertheless
remains at most m⁻², so this alternate sampler supports the stated m² repair
lower bound without losing a factor.

The blowup argument correctly partitions all edited cells into q² slices
and transfers the repair lower bound to arbitrary repairs of the enlarged
matrix. Distinct rows and columns of H ensure projected copies remain
strictly ordered. The formal counting result is the upper bound
N_H(A^(q))≤q⁷N_H(A), which suffices for the capstone; it does not establish
exact equality.

The final `OrderedRemoval.Rectangular.no_polynomial_removal_bound` has the
intended strong quantifiers: for all c,C,ε₀>0, there exists ε in (0,ε₀)
such that for every N there exist n≥max(1,N) and A, with every H-free repair
requiring at least εn² changes and N_H(A)<c ε^C n⁷. The base host and ε are
chosen before N; a positive blowup factor supplies arbitrarily large hosts.
The final arithmetic correction preserves this statement and argument.

## Execution scope

This is a separate AI-agent semantic review, not human peer review or a
novelty certification. Earlier targeted Lean inspection confirmed that the
repair theorem resolves to the new rectangular host and pattern, with only
`propext`, `Classical.choice`, and `Quot.sound` reported as axioms.

The reviewer did not complete a fresh final whole-project build: an attempted
import encountered a missing `NoAnchorColumns.olean` during the concurrent
rebuild. The coordinator separately runs the final source-bound axiom audit
and kernel replay. The historical H4 audit does not certify this new result.
This review makes no claim of exact repair distance, exact copy count, or
a 3×3 obstruction.
