# Attribution and scope

## October 11 — 3×3 qualitative Lean theorem

The [new certificate](formal/README.md) proves the full theorem for the
3×3 crown using doubled anchor blocks and the coarse bound 2mn⁴. The
new anchor classification, suffix column order, five-cell completion, and
all-copy localization are connected to the inherited OpenAI tree,
three-seed sampling, propagation, counting injection, and asymptotic
arguments. Several arithmetic lemmas are reused directly from our 3×4
formalization. Module and theorem totals include inherited infrastructure
and should not be described as new mathematical contributions.

The [separate-agent review](verification/reviews/three-by-three-adversarial.md)
covers the original written proof snapshot. It did not examine this Lean
port. The written exact 7m⁴ formula and the smaller host's quantitative
parameters remain outside the formal certificate. Human peer review,
worldwide priority, and minimality are not established by the checks.

## October 11 — 3×3 crown candidate and further baseline correction

The [3×3 proof draft](proofs/three-by-three.md) uses OpenAI's signed tree,
role table, threshold body and arbitrary-repair propagation. It adapts
the nonuniform row supports developed for the preceding 3×4 construction.
The new encoding puts a single column anchor after the nonanchors and
adds dummy-row ones in vertical anchor columns. Its all-copy classification
and exact 7m⁴ count are written candidate claims, supported by two
same-agent implementations. That discovery checkpoint preceded the later
separate review and qualitative Lean certificate above. Independent
mathematical peer review remains pending.

The refreshed search found [Zinan Wang's 4×4 manuscript](https://github.com/wzn1118/h4-ordered-matrix-removal/tree/8c503f7a7a0f42c53621dcd0bdaf753e2580aa3e).
It states the same (5/2)m⁶−m⁵ count as our earlier 4×4 refinement, with
its own mode order and formal exact-count/repair claims. We found it
during this 3×3 attempt, not before our earlier discoveries. Its source
and finite census were checked; its Lean build was not rerun. Previous
bounded-search descriptions must not imply that matching count occurs
only in our work. See [BASELINE.md](BASELINE.md) for versions and scope.

This release packages the 3×3 result in a user-authorized PR. No
social announcement or author contact has been performed. Older checkpoint
statements below are historical.

## New asymmetric 3×4 candidate — October 11

The [new proof](proofs/three-by-four.md) inherits OpenAI's binary tree,
threshold body, mode roles, protected-path sampling, and four-step
propagation. It uses the global mode order explored in the preceding
local H4 refinement. The new construction replaces two anchor row groups
with one, while adding W-dummy ones and parity-dependent nonterminal
minus-child ones. Its new all-copy classification proves a 3×4 obstruction.
Erebos's earlier H4 and formalization remain the external pattern baseline;
no priority claim for H4 is restored. Erebos's exact repair upper bound
is not transferred or needed for the new theorem.

The coordinating agent discovered the rule and wrote the candidate proof
and two check implementations. The existing user-authorized reviewer
agent separately analyzed the proof and wrote another checker. This is
separate AI review, not independent mathematical peer review. The new Lean
formalization adapts the inherited path and sampling framework to the rectangular
pattern and proves the new localization and full removal theorem. Its uniform
blowup proof uses offset slices to handle arbitrary repairs. No Erebos Lean code
is copied. The user-authorized draft PR is the review channel; no social
announcement or author contact has been performed.


## Previous checkpoint record

# Attribution and scope

## Prior-work correction and current contribution — October 11

[Erebos v1.0.0](https://github.com/erebos-labs/ordered-matrix-removal-4x4/releases/tag/v1.0.0) already gives the same H4, complete
localization, and qualitative Lean theorem; [v1.1.0](https://github.com/erebos-labs/ordered-matrix-removal-4x4/releases/tag/v1.1.0)
adds exact repair via the terminal-anchor edit. [ProveIt](https://github.com/VladimirReshetnikov/ProveIt/tree/bfbfe915186310fdf745a7a089e7dd88eeb773b1/Combinatorics/OrderedMatrices/Research/ordered-matrix-removal) earlier gave a
5×5 obstruction, exact repair and sampling results, and the explicit H4 candidate.
Both sources preceded our 4×4 PR and were missed by our initial search. We do
not imply we consulted them before that discovery. Older novelty descriptions
below are historical and superseded by this correction.

The current manuscript proposes a global anchor-mode ordering and the exact
count (5/2)m⁶−m⁵, optimal over the stated block-permutation class. Its repair
upper bound explicitly adapts Erebos's terminal-anchor argument. The tree,
propagation, sampling and blowup mechanisms remain inherited. No Erebos Lean
code is copied into the unchanged local Lean project; the new refinement is
not yet formalized. New coordinating-agent and separate-reviewer checks have
distinct implementations but are not independent mathematical peer review.


Author: Ryan Shea. Developed with Codex assistance. A separate Codex reviewer
audited the 4×4 argument; this is not independent mathematical peer review.
No specific model configuration is claimed by this package.

The construction adapts OpenAI, *Polynomial removal fails for ordered binary
matrices*, September 25, 2026, pinned at
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` in
[openai/math](https://github.com/openai/math). Its tree host, sign chains,
four-step propagation, sampling argument for arbitrary repairs, and diagonal
leaf localization are inherited. The original source repository is licensed
under Apache 2.0. The pinned [source manifest](verification/source_manifest.json)
records provenance; upstream files are fetched into an ignored cache.

The first proposed contribution was a three-column nonshattering argument
and a 13×13 anchor yielding a 15×15 pattern. The next candidate used
three-row crown exclusion and ordered laminar supports to make a 3×3
anchor rigid, yielding a 5×5 pattern. The current 4×4 candidate uses a
2×2 anchor without pure anchor rigidity. Its proposed new contributions
are the full-pattern anchor classification, leaf-to-parent zero-cell
localization, and exact enumeration of the additional copy families.
The arbitrary-repair argument remains inherited. The exact 4^−h decay
also follows for the original construction and is not a new mechanism.

These proof drafts and verification scripts were prepared for this research
track. The current manuscript describes the 4×4 candidate; the 5×5 and
15×15 drafts and exact reports are retained for provenance. Companion
literature and the unresolved novelty check are recorded in
[BASELINE.md](BASELINE.md). The qualitative 4×4 removal theorem now has a
Lean certificate; the sharper exact count and canonical sampler bound do not.
Independent acceptance is not asserted.

The [separate-agent report](verification/reviews/four-separate-agent.md)
and its checker retain reviewer provenance. The coordinating agent wrote
the additional literal checker and the new formal bridges. Generic host,
order, and sampling modules were adapted from the pinned upstream Lean
sources with attribution headers. In particular, the three-seed sampler is
already present in upstream `ThreeSeedSampling.lean`; neither it nor the
propagation/sampling methods are new mathematical contributions.
The full original upstream development has not been rebuilt. Actual formal
coverage is described in [formal/README.md](formal/README.md).

## End-to-end certificate — 2026-10-11

The added upstream adaptations are `Model`, `CopyBound` (renamed
`CountingInjection`), `SamplingAvoidance`, `SamplingDistance`, `BodyExtension`,
`PathPropagation`, `GuardedFrame`, `GuardedPath`, `GuardContainment`,
`HostSampling`, `SampledPath`, `HostSampledPath`, `SampledPathOrder`,
`HostRootLeaf`, `HostAnchorFrames`, `HostSampledSelection`,
`HostSamplingCompatibility`, `HostRepairDistance`, `OrderedSampledSelection`,
`OrderedRepairDistance`, `SequenceAssembly`, `Asymptotics`, and `Consequence`.
All derive from the pinned Apache-2.0 source manifest. Namespace and host
interfaces are adapted to the local construction; two anchor groups and four
pattern positions replace 64 and 66. The sequence has coefficient 14, copy
normalization exponent 8, and the required factor two in the coarse bound.

`CoarseCopyBound` connects the previously checked local zero set to the generic
encoding. `DistanceMeaning` verifies that the sentinel minimum denotes an
actual optimal repair. `Main` discharges the concrete-host premises and gives
the final theorem, including an explicit arbitrary-repairs variant. The local
all-copy classification/localization supplies the essential refinement over
the baseline; the sampling/propagation/decay machinery is inherited.
