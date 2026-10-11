# Lean formalization of the 4×4 removal obstruction

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

The script builds the project and audits **every compiled project declaration's
transitive axioms**, matching each named source theorem to its owning module.
Only `propext`, `Quot.sound`, and `Classical.choice` are permitted. No added
axioms, admitted proofs, or native decision shortcuts are used. It replays
**each project module into its imported environment** using Lean's kernel.
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
