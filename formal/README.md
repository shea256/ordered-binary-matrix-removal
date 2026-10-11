# Lean verification of the 3×4 theorem

**The main theorem is checked end to end**, including arbitrarily small ε
and arbitrarily large square hosts at the same chosen ε. The pattern is
`1001/1010/0111`, with separately increasing row and column maps matching
all twelve binary entries. Every H-free binary repair is quantified over,
including anchor edits and changes in both directions.

The principal export is `OrderedRemoval.Rectangular.no_polynomial_removal_bound`
in [Complete.lean](OrderedRemoval/Rectangular/Complete.lean). For all real
c,C,ε₀>0, it chooses 0<ε<ε₀ such that, for every threshold N, there is an
n≥max(1,N) square host requiring at least εn² edits in every H-free repair
and containing fewer than c ε^C n⁷ ordered copies.

| Component | Checked conclusion |
| --- | --- |
| [Model](OrderedRemoval/Rectangular/Model.lean), [Host](OrderedRemoval/Rectangular/Host.lean), [OrderedHost](OrderedRemoval/Rectangular/OrderedHost.lean) | The literal 3×4 pattern, full host entry rule, global W−/W+/V order, and independent axis orders. |
| [AnchorClassification](OrderedRemoval/Rectangular/AnchorClassification.lean), [ZeroLocalization](OrderedRemoval/Rectangular/ZeroLocalization.lean) | Every copy has one anchor row and one or two anchor columns; its fixed zero belongs to the terminal parent-minus set. |
| [CoarseCopyBound](OrderedRemoval/Rectangular/CoarseCopyBound.lean) | Every copy is encoded by a cell in a set of at most 2m cells and five remaining indices, giving N_H≤2mn⁵. |
| [RepairDistance](OrderedRemoval/Rectangular/RepairDistance.lean) | Every H-free repair of the actual new host changes at least m² entries. |
| [Main](OrderedRemoval/Rectangular/Main.lean), [Blowup](OrderedRemoval/Rectangular/Blowup.lean), [Complete](OrderedRemoval/Rectangular/Complete.lean) | Normalization, exponential decay, and uniform blowup give the full quantifier order. |

The formal sampler selects from both m-sized subgroups of each 2m anchor
row block, then uses only the second row in copy completion. This differs
from the paper's uniform 2m representative; the per-cell bound is still
1/m². Blowup repair is proved by partitioning all cells into q² offset
slices. Distinct pattern rows and columns give the sufficient q⁷ upper
bound on the blowup copy count.

With the pinned Lean 4.34.1/Lake toolchain, from the repository root:

```sh
(cd formal && lake exe cache get)
python3 scripts/run_rectangular_formal_checks.py
```

The [source-bound audit](../verification/reference/rectangular-formal-audit.json)
checks every declaration in both historical and rectangular project modules,
including generated declarations, for transitive axiom dependencies. Only
`propext`, `Quot.sound`, and `Classical.choice` occur. Each module is replayed
into its imported Lean environment. This does not freshly replay all Mathlib.
The [separate-agent semantic review](../verification/reviews/three-by-four-formal.md)
checks agreement with the written theorem and is not independent peer review.
Exact all-depth enumeration, repair equality, and global minimality are
outside the certificate. The repository retains candidate status pending
independent mathematical review.

The following record concerns the older H4 proof only.

# Lean formalization of the 4×4 removal obstruction

**Scope after the October 11 ordering refinement:** the historical top-level Lean sources
use the previous within-depth order W+0,W+1,W−0,W−1,V+,V−.
They establish the qualitative theorem for the same H4, already known from
Erebos's earlier release. They do not certify the newly proposed global order,
its exact copy count, repair equality, or optimality statement. The source-bound
387-theorem audit remains a receipt for those unchanged historical sources.


**The qualitative theorem is formalized end to end.** For the explicit fixed
4×4 binary pattern, Lean proves that every proposed polynomial removal bound
fails. The construction uses independent increasing row and column maps and
allows every binary repair, including changes to anchors and both edit directions.
The overall research record remains **candidate** pending independent mathematical
review and a conclusive novelty assessment.

The sharper exact copy formula and the canonical sampler lower bound in the
manuscript are **not formalized**. The capstone instead uses the sufficient
coarse estimate `N_H(A_h) ≤ 2mn⁶`, together with the `m²` arbitrary-repair bound.
For `m=2^h`, `d=14h+2`, and `n=dm`, this gives distance at least `d⁻²` and
copy density at most `2d⁻²2⁻ʰ`. Exponential decay beats every fixed power of
the distance scale. The factor two is retained throughout the formal proof.

## Reproduce

With the pinned Lean/Lake toolchain available, from the repository root:

```sh
(cd formal && lake exe cache get)
python3 scripts/run_formal_checks.py
```

Lean is pinned to 4.34.1 and Mathlib to
`d13f23b723b8a846827a245b89c10fc7d3f11612`;
`lake-manifest.json` also pins transitive dependencies. The initial dependency
and cache download requires network access and substantial disk space.

The script builds the project and audits **every compiled declaration in the historical H4 modules
and its transitive axioms**, matching each named source theorem to its owning module.
Only `propext`, `Quot.sound`, and `Classical.choice` are permitted. No added
axioms, admitted proofs, or native decision shortcuts are used. It replays
**each historical H4 module into its imported environment** using Lean's kernel.
This does not freshly replay all Mathlib or use another proof assistant.
The earlier Std-only checkpoint had a different replay scope.

The source-bound receipt is written to `.context/formal-checks-receipt.json`;
the archived run is [formal-audit.json](../verification/reference/formal-audit.json).
The default Python suite validates this binding but does not execute Lean.

## Proof map

| Component | Checked conclusion |
| --- | --- |
| [Model](OrderedRemoval/Model.lean), [DistanceMeaning](OrderedRemoval/DistanceMeaning.lean) | Copies match all sixteen entries under separate increasing maps; the literal pattern equals the previously localized H4; minimum edit distance is attained by an actual H4-free binary repair. |
| [ConcreteHost](OrderedRemoval/ConcreteHost.lean), [OrderedHost](OrderedRemoval/OrderedHost.lean) | The actual host has `(14h+2)2^h` positions, the revised mode ordering, and separate row/column orders. |
| [AnchorCertificate](OrderedRemoval/AnchorCertificate.lean), [IndexedHost](OrderedRemoval/IndexedHost.lean) | Every concrete copy has anchor counts (2,2) or (2,1); no structural certificate is assumed. Height zero has no copies; an explicit height-one copy shows nonvacuity. |
| [ZeroLocalization](OrderedRemoval/ZeroLocalization.lean), [LastRow](OrderedRemoval/LastRow.lean), [ZeroSetSize](OrderedRemoval/ZeroSetSize.lean) | The fixed zero lies in the leaf-to-parent-minus set, the last selected row is dummy, and the set has at most 2m cells. |
| [CountingInjection](OrderedRemoval/CountingInjection.lean), [CoarseCopyBound](OrderedRemoval/CoarseCopyBound.lean) | Encode each copy by its fixed zero and remaining six indices to obtain `N_H ≤ 2mn⁶`. |
| [HostSampling](OrderedRemoval/HostSampling.lean), [GuardContainment](OrderedRemoval/GuardContainment.lean), [HostSamplingCompatibility](OrderedRemoval/HostSamplingCompatibility.lean) | Every protected edited cell is incident to at most m of the m³ three-seed selections. There is no extra factor for modes, levels, or roles. |
| [BodyExtension](OrderedRemoval/BodyExtension.lean), [GuardedPath](OrderedRemoval/GuardedPath.lean), [OrderedSampledSelection](OrderedRemoval/OrderedSampledSelection.lean) | A surviving selected path gives an ordered copy of the fixed H4 in an arbitrarily edited matrix; all host, order, and signature premises are discharged. |
| [OrderedRepairDistance](OrderedRemoval/OrderedRepairDistance.lean) | Every H4-free binary repair of the actual host changes at least m² cells for h≥1. |
| [SequenceAssembly](OrderedRemoval/SequenceAssembly.lean), [Asymptotics](OrderedRemoval/Asymptotics.lean), [Consequence](OrderedRemoval/Consequence.lean), [Main](OrderedRemoval/Main.lean) | Both estimates concern the same concrete host; normalization and decay yield the unconditional theorem for every positive real c,C. |

The principal export is `OrderedRemoval.no_polynomial_removal_bound`:
for every real `c,C>0`, there exist `n≥1`, `0<ε<1`, and a binary n×n matrix
whose normalized repair distance is at least ε and whose ordered H4-copy
count is strictly less than `c ε^C n⁸`.

`OrderedRemoval.no_polynomial_removal_bound_arbitrary_repairs` states the
same conclusion directly as `εn² ≤ hammingDistance A B` for **every** H4-free
binary matrix B. Neither capstone has a localization, sampling, host-existence,
or anchor-preservation premise.

## Inherited sampler and attribution

The three-seed sampler already appears in upstream
[ThreeSeedSampling.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Combinatorics/MatrixRemoval/ThreeSeedSampling.lean).
Take uniform `z,u,v` among m choices. Choose leaf z; in a size-w ancestor
block use row offset `u mod w` and column offset `v mod w`. Anchors and dummies
use the corresponding axis seed. Every protected cell has m preimages among
m³ seeds. The common-leaf diagonal has m² preimages and is deliberately
unprotected. The finite incidence bound does not require independent choices
at different depths. All of these connections are now formalized.

OpenAI's guarded-path, sampling, counting-injection, normalization, and
asymptotic modules were adapted selectively with attribution headers.
The original full upstream development has not been rebuilt. These inherited
arguments and their theorem counts are not new mathematical contributions.
See [ATTRIBUTION.md](../ATTRIBUTION.md).

The [host](../verification/reviews/four-concrete-host.md),
[localization](../verification/reviews/four-localization.md), and
[final theorem](../verification/reviews/four-removal.md) reviews examine
agreement between the Lean statements and intended mathematics. They are
separate-agent reviews, not independent mathematical peer review.

## Remaining scope

The exact zero-set cardinality, sharper exact copy formula (including its
h=1 exception), and canonical sampler asymptotics remain outside this formal
certificate. Independent mathematical review and novelty assessment remain
open. No global minimality claim for 4×4 is made.
