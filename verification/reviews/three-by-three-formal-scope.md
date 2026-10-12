# 3×3 Lean statement and construction alignment

Date: 2026-10-11. This note is the formalizing agent's semantic second pass,
**not a separate-agent review or independent human mathematical peer review**.
The user's [separate adversarial report](three-by-three-adversarial.md) covers
the written proof snapshot and explicitly did not build or review Lean.

## Exported statement

[`OrderedRemoval.Crown.no_polynomial_removal_bound`](../../formal/OrderedRemoval/Crown/Complete.lean)
has no host, localization, sampling, or entry-preservation hypotheses. It
quantifies over positive real c,C,ε₀ and produces 0<ε<ε₀ such that every
natural host-size threshold N admits n≥max(1,N) and a square binary host.
Every crown-free binary repair has Hamming distance at least εn², and the
ordered-copy count is strictly below c ε^C n⁶.

`Crown.fixedH` is literally `Fin 3 → Fin 3 → Bool`, with rows
`011/101/110`. `orderedCopies` matches all nine labels under two separately
increasing maps. `HFree` means zero such copies. The inherited Hamming
distance counts all cells at which the two binary matrices differ, so
edits to anchors, dummies, zeros and ones are all included.

## Deliberate quantitative difference

The written construction has m=2^h, size-m anchors, n=(8h+2)m, and exact
count 7m⁴. The formal construction has **size-2m anchor blocks on both
axes**, n=(14h+2)m, and proves only the sufficient estimate N_K≤2mn⁴.
It uses the same pattern, body, entry rules, and relative block orders.
Each doubled anchor is implemented as two consecutive twin subgroups.

The raw carrier and its cardinality are inherited; the new column order
moves all anchors after dummy and variable columns. The row order remains
prefix anchors, the signed tree, then dummy. The executable comparison
checks these actual Lean order definitions against the literal Python
model, not a handwritten substitute for the Lean order.

Both variants prove the qualitative statement above. The new certificate
must not be described as proving the written 7m⁴ enumeration, its smaller
host parameters, exact repair equality, or minimality.

## Proof connections checked

1. `Copy.first_row_anchor`, `Copy.middle_col_nonanchor`,
   `Copy.last_col_anchor`, and
   `Copy.second_row_nonanchor_of_last_col_anchor` classify every copy.
   The new crossing-support argument uses the common column last. The
   shared-leaf exception and absence of the odd-child addition at the
   leaves are retained by the inherited `topVariable` definition.
2. `Copy.zero_localization` places the middle zero at a leaf and its own
   minus parent. The vertical/dummy exception is excluded by the added
   ones from dummy rows to vertical anchor columns. The general counting
   injection retains the two fixed coordinates and encodes the other four,
   hence 2m·n⁴, not the old 3×4 exponent.
3. `FrameValid.not_HFree` completes the ordered body P using one prefix
   anchor row and one suffix anchor column, matching the crown's five
   border entries. Named role membership supplies these entries; the added
   vertical-dummy ones lie outside the vertical body roles.
4. The inherited three-seed guard argument is applied to the new host.
   It selects one representative from each m-sized subgroup, not a uniform
   representative from a whole 2m anchor block. Each guarded cell has
   selection probability at most 1/m², giving the stated repair lower
   bound m². No such frequency bound is asserted for leaf diagonals.
5. For d=14h+2, the two estimates concern the **same** matrix and give
   ε=d⁻² and density at most 2ε2⁻ʰ. The inherited analytic lemma makes this
   smaller than c ε^C for arbitrarily large h. Uniform blowup multiplies
   the repair lower bound by q² and bounds the copy count by q⁶ times the
   original; ε is chosen before the universal host-size threshold N.

## Executed checks and limits

The [printed theorem statements](../reference/crown-theorem-statements.txt)
come from executing [crown_statements.lean](../crown_statements.lean).
They expose the exact quantifier order, n⁶ normalization, unrestricted
repair type, literal nine entries, and the capstone's three standard axioms.

The [model report](../reference/crown-formal-model-report.json) compares
both axis orders and every entry at h=0,1,2,3: 139,332 cell comparisons.
Physical copy censuses at h=0,1,2 give 0,448,7,168. The zero-height case
has no anchors or copies; the repair theorem explicitly requires h≥1.

The [formal audit](../reference/crown-formal-audit.json) binds the code,
audits every imported project declaration's transitive axioms, and replays
each local module into its imported environment. Only Lean's standard
`propext`, `Quot.sound`, and `Classical.choice` are permitted. Replaying
modules is not a fresh replay of all Mathlib or a check by another proof
assistant. Finite model comparisons supplement, rather than establish,
the universal theorem. No new priority search was performed in this port.
