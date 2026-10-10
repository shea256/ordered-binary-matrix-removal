# Concrete-host semantic review

Date: 2026-10-10. Separate-agent review by `/root/four_proof_reviewer`.

**Verdict: no semantic error found in the seven requested modules.** Their host entries and actual axis orders agree with the written 4×4 construction. The class and crown statements in `HostStructure.lean` are mathematically valid. I did not assess compiler status, run Lean, or modify these modules; this is not a kernel certificate or independent peer review.

Reviewed: `ConcreteHost.lean`, `TreePositions.lean`, `AnchorFrames.lean`, `OrderedHost.lean`, `HostTreeOrder.lean`, `HostStructure.lean`, and `ThreeSeedSampling.lean` under `.context/ordered-binary-matrix-removal/formal/OrderedRemoval/`.

## Concrete host and actual orders

- **Classes and leaves:** `Fin (2*h+1)` assigns classes `2*i` and `2*i+1` to plus/minus at depth `i<h`, and only class `2*h` to the shared leaves. Each class has `2^h` coordinates. Dividing a coordinate by `2^(h−i)` gives the intended node and block size. `AtLevel` correctly lets the one leaf class satisfy both signs. The carrier size is exactly `(14*h+2)*2^h`.
- **Six roles:** Raw kind IDs remain `V+,V−,W+0,W+1,W−0,W−1`. Their row and column roles match all six manuscript modes, with zero-based group indices. Dummy row roles occur only as W role 2; dummy column roles only as V role 1. The own-minus variable-entry rule is strict only away from leaves; leaf-to-parent-plus uses `≤`, and leaf-to-parent-minus uses `<`.
- **Revised mode order:** `modeRank` maps the six raw kind IDs to `4,5,0,1,2,3`. Sorting therefore yields exactly `W+0,W+1,W−0,W−1,V+,V−` at every depth. Both full-axis order constructors explicitly pass `modeOrder`; neither silently uses the default `Fin` order.
- **Tree order:** The dyadic keys implement the recursive traversal. Early blocks sit at a subtree's left endpoint, ordered with shallower ancestors first. Late blocks sit at its right endpoint, ordered with deeper descendants first. At a shared endpoint, late phase 0 precedes early phase 1, so one subtree ends before the next begins. Leaves have odd endpoint keys strictly between their bounding even endpoints. The final coordinate orders actual positions inside each block. Thus rows have minus/subtrees/plus order and columns plus/subtrees/minus order.
- **Full axes:** `AnchorFrames` puts anchors first on both axes, dummy rows last, and dummy columns immediately after anchors. `rowIndex` and `columnIndex` separately enumerate these finite orders. The four parent/child inequalities in `HostTreeOrder` and their actual-index versions in `OrderedHost` have the same directions and weak endpoints as the manuscript, including shared leaves.

**Bridge caution:** When constructing `AnchorClassification.Certificate`, use `modeRank` (or an equivalent order-preserving numbering) as the natural-number mode label. Raw `Mode.val` still puts V before W. This is a future integration requirement, not a defect in the current actual orders.

## HostStructure class and crown statements

The entry formula in `variableEntry_true_iff` is exhaustive. Its three disjuncts mean: same class; matching-sign parent class two class-indices earlier; and the exceptional leaf-to-parent-minus transition one class-index earlier. That last disjunct is necessary, and its strict inequality is correct. No third alphabet symbol or accidental second leaf class is introduced.

The column-monotonicity and row-antimonotonicity statements require equal classes and the correct node inequality. They concern variable entries only, so anchor parity signatures do not invalidate them.

The class graph has edges between labels differing by two, plus all pairs among the terminal labels `{2h−2,2h−1,2h}`. `common_one_classes` supplies a sound necessary condition for two one-entries in a row. `class_triangle_terminal` is also valid: if the smallest vertex of a triangle were below the terminal three labels, its only higher neighbor outside the terminal clique would be the unique vertex two steps later, so it could not have two higher neighbors. At `h=0`, three distinct admissible labels cannot exist; the statement is vacuous rather than missing a positivity premise.

The crown proof first excludes equal column classes using opposite traces. It then forces the three distinct classes into the terminal three labels, hence one column is a leaf. Both rows that are one at that leaf column must themselves be leaves. Equal-class row antimonotonicity prevents the opposite traces required on the other columns. All three possible locations of the leaf column are explicitly covered. Distinct row/column position hypotheses are unnecessary because the asserted crown entries already exclude equal positions.

**Scope boundary:** `variable_crown_absent` excludes crowns on variable positions. A full nonanchor crown lemma must additionally discharge dummy rows and columns, each of which would be all ones on nonanchor positions and therefore cannot occupy a crown row or column. That extension is immediate mathematically but is not stated in this module. Ordered role-support containment and extraction of the anchor-count certificate also remain separate obligations.

## Three-seed sampling and provenance

I directly accessed the pinned upstream [ThreeSeedSampling.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Combinatorics/MatrixRemoval/ThreeSeedSampling.lean). It already contains the mixer, the row/column/both fiber decompositions, `atLevel`, root/leaf identities, ancestor identity, and protected-cell fiber theorems. The local attribution is appropriate: this sampling parameterization is inherited from upstream, not a new local result.

The mixer selects `u mod blockSize + blockSize * floor(z/blockSize)`. It preserves the ancestor of the shared leaf and uses an independent axis seed for the within-block coordinate. It equals the axis seed at the root and the common leaf at the leaf. Each protected row-variable/column-anchor pair, or the transposed pair, has exactly `m` preimages among `m³` seeds. Two anchor/dummy coordinates and two root coordinates use the independent axis seeds and have the same multiplicity. Reusing a seed within an axis does not affect these facts.

This distribution differs from the manuscript's many conditionally independent choices, but supplies the same required protected-cell bound. My previous report's observation about the distributions remains correct; any implication that the three-seed construction would need to be newly invented is superseded by this confirmed upstream provenance. The concrete selection/edited-cell incidence bridge and its composition with repair propagation still need to be established by the surrounding formalization.

## Checks performed

In addition to reading and reasoning through the declarations, I ran an independent Python transcription, importing none of the package code. It compared the dyadic-key order with an explicit recursive traversal for both axes at depths 0–6; compared the class-based entry formula with the raw host rule on 47,653 node-block pairs; checked every triangle in the integer class graph through depth 32; and checked 4,779 protected fiber counts through depth 4. Actual output:

```text
{'orders': 14, 'entry_iff_pairs': 47653, 'class_triangles': 32, 'seed_fibers': 4779}
All finite semantic spot-checks passed; no Lean build was assessed.
```

These finite checks are supporting evidence only. No compiler result, full removal theorem, or completed concrete-host certificate extraction is claimed by this review.

## Follow-up: concrete copy and anchor-certificate bridge

Reviewed subsequently: `RoleSupports.lean`, `ConcreteCopies.lean`, `ExtractAnchors.lean`, and `AnchorCertificate.lean`. **No semantic error or missing mathematical hypothesis found.** This conclusion concerns the declarations and arguments as written; I did not assess the pending `AnchorCertificate` build. Once that build succeeds, the concrete anchor-count extraction is a stronger checkpoint than the earlier conditional result. It still does not establish localization, the copy count, repair distance, or the full removal theorem.

### Copy model and possible vacuity

`ConcreteCopies.lean:13` defines `Copy h` by two independently chosen maps from `Fin 4` to raw positions. Their compositions with the separate increasing row and column enumerations are strictly increasing, and `entry_eq` fixes every one of the 16 Boolean entries to `H4`. This is exactly an arbitrary ordered induced copy in the original host. In particular:

- Row and column selections are independent; using a common raw carrier type does not identify their selections or their orders.
- Strict increase and the bijective enumerations imply distinct selected positions on each axis. No separate injectivity hypothesis is missing.
- Both zero and one constraints are enforced. No role, mode, anchor-count, or localization condition is built into `Copy`.
- The definition is specific to the original `host`. It should not be described as a copy predicate for an arbitrary edited matrix without a separate generalization.

The anchor-count theorem is nonvacuous for every `h≥1`. For example, take the `W_(h,0)−` mode, both of its anchor groups, leaf 0 and a dummy row; take the same two column anchor groups, leaf 0 and a position in its parent-minus block. This gives the displayed `H4` in the required orders. At `h=0`, the host has only two positions on each axis and no `Copy 0`; vacuity there is legitimate. Thus omitting a positivity premise from the universally quantified anchor-count implication is sound.

### Role supports and revised ranking

`RoleSupports` faithfully encodes each role as a whole class or one node-parity half. Dummy and anchor sentinel classes are respectively `2h+1` and `2h+2`, above all variable classes. No actual role accidentally contains anchor positions. `classAt` merges the two signs only at depth `h`.

The whole-before-half exclusion explicitly assumes `modeRank t ≤ modeRank u`, and uses the rank formula with the revised within-depth permutation. On rows, whole child-class supports in `V_i` follow `W_i`; on columns, whole supports of a child class occur only at the next depth. Leaf sign coincidences give equal halves, not new partial intersections. Dummy supports are whole and cannot coincide with a variable half.

`support_forward` is valid for arbitrary `Support` values under its stated whole-support implication: if the first support is whole, the second must be whole; otherwise the two points have the same parity, and a second half containing one contains both. Its applications get equality of class labels from the shared point. The resulting `rowRole_forward` and `colRole_forward` are exactly the no-earlier-proper-container property needed by the certificate.

The previous rank integration caution is resolved in this bridge: `ExtractAnchors.anchorRank` uses `modeRank`, not raw mode IDs. `row_anchor_order_iff` and `col_anchor_order_iff` also use that rank. The rank fields assigned by `Copy.anchorCertificate` therefore match the actual host order.

### Every certificate field is extracted

| Certificate field | Concrete justification checked |
| --- | --- |
| `rows_le`, `cols_le` | The explicit four-position `prefixCount` lies between zero and four. |
| `rowMode`, `colMode`, group fields | Actual anchor ranks and group indices; arbitrary defaults on nonanchors are harmless because all rank-field hypotheses restrict to anchors. |
| `row_order`, `col_order` | Anchor initial segments plus actual increasing order. Same-group twins are excluded by the distinct rows/columns of `H4`, so the block rank is strictly increasing even after offsets are discarded. |
| `anchor_one` | A one between two anchors forces their actual modes equal; their ranks therefore agree. |
| `crown_absent` | The concrete full-nonanchor crown exclusion is transported using `entry_eq` and the prefix characterization. |
| `row_support_comparable` | The shared anchor column places both rows in one row role/class; the concrete row-comparability lemma excludes the crossed traces. |
| `col_support_comparable` | The shared anchor row places both columns in one column role/class; the concrete column-comparability lemma excludes the crossed traces. |
| `no_backward_row_containment` | Actual anchor-row order gives nondecreasing mode ranks, and `colRole_forward` rules out the traces `11` then `01`. |
| `no_backward_col_containment` | The transpose argument uses actual column order and `rowRole_forward`. |

`prefixCount_spec` assumes the necessary initial-segment property; the two copy-specific prefix lemmas derive that property from the corresponding actual axis order. It is not imposed as an extra restriction on copies. Same-mode anchors with different offsets also cause no loophole: identical group labels would give globally twin rows/columns, contradicting distinct `H4` rows/columns. The group-rank inequalities consequently hold for every selected anchor pair.

The previous dummy-exclusion boundary is now resolved by `ConcreteCopies.nonanchor_zero_variables`: a zero between two nonanchors forces both to be variable positions. The three zero cells in the crown cover all six participating positions; the two zeros in each comparability contradiction cover all four positions. Therefore the uses of the variable-only lemmas do not silently omit dummy cases.

There is no circularity: `Copy.anchorCertificate` derives the structural fields from host lemmas, and only afterward invokes the earlier abstract `anchor_counts`. In particular, `Copy.anchor_counts` does not assume its conclusion or a prelocalized copy.

### Supporting checks and reporting boundary

I ran the separate reviewer support implementation through `h=8`, checking the forward-support property for every ordered pair of mode/group supports on both axes. I also checked the canonical witnesses above and a negative control using the obsolete V-before-W order. Actual output:

```text
Forward-support checks through h=8: 30240
Canonical nonvacuity witnesses h=1,...,8: all passed
Negative control: old V-before-W order violates forward support at h=1
```

The negative control uses a whole `V_1+` leaf support before a `W_(1,0)+` parity half under the old ordering; an odd and an even leaf disprove forward containment. Its exclusion by the new ranks is substantive.

After a successful build, update any package-wide statement that the concrete anchor-count certificate is still missing. The original `AnchorClassification` file alone remains conditional, but the new `AnchorCertificate` module supplies that connection. Other concrete theorem obligations remain and should be named separately. This source-level review does not itself establish compiler success or independent peer review.
