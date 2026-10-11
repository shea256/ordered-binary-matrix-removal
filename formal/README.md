# Partial Lean formalization of the 4×4 argument

**Status: partial, with concrete zero-cell localization proved.** Lean 4.34.1
checks the actual host and its independent axis orders, anchor counts
**(2,2) or (2,1)**, and localization of every ordered H4 copy at every
depth. The fixed zero (third row, fourth column) lies in the
leaf-to-parent-minus set; that set has at most `2·2^h` cells, all zero,
and the last selected row is dummy. No structural certificate or
localization hypothesis is assumed by the copy theorems. Copy counting,
arbitrary-repair connections, and the final removal theorem remain open.
The overall research result remains a candidate.

With the pinned Lean/Lake toolchain available, from the repository root:

```sh
(cd formal && lake exe cache get)
python3 scripts/run_formal_checks.py
```

Mathlib is pinned to commit `d13f23b723b8a846827a245b89c10fc7d3f11612`;
`lake-manifest.json` pins its transitive dependencies. The initial dependency
and cache download requires network access and substantial disk space.

The script builds the project, discovers compiled declarations by owning
module, and checks their transitive axiom dependencies. It also matches every
source-declared theorem against the compiled environment, including nested
namespaces and dotted names. Only `propext`, `Quot.sound`, and
`Classical.choice` are permitted. No added axioms or admitted proofs are used.
It then replays **each project module into its imported environment** using
Lean's kernel. This does not freshly replay all Mathlib dependencies or use
a different proof assistant. The earlier 34-helper Std-only checkpoint did
use fresh-environment replay; these are different verification scopes.

Source hashes and results go to `.context/formal-checks-receipt.json`.
The archived run is [formal-audit.json](../verification/reference/formal-audit.json).
The [host review](../verification/reviews/four-concrete-host.md) and
[localization review](../verification/reviews/four-localization.md) check
agreement with the manuscript. These are separate-agent semantic reviews,
not independent peer review.

## What is proved

| Component | Checked statement | Remaining connection |
| --- | --- | --- |
| [ConcreteHost](OrderedRemoval/ConcreteHost.lean), [TreePositions](OrderedRemoval/TreePositions.lean), [AnchorFrames](OrderedRemoval/AnchorFrames.lean), [OrderedHost](OrderedRemoval/OrderedHost.lean) | The finite binary host has `(14h+2)2^h` positions, shared leaves, the revised mode ranks, and two independently enumerated axis orders. | Use these definitions in the remaining repair arguments. |
| [HostStructure](OrderedRemoval/HostStructure.lean), [RoleSupports](OrderedRemoval/RoleSupports.lean), [ConcreteCopies](OrderedRemoval/ConcreteCopies.lean) | Concrete crown exclusion, same-class comparability, forward support containment, twin exclusion, and dummy exclusions. | These structural facts are already connected to anchor classification. |
| [ExtractAnchors](OrderedRemoval/ExtractAnchors.lean), [AnchorCertificate](OrderedRemoval/AnchorCertificate.lean), [IndexedHost](OrderedRemoval/IndexedHost.lean) | Every actual ordered copy supplies the certificate and has counts (2,2) or (2,1). The indexed matrix interface assumes only increasing index maps and the sixteen H4 entries. No copies at height zero; an explicit balanced copy at height one. | Used by the concrete localization theorem. |
| [HostTreeOrder](OrderedRemoval/HostTreeOrder.lean), [LocalArithmetic](OrderedRemoval/LocalArithmetic.lean) | Four concrete parent/child order equivalences and the conditional arithmetic contradictions for localization. | Connected to actual copies by the localization modules below. |
| [TreeComparisons](OrderedRemoval/TreeComparisons.lean), [LocalizationFrame](OrderedRemoval/LocalizationFrame.lean), [LocalizationArithmetic](OrderedRemoval/LocalizationArithmetic.lean), [ThirdColumn](OrderedRemoval/ThirdColumn.lean) | Concrete order bounds, common mode frame, variable third column, and all mode cases including the essential earlier-minus parity condition. | Connected to every copy in ZeroLocalization. |
| [ZeroLocalization](OrderedRemoval/ZeroLocalization.lean), [LastRow](OrderedRemoval/LastRow.lean), [ZeroSetSize](OrderedRemoval/ZeroSetSize.lean) | Every copy localizes to a zero cell in T_h; its last row is dummy; an injection into leaves × parity bits proves cardinality at most 2m. | Count copies from the fixed cell. Exact cardinality 2m for h≥1 and the sharper exact copy formula are not formalized here. |
| [ThreeSeedSampling](OrderedRemoval/ThreeSeedSampling.lean) | The inherited finite sampler, root/leaf and ancestor identities, and exact mixer fiber counts. | Instantiate the protected-cell incidence bound for edited host cells. |
| [Propagation](OrderedRemoval/Propagation.lean), [ProtectedSampling](OrderedRemoval/ProtectedSampling.lean) | Arbitrary-depth Boolean propagation and a finite union bound under explicit incidence hypotheses. | Extend the resulting body to an ordered H4 copy in an arbitrary edited matrix. |

The key exports in `OrderedRemoval.Concrete` are:

- `Copy.zero_localization` and `matrix_zero_localization`: all ordered
  copies, including both anchor-count cases, with independent axis maps.
- `Copy.last_row_dummy`: the last selected row is dummy in every copy.
- `zeroSet_entry` and `card_zeroCells_le`: the designated cells are zeros
  and their number is at most `2·2^h`, including the h=0 boundary.

These statements concern all natural depths, not an enumeration of finitely
many hosts. The matrix interface assumes only strict row/column order and
the sixteen H4 entries. The earlier height-zero exclusion and explicit
height-one copy witness nonvacuity and boundary behavior.

## Inherited three-seed sampler

The paper chooses many representatives independently conditional on a leaf.
The smaller three-seed parameterization already appears in upstream
[ThreeSeedSampling.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Combinatorics/MatrixRemoval/ThreeSeedSampling.lean).
Our adapted module preserves that construction; it is not a new local result.

Take independent uniform `z,u,v∈{0,...,m−1}`. Choose leaf z. In each ancestor
block of size w, select offset `u mod w` on rows and `v mod w` on columns.
Select u in every size-m row anchor/dummy block and v in the column blocks.
At a root the position is the axis seed; at a shared leaf it is z.

For a variable position in a size-w block, w leaves and m/w offsets yield
the given position. Fixing an opposite anchor/dummy coordinate fixes the
other seed. Every protected such cell has m preimages among m³ seeds.
Two anchor/dummy endpoints or two root endpoints likewise fix the two axis
seeds and leave the leaf free. The diagonal shared leaf has m² preimages
and probability 1/m, so it is deliberately unprotected. Correlations within
an axis do not invalidate the union bound or path propagation.

The mixer and fiber statements are now Lean theorems. Identifying every
protected host cell with the appropriate fiber and connecting the sampler
to an arbitrary repair remain formal proof obligations.

## Next decisive steps

1. Encode copies by their localized zero and the remaining six indices,
   deriving the coarse copy bound `2mn⁶` from the checked `|T_h|≤2m`.
2. Instantiate protected sampling and designated-body extension for an
   arbitrary edited binary matrix, proving the `m²` edit lower bound.
3. Combine the copy and repair bounds and prove the final statement for
   every positive real c,C. Exact enumeration can follow.

The original full 61-module upstream development has not been rebuilt here.
Generic modules were adapted selectively with source headers and attribution;
their theorem count is not a count of new mathematical contributions.
