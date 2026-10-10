# Partial Lean formalization of the 4×4 argument

**Status: partial, with concrete anchor classification proved.** Lean 4.34.1
now checks the actual binary host, its independent row and column orders,
and the theorem that every ordered H4 copy has anchor counts **(2,2) or
(2,1)**. No structural certificate is assumed by that theorem. Localization,
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
The [separate-agent semantic review](../verification/reviews/four-concrete-host.md)
checks agreement with the manuscript. It is not independent peer review.

## What is proved

| Component | Checked statement | Remaining connection |
| --- | --- | --- |
| [ConcreteHost](OrderedRemoval/ConcreteHost.lean), [TreePositions](OrderedRemoval/TreePositions.lean), [AnchorFrames](OrderedRemoval/AnchorFrames.lean), [OrderedHost](OrderedRemoval/OrderedHost.lean) | The finite binary host has `(14h+2)2^h` positions, shared leaves, the revised mode ranks, and two independently enumerated axis orders. | Use these definitions in the remaining localization and repair arguments. |
| [HostStructure](OrderedRemoval/HostStructure.lean), [RoleSupports](OrderedRemoval/RoleSupports.lean), [ConcreteCopies](OrderedRemoval/ConcreteCopies.lean) | Concrete crown exclusion, same-class comparability, forward support containment, twin exclusion, and dummy exclusions. | These structural facts are already connected to anchor classification. |
| [ExtractAnchors](OrderedRemoval/ExtractAnchors.lean), [AnchorCertificate](OrderedRemoval/AnchorCertificate.lean), [IndexedHost](OrderedRemoval/IndexedHost.lean) | Every actual ordered copy supplies the certificate and has counts (2,2) or (2,1). The indexed matrix interface assumes only increasing index maps and the sixteen H4 entries. No copies at height zero; an explicit balanced copy at height one. | Localize the fixed zero in both surviving cases. |
| [HostTreeOrder](OrderedRemoval/HostTreeOrder.lean), [LocalArithmetic](OrderedRemoval/LocalArithmetic.lean) | Four concrete parent/child order equivalences and the conditional arithmetic contradictions for localization. | Extract the complete balanced and unbalanced case hypotheses from actual copies. |
| [ThreeSeedSampling](OrderedRemoval/ThreeSeedSampling.lean) | The inherited finite sampler, root/leaf and ancestor identities, and exact mixer fiber counts. | Instantiate the protected-cell incidence bound for edited host cells. |
| [Propagation](OrderedRemoval/Propagation.lean), [ProtectedSampling](OrderedRemoval/ProtectedSampling.lean) | Arbitrary-depth Boolean propagation and a finite union bound under explicit incidence hypotheses. | Extend the resulting body to an ordered H4 copy in an arbitrary edited matrix. |

The key exports are `OrderedRemoval.Concrete.Copy.anchor_counts` and
`OrderedRemoval.Concrete.matrix_anchor_counts`. Their quantifiers cover all
natural depths and all ordered copies in the concrete host. The proof is
not an enumeration of finitely many depths. The original conditional
`AnchorClassification.anchor_counts` remains a reusable intermediate lemma.

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

1. Derive the complete balanced/unbalanced arithmetic cases and prove that
   every copy's fixed zero lies in the leaf-to-parent-minus set `T_h`.
2. Instantiate protected sampling and designated-body extension for an
   arbitrary edited binary matrix, proving the `m²` edit lower bound.
3. Combine localization with the coarse copy bound `2mn⁶` and prove the
   final statement for every positive real c,C. Exact enumeration can follow.

The original full 61-module upstream development has not been rebuilt here.
Generic modules were adapted selectively with source headers and attribution;
their theorem count is not a count of new mathematical contributions.
