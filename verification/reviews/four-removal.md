# Separate-agent semantic review: coarse counting and arbitrary repairs

Date: 2026-10-11. Reviewer: `/root/four_proof_reviewer`.
Candidate checkout: `.context/ordered-binary-matrix-removal`, branch
`shea256/four-removal-theorem`.

**Verdict:** the inspected counting, guarded-repair, distance-meaning,
normalization, asymptotic, and final capstone statements have the required semantics. I found
one mechanical 65-to-3 adaptation error in an intermediate anchor-extension
proof; the implementation agent corrected it. I found no remaining mathematical
counterexample in the reviewed chain. The final concrete-to-sequence capstone
uses both bounds for the same actual matrix and leaves no structural or
host-existence assumption in the removal theorem.

This is a separate-agent adversarial semantic review, **not independent peer
review, a Lean compilation report, an axiom audit, or universal certification
by finite testing**. Files were being implemented and built during review.
I did not edit implementation files, publish, or commit anything. The result
remains classified as candidate under the project instructions. This pass does
not establish novelty or formalize the manuscript's stronger exact copy count
or canonical sampling consequence.

## Scope and provenance

I reread the root and candidate `AGENTS.md`, the four-by-four manuscript's
counting/repair/conclusion sections, and the baseline model and strongest
recorded bounds. I inspected the pinned upstream modules underlying the
proposed adaptation, including `Model`, `CopyBound`, `SamplingAvoidance`,
`SamplingDistance`, `BodyExtension`, `GuardedFrame`, `GuardedPath`,
`PathPropagation`, the concrete path/sampling/order/repair chain,
`SequenceAssembly`, `Asymptotics`, and `Consequence`. All 78 locally cached
source files match the SHA-256 values in `verification/source_manifest.json`
for upstream commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

The three-seed sampler, Boolean propagation, coordinate-deletion encoding,
finite union bound, and asymptotic method are inherited from that upstream
implementation. In particular upstream already contains `ThreeSeedSampling`.
The proposed advance is the fixed 4×4 pattern and its concrete all-copy
localization, not a new repair-sampling mechanism. I did not rerun a fresh
literature/novelty search in this module review.

Local modules inspected are `Model`, `CountingInjection`, `CoarseCopyBound`,
`BodyExtension`, `GuardedFrame`, `GuardedPath`, `PathPropagation`,
`HostAnchorFrames`, `HostRootLeaf`, `HostSampledPath`, `HostSampledSelection`,
`SampledPath`, `SampledPathOrder`, `HostSampling`, `HostSamplingCompatibility`,
`GuardContainment`, `SamplingAvoidance`, `SamplingDistance`,
`HostRepairDistance`, `OrderedSampledSelection`, `OrderedRepairDistance`,
`DistanceMeaning`, `SequenceAssembly`, `Asymptotics`, `Consequence`, and `Main`.
I checked their interfaces against the previously reviewed concrete host,
independent orders, indexed matrix, and zero-set localization/cardinality.

## Findings and delicate interfaces

### 1. Correct model and fixed pattern

`Model.lean` defines copies by two **independent** strictly increasing maps
`Fin 4 → Fin n`, and matches every one of the sixteen binary entries. It does
not replace induced copies by one-entry embeddings or use a shared row/column
map. `fixedH_eq_H4` connects the removal pattern to the pattern used by the
prior localization modules. Direct expansion gives

```text
0 1 1 0
1 0 0 1
1 0 1 0
0 1 1 1
```

`HFree` is zero actual-copy count, and Hamming distance counts all unequal
cells of arbitrary binary matrices. No constraint protects anchor cells from
repair or restricts edits to one direction.

### 2. Coarse count and the changed localization witness

`CountingInjection.card_le_card_mul_pow` records the designated row-column
cell together with all other row and column coordinates. Equality of these
data recovers each increasing map; there is no omitted ordering or factorial
factor. Taking `k=3`, `i=2`, `j=3` gives six remaining coordinates and hence
`|L| n^6`.

`CoarseCopyBound.copyCount_le` (lines 17–35 of the reviewed snapshot) correctly
obtains the actual-copy equation from membership in `orderedCopies`, invokes
`matrix_zero_localization`, and transports the raw zero cell by **separate**
row and column equivalences. Its set is the image of the full `zeroCells h`.
The bound `card_image_le` suffices; equality of image cardinality is unnecessary.
Combined with `card_zeroCells_le`, this gives `2·2^h·n^6`.

This adaptation deliberately does not reuse upstream's single leaf-diagonal
witness. That witness is invalid for the additional unbalanced 4×4 copies.
The current proof retains the two positions of the parent-minus block and
therefore the necessary factor two. It also does not require the stronger
last-row theorem or exact enumeration. Height zero is allowed in the count;
there are no H4 copies there, whereas the repair sequence uses `h≥1`.

### 3. Anchor completion: intermediate error, corrected

**Severity: implementation blocker in an intermediate proof, now resolved.**
The first `BodyExtension.appendTwo_matches_fixedH` snapshot retained three
upstream case splits of the form `j.val = 2 ∨ j.val = 65` or
`i.val = 2 ∨ i.val = 65`, at lines 83, 87, and 93 in that snapshot. The index
3 in `Fin 4` refutes those disjunctions. I reported this immediately. A later
read confirmed all three second alternatives are 3. This was a proof-body
porting error; the theorem statement and pattern definition were already
correct. It is not evidence that an invalid theorem compiled.

The corrected extension uses two increasing anchor positions, both before
the two ordered body positions on their respective axes. The exact anchor
is `decide (u≠v)` and the four cross signatures are the two unit signatures.
With body `((1,0),(1,1))`, these give precisely `fixedH` in all four blocks.
`GuardedFrame.Valid` constrains the anchor and signatures but no body entry.
Its transfer lemma checks equality for zeros as well as ones. No anchor
rigidity theorem is needed for these designated embeddings.

### 4. Actual selected paths and the revised mode order

`HostSampledSelection.AxisConditions` isolates ten genuine ordering facts;
`OrderedSampledSelection.sampledAxisConditions` derives all of them from the
actual `rowIndex` and `columnIndex`. Thus the final repair theorem does not
leave an order certificate as an unproved hypothesis.

The raw mode encoding remains `6*i+k`, with kind IDs
`V+, V−, W+0, W+1, W−0, W−1`. This is correct: the changed **order** is supplied
by `modeRank`, not by changing those semantic kind IDs. The selected horizontal
mode uses the parity of the common child node. Both axes have that node even
though their within-block offsets use distinct seeds. The four body orders
agree with the manuscript, including the shared-leaf edge:

| Mode | Body rows | Body columns |
| --- | --- | --- |
| V+ | child-plus, parent-plus | dummy, parent-plus |
| V− | parent-minus, child-minus | dummy, parent-minus |
| W+ | child-plus, dummy | parent-plus, child-plus |
| W− | child-minus, dummy | child-minus, parent-minus |

Anchor groups are increasing within a fixed mode and precede all nonanchors.
The changed order among modes does not affect designated frame completion.
The path is total by repeating the shared leaf beyond `h`; only indices
`i≤h` and edge indices `i<h` are used. The modulo-defined edge extension has
the required `h≥1` hypothesis and equals the actual edge inside that range.

`HostSamplingCompatibility.atLevel_eq_mixFin` identifies the arithmetic path
sampler with the previously formalized equivalence-based fiber sampler. This
is an actual equality, not an assumption that two sampling descriptions are
interchangeable. The local three-seed law differs from the manuscript's larger
independent-choice product law, but proves the same existence-of-clean-guards
step. It is an inherited alternate proof, not a claim that the two joint laws
are equal.

### 5. Arbitrary repairs and guard frequencies

`GuardedPath.Selection.guards` includes roots, dummy incidences, and each
selected frame's anchor and signature cells. It omits other variable-variable
body cells. `GuardContainment` proves every actual guard is both protected
and selected. Protection means at least one anchor/dummy endpoint, or two
depth-zero variable endpoints. `HostSampling.selected_fiber_card` gives
exactly `m` of the `m³` seeds for every protected cell; a guard event is a
subset of that event and therefore has frequency at most `m`.

Correlating all anchor representatives on one axis via the same seed is
harmless. The two axes still use different offset seeds, and the union bound
does not require independence between different edited cells. Even when a
cell belongs to several frames, the guard is a finite **set**, so a changed
cell is charged once. There is no factor for the number of modes, groups,
levels, or frame incidences.

`SamplingDistance.hammingDistance_ge_of_guard_sampling` (lines 29–49) begins
with the full set of cells where arbitrary `A` and `B` disagree, not an
assumed protected edit set or an original-copy hitting set. If its size is
less than `m²`, finite avoidance provides a sample with no changed guard.
Transfer preserves the selected frames, roots, and dummy ones in `B`.
`PathPropagation.exists_modeBody` then forces some body in `B`: the four
avoidance implications would otherwise propagate opposite root bits to the
same final cell. Completing that body with its unchanged designated frame
produces an actual ordered H4 copy. Unprotected entries may have changed in
either direction throughout this argument.

`OrderedRepairDistance.hammingDistance_ge` consequently has only `h≥1`, an
arbitrary binary repair, and its H4-freeness as premises. Its source matrix
is `SelectedAnchor.matrix (rowIndex h) (columnIndex h)`, definitionally the
same raw-host reindexing as `Concrete.matrix h`; the final capstone correctly
uses this equality when combining the two integer bounds.

### 6. Sentinel minimum is the real repair minimum

`DistanceMeaning.zero_HFree` uses the required one at zero-based `(0,1)` to
show the all-zero matrix is H4-free for every `n`, including zero. Every
Hamming distance is at most `n²`. Therefore the minimum of the finite image
defining `fixedMinEdits` is at most `n²`, and the nonfree sentinel `n²+1`
cannot attain it. `exists_optimal_repair` extracts a minimizing **free**
matrix, while `fixedMinEdits_le_repair` gives minimality against every free
repair. These statements settle the semantic issue completely.

`SequenceAssembly.fixedMinEdits_ge_of_repairs` only needs its explicit
`q≤n²` hypothesis to handle the sentinel branch. The subsequent use sets
`q=m²`, `n=dm`, and proves this inequality using `d,m>0`. No hidden existence
or division-by-zero condition is used in the final positive-size sequence.
The size-zero normalization convention is irrelevant to the final `n≥1`
statement, and is not used to manufacture a counterexample.

### 7. Normalization and final quantifiers

The two normalization identities are exactly

```text
m² / (dm)² = d⁻²,
(2m (dm)^6) / (dm)^8 = 2 d⁻² / m.
```

They require positive `d,m`, both supplied. With `d=14h+2` and `m=2^h`, the
coarse ratio to `epsilon_h^C` is
`2 (14h+2)^(2C−2) 2^(−h)`, which tends to zero for each fixed real `C`.
`Asymptotics` uses a natural exponent `k≥C`, the bound `14h+2≤16h` for
`h≥1`, and the correct inequality `epsilon_h^k≤epsilon_h^C` for
`0<epsilon_h≤1`. Its factor-two theorem explicitly applies the preceding
decay theorem with `c/2`; no constant is silently discarded.

`Consequence.no_polynomial_removal_bound_of_sequence` preserves
`∀ c,C>0, ∃ n≥1, ∃ epsilon∈(0,1), ∃ A` with distance at least epsilon and
strictly fewer than `c epsilon^C n^8` copies. The fixed pattern does not
depend on either constant. The epsilon parameter varies with the chosen
depth, so the conclusion does not contradict qualitative removal at a
fixed positive epsilon. Ignoring the extra hypothesis `C>0` inside the
analytic proof is legitimate: the analytic estimate is stronger and holds
for all real exponents.

The conditional `SequenceAssembly` and `Consequence` modules do not by
themselves assert existence of concrete hosts. `Main.concrete_host_bounds`
(lines 11–15) explicitly instantiates both estimates for `Concrete.matrix h`.
`Main.counterexample_sequence` (lines 18–28) supplies that very matrix at
every `h≥1`, and `Main.no_polynomial_removal_bound` (lines 31–39) removes the
sequence hypothesis entirely. No separate matrix is used for the repair
bound versus the copy bound, and no structural certificate remains as a
premise of the final theorem.

The additional `Main.no_polynomial_removal_bound_arbitrary_repairs`
(lines 43–59) correctly spells out the repair quantifier as
`∀ B : BinaryMatrix n, HFree fixedH B → epsilon*n² ≤ hammingDistance A B`.
It derives this from `fixedDistance_le_repair` and the strictly positive
denominator justified by `n≥1`. This is the literal unrestricted repair
statement; there is no monotonicity, anchor-preservation, original-copy
hitting, or restricted-repair assumption hidden in the capstone.

## Executed exact finite audit

The standalone standard-library checker `.context/reviewer-removal-checks.py`
imports **no candidate implementation**. It reconstructs actual positions,
recursive row/column orders, entries, roles, and every three-seed selection
directly from the manuscript description. It checks all selected anchor and
signature entries against the literal H4, all four body orders per edge,
root values, dummy ones, shared leaves, and containment of every actual guard
in the protected selected event. It then counts each guard cell's frequency
over all seeds. It also checks both normalization identities with exact
fractions.

Reproduction from the root workspace:

```sh
python3 .context/reviewer-removal-checks.py > .context/reviewer-removal-checks-output.json
```

Executed under Python 3.9.25, exit code 0:

| h | Seeds | Frames checked | Distinct guard cells | Guard incidences | Maximum frequency |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 8 | 32 | 288 | 448 | 2 |
| 2 | 64 | 512 | 2,240 | 6,912 | 4 |
| 3 | 512 | 6,144 | 13,312 | 81,920 | 8 |
| 4 | 4,096 | 65,536 | 70,656 | 868,352 | 16 |

Each maximum is `m`, as required. The check includes substantial numbers of
zero-valued guards (200, 3,136, 37,376, 397,312 incidences respectively), so it
would not pass by preserving only ones. The negative control counts a fixed
unprotected common-leaf diagonal in `m²` samples, strictly above `m`. It
confirms the necessity of restricting the frequency claim to protected
cells. These checks do not enumerate all arbitrary repairs and do not prove
the universal theorem; the arbitrary-repair conclusion is supported by the
semantic argument above and the separately implemented formal proof.

## Reviewed snapshots and validation

SHA-256 hashes for all 26 newly inspected modules, the independent checker,
and its actual output are recorded in `.context/reviewer-removal-snapshots.json`.
Selected integration snapshots:

| File | SHA-256 |
| --- | --- |
| `Model.lean` | `1fa8211ce68801b690d85faefea98efb7eba3598ccf4d4e9f4ca7067df528644` |
| `CoarseCopyBound.lean` | `dcf1560b906f819f11804fea10f1f79d1fb9b24bc631f3dfdb599b84ac98a2ee` |
| corrected `BodyExtension.lean` | `3be744564f075a04014f35c87e74dd52fd51663580d5f4d70d7030794277b501` |
| `DistanceMeaning.lean` | `64e5bc043b407d0b02e4e890f522d1d6608a1e98cc3491cf13b84c6bed740a1a` |
| `SequenceAssembly.lean` | `6cc9ac077030b905464dd442cfdd75f7cea56c35c02a526d13af7ebd4ee69866` |
| `Asymptotics.lean` | `8b885c33754c9169d4f958c5514f0bfa67003110874db253937c511c8e4b84a9` |
| `Consequence.lean` | `d2c36fc14b7cd3345722d5518880d613e84bccb2f47d28019e38b62ce8bd9838` |
| `Main.lean` | `6721fd9a1da6c2229705bf42ab5c279e033a88f6c1a9de8e46e5ef7943ac1f80` |

Root validation `python3 scripts/validate_repository.py` passed: 34 tracks
in 7 groups; 376 local links across 108 Markdown files. The nested project's
required `python3 scripts/run_checks.py` completed all eight mathematical
checks and exact reference comparisons successfully (`compression`,
`adversarial`, `refinement`, `four`, `four_repair`, `four_literal`,
`four_reviewer`, `four_localization`). It then exited 1 in the repository
validator at the assertion that the stored hash for
`formal/OrderedRemoval.lean` matches its current contents. The import root
was being updated during the active implementation. This is a validation
blocker until metadata is refreshed, not a failed finite mathematical check.
I did not alter the metadata or claim an overall project-check pass.

The exact command was run from the candidate checkout:

```sh
python3 scripts/run_checks.py > /home/vercel-sandbox/open-math-problems/.context/reviewer-removal-project-checks.log
```

The stdout log is preserved at `.context/reviewer-removal-project-checks.log`
in the root workspace. The tool returned this concluding error on stderr:

```text
File "scripts/validate_repository.py", line 41, in <module>
  assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
AssertionError: formal/OrderedRemoval.lean
```

Compiler success and theorem axiom reports remain the implementation agent's
separate evidence, not claimed here. Exact enumeration, the canonical-sampler
statement, novelty, and independent mathematical peer review remain outside
this capstone's scope.

## Packaged artifact locations

The reviewer-authored checker is preserved byte for byte at
[check_four_removal.py](../check_four_removal.py), its actual output at
[four-removal-report.json](../reference/four-removal-report.json), and its original
snapshot manifest at [four-removal-snapshots.json](four-removal-snapshots.json).
The workspace paths above identify the original execution. From this repository
root, reproduce with `python3 verification/check_four_removal.py`. The coordinating
agent separately records the completed Lean audit and package validation in
[RUNLOG.md](../../RUNLOG.md); the intermediate validation failure above is retained
as part of the review record.
