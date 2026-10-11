# Separate-agent adversarial audit of the 4×4 candidate

Date: 2026-10-10. Reviewer task: `/root/four_proof_reviewer`.

## Verdict and scope

**I found no mathematical error or missing universal case in the written 4×4 argument.** In particular, I could reconstruct the full anchor-count classification, both localization branches, the exact enumeration, and the arbitrary-binary-repair lower bound from the host definitions. The previously delicate unbalanced branch survives this adversarial pass. I found no counterexample.

This is a separate-agent audit within the same research session. It is **not independent peer review**, an end-to-end Lean proof, or a proof of novelty. The candidate classification should remain. Finite non-findings do not certify the all-depth theorem; my favorable assessment of the universal argument comes from the case analysis below, subject to ordinary reviewer fallibility.

I did not modify the proof, manuscript, metadata, or existing verification scripts. My artifacts are this report, [reviewer-four-localization.py](../check_four_reviewer.py), and its [actual output](../reference/four-reviewer-report.json). The scratch program imports no candidate-package code. I also ran the required existing checks, as recorded below.

The audited snapshots were:

| File | SHA-256 |
| --- | --- |
| `proofs/four-by-four.md` | `9e8816dd5d37aa086c732c80e3f3312d3b7dcdbad13ed2e4c978da11206baaa1` |
| `manuscript.md` | `46ecfd922ce79522516cd6a1affc668c6123bc73d215d374a4293be72e9b209f` |
| `BASELINE.md` | `2d4f9972f97300dbbbe75a2f31b7a45223363c511be6e8f79957096dc018f27b` |

Line references below refer to that 525-line standalone proof snapshot. Its text from “Statement and explicit pattern” through the mathematical argument was byte-for-byte present in `manuscript.md`, so there was no separate mathematical-text discrepancy in the manuscript. Other work by the parent agent may subsequently change verification sections and line numbers.

## Findings by severity

| Severity | Finding | Evidence / location |
| --- | --- | --- |
| Fatal / major | None found. | All steps discussed below. |
| Minor correctness | None found. | The depth-one exception, disappearing depth-two half-class contribution, and leaf sign identification are handled correctly. |
| Optional exposition | Spell out that `A=B` in the unbalanced branch forces the first anchor row into group 1. | Lines 291–307 and 383–385. This already follows from the second anchor row being group 2, increasing row order, and twin exclusion; the enumeration uses it correctly. |
| Optional exposition | Mention that the parent-half family exists as a support at `h=2` but contributes zero there; it first contributes at `h=3`. | Lines 367–392. The formula already gives zero correctly. |
| Optional model precision | State that the canonical sampler chooses uniform `q`-element subsets with `0≤q≤n`, if that is the intended convention. | Lines 487–503. The stated bound also holds for independent draws with replacement by a union bound, but exact marginal equality is clearest for subsets. This does not affect the removal theorem. |
| Verification / novelty boundary | Human independent review, complete formalization, and conclusive novelty assessment remain outstanding. | These are accurately labeled as outstanding in the audited snapshot. This report does not remove them. |

None of the optional exposition points is a gap requiring a new mathematical lemma.

## Baseline and contribution check

I accessed the pinned [primary contents](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/CONTENTS.md), the manuscript's [introduction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-removal-fails-for-ordered-binary-matrices-September-25-2026/build/sections/01-introduction.tex), [copy-localization section](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-removal-fails-for-ordered-binary-matrices-September-25-2026/build/sections/03b-count.tex), and [arbitrary-repair proof](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-removal-fails-for-ordered-binary-matrices-September-25-2026/build/sections/04-distance.tex). The #190 contents entry has one manuscript. The GitHub API returned main commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, timestamp `2026-10-08T05:20:00Z`, during this audit. No newer repository correction was thereby indicated.

The original theorem uses a fixed 66×66 binary pattern, `n=(386h+2)2^h`, distance at least `(386h+2)^−2`, independent increasing row/column orders, and arbitrary binary edits. Its localization section also implies the stronger exact count `2m^130`: choose the leaf, the dummy row, one of the two parent-minus column positions, and 128 anchor coordinates. Thus the stronger derived density `2(386h+2)^−132 4^−h` in `BASELINE.md` is consistent with the primary proof. The current candidate's contribution is smaller pattern size, not a new decay mechanism or arbitrary-tester lower bound.

I ran two additional searches: `"Polynomial removal fails for ordered binary matrices" correction smaller 4x4` and `"ordered binary" "removal" "4" 2026`. They did not identify a stronger direct primary follow-up. This is a limited novelty screen. I did not independently re-audit every adjacent older theorem or rebuild the original 61-module Lean development; the existing baseline's descriptions of those results are not upgraded by this pass.

## Attacks actually executed

1. **Find an omitted anchor configuration or a nonleaf unbalanced copy.** I partitioned all 25 anchor-count pairs and reconstructed the role/support restrictions. I then independently implemented the role sets and host entries and enumerated relaxed unbalanced configurations through depth seven, retaining fewer conditions than a full copy. The only survivors still localized to the claimed parent-minus zero cells.
2. **Break the enumeration at leaf-sign collisions or short depths.** I independently derived the four families and multiplicities, then restored `c2` and every possible later `r4` in the scratch check. This tested the dummy-row conclusion and unbalanced counts without presupposing either. It found zero unbalanced copies at `h=1`; the parent-half family is absent from the count at `h=2` and appears at `h=3`.
3. **Defeat the repair lower bound by correlated leaf samples or anchor edits.** I reconstructed the probability space and identified exactly which edited cells are protected. The two variable axes are correlated, but every protected cell has the asserted `m^−2` selection probability. The proof never needs this probability for general variable-variable cells. The four implications then force an actual contradiction in the edited matrix, even when all unprotected entries are arbitrary bits.

These are executed mathematical attacks, supplemented by exact finite code for the first two; they are not merely proposed tests.

## Host definitions and prerequisites

### Binary host, sizes, and order

Lines 70–126 define a consistent host. Shared leaf signs create no conflicting entry assignment: the own-minus rule excludes the leaves, while the two transition rules target different parent signs. There are `12h` size-`m` anchor groups, `2h+1` size-`m` variable classes, and one dummy class per axis. This gives exactly `(14h+2)m` positions.

Rows and columns have different recursive traversals. I checked the use of their directions: row minus comes first and row plus last, while column plus comes first and column minus last. The immediate parent/child inequalities in lines 130–141 and the strict comparisons in lines 219–230 follow from that traversal, including leaves. For columns in the same block, the argument uses weak inequalities between node labels when needed; identical block entries prevent a zero/one transition inside that block.

Both the four rows and the four columns of `H` are distinct. Therefore a copy cannot select two actual positions in the same global twin block. Node blocks and anchor groups are global twin blocks because every rule, including parity signatures, is constant inside each one. The larger depth/sign classes need not be global twin blocks; the proof does not treat them as such.

### Lemma 1: comparability and crown exclusion, lines 150–183

On nonanchor columns, row entries within a fixed level/sign class decrease with the node index; on nonanchor rows, column entries within a fixed level/sign class increase with the node index. Thus the relevant one-sets are nested. This statement is deliberately restricted to nonanchor opposite coordinates; anchor parity signatures could otherwise destroy nesting. All subsequent comparability applications respect the restriction.

In a crown `Q`, each pair of columns has both traces `10` and `01`, so their classes must be distinct. A dummy column cannot participate because it would have no zero. Each required pair of one-entries must come from a nondummy row and therefore lie on an edge of the two sign chains with the terminal triangle. The only triangle is `{L,(h−1,+),(h−1,−)}`.

For that triangle, only leaves can supply the two traces with a one in the leaf coordinate. As the leaf index `p` increases, all three threshold indicators decrease. Their trace vectors are a chain, whereas `110` and `101` are incomparable. Nonleaf rows have zero on every leaf column, and dummy rows give `111`, so neither supplies the missing trace. This argument works at `h=1`; it does not assume a nonempty interior chain.

### Lemma 2: role supports, lines 185–213

Each support lies in a single whole class or one parity half. At the leaves, plus and minus halves coincide when their parity coincides; they do not partially overlap in a new way. The only strict containment is half-in-whole, and the mode table puts every containing whole support later.

The distinction between axes matters. On the row axis, a depth-`i` half can be contained by `V_i` or `V_(i+1)`. On the column axis, the relevant whole supports occur only at `i+1`. There is no whole leaf support on the column axis because level `h+1` modes are absent. Dummy supports are separate from variable classes. These observations validate the later nonleaf-minus exclusion and the count's list of possible first anchor rows.

## Full anchor-count classification

For clarity, the complete `(a,b)` partition is as follows. `Q` denotes the nonanchor crown contradiction; `C` a same-class comparability contradiction; `L` an earlier-proper-container contradiction; and `X` alignment into one two-group mode followed by exclusion of any further anchor.

| Anchor rows `a` \ anchor columns `b` | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| 0 | Q | C | C | L | L |
| 1 | Q | C | C | L | L |
| 2 | C | allowed | allowed | X | X |
| 3 | L | L | X | X | X |
| 4 | L | L | X | X | X |

The actual witnesses, lines 240–261, check out:

- When `a≤1,b=0`, rows `2,3,4` and columns `1,3,4` are nonanchor and form a crown up to row permutation.
- When `a≤1,b∈{1,2}`, column 1 forces rows 2 and 3 into one role support, hence one class; nonanchor columns 3 and 4 give the forbidden opposite traces.
- When `a≤1,b≥3`, anchor columns 1 and 3 have traces `11` and `01` on nonanchor rows 2 and 3. Their supports intersect, and one contains the other strictly in the wrong mode order.
- When `a≥3,b≤1`, anchor rows 1 and 3 have the same offending pair of traces on nonanchor columns 2 and 3.
- When `a=2,b=0`, anchor row 2 puts columns 1 and 4 into one class, while nonanchor rows 3 and 4 distinguish them by opposite traces.
- When `a,b≥2`, the crossed ones force equality of all four first-two mode labels by the displayed inequality cycle. Twin exclusion forces each axis to use its two groups once. Every extra anchor is in a later mode and gives `00` against the opposite anchors, which neither remaining row nor remaining column of `H` permits.

The proper-containment arguments also handle equal mode labels: roles of one mode are disjoint, so intersecting supports with different traces cannot be two same-mode roles. This closes a possible loophole in using non-strict mode ordering.

## Localization

### Balanced copies, lines 273–289

The signatures identify the four designated body roles in the common mode. Recomputing the four body cases gives:

- `V_i+`: `π(p)≤a≤b`, forcing the allegedly zero top-right entry to one.
- `V_i−`: `π(p)≥a≥b`, forcing the allegedly one bottom-right entry to zero.
- `W_i+`: `π(p)≤b≤π(q)` and equal parity force `p≤q`, again making the top-right entry one.
- `W_i−`: `π(p)≥b≥π(q)` and equal parity force `p≥q`. For `i<h` the own-minus entry cannot be one. For `i=h` the shared leaf entry uses `≤`, and its being one forces `p=q` and `b=π(p)`.

The last mode has dummy row role 2. Its fixed `(3,4)` entry is the claimed zero. No depth-one exception occurs in these implications.

### Unbalanced orientation and class reduction, lines 291–307

The one at `(2,1)` forces a common mode `B` and opposite anchor groups. The orientation “second row group 1, first column group 2” would place `(r3,c4)` in row role 2 × column role 1. In every `V` mode the column is dummy, and in every `W` mode the row is dummy. Its entry would be one. Therefore the sole possible orientation is row group 2, column group 1.

Consequently `r3` is in row role 1 of `B`, `c4` is in column role 2, and their entry is zero. The first anchor row's support contains `c2,c3`, so they lie in one class `K`. Their differing entries at `r3` exclude the dummy class. This exclusion is essential: a relaxed search that intentionally omits it admits spurious `V−` partial configurations with `c3` dummy. Such configurations cannot be full copies because a preceding `c2` in that same class cannot have a zero against `r3`. The written proof includes the exclusion explicitly.

### Unbalanced mode cases, lines 309–334

For each possible `r3`, I independently listed every nondummy column class where it could be one. These are precisely its own and preceding matching-sign class, with the extra parent sign only at the leaf. There is no additional column class to consider.

| Mode of `B` | Consequence of zero at `(r3,c4)` | Why a permitted `c3<c4` is impossible, or what survives |
| --- | --- | --- |
| `V_i+` | `π(p)>b` | Parent-plus: `π(p)≤a≤b`; own: `p≤q` and `π(q)<b`; leaf parent-minus: `π(p)<a<b`. Each contradicts the zero. |
| `V_i−` | `p≥b` | Own: `p<a≤b`; preceding minus: `π(p)<a<π(b)`. The preceding class is absent at `i=1`. |
| `W_i+` | `p>q`, same parity | Own: `p≤q′≤q`; parent-plus: `π(p)≤a≤π(q)`; leaf parent-minus: `π(p)<a<π(q)`. Equal parity rules out the weak-parent equality escape. |
| `W_i−` | `π(p)≥b` | Parent-minus cannot work. Nonleaf own-minus is excluded by the earlier support argument below. At a leaf, either the own leaf class or parent-plus class forces `b=π(p)`. |

The critical nonleaf own-minus step is valid: a column support in the nonleaf class `C_i−` from mode `A≤W_(i,d)−` must be the child support of `W_(i,e)−`, group 1, with `e≤d`. No plus mode has that class away from the leaves; the whole-class supports occur at level `i+1`. Thus `q=2π(q)+e`, `p=2π(p)+d`, and `π(p)≥b≥π(q)` imply `p≥q`. This contradicts the necessary strict own-minus one. At a leaf, opposite signs become the same class, and the proof correctly stops using this parity restriction; the weaker relation `p≤q` is enough to force equality of the parent indices.

For the additional parent-plus possibility, a minus row has no one there unless it is a shared leaf. Then the one gives `π(p)≤a`, and the plus-before-minus order gives `a≤b`. Together with `π(p)≥b`, this forces `a=b=π(p)`.

Therefore every surviving unbalanced copy has `B=W_(h,d)−`, leaf row `p`, and parent-minus column at node `π(p)`, exactly as required.

### Why the last row is dummy, lines 336–343

If `K=L`, the zero at `c2` gives a leaf index `q1<p`. A nondummy row one at `c2` must itself be a leaf of index at most `q1`; it cannot occur after `r3=p`.

If `K` is parent-plus, the zero at `c2` gives parent index `a<π(p)`. To be one on both that plus column and `c4` in the minus class at the same depth, a nondummy row must be a shared leaf. Its being one at `c2` gives parent index at most `a`, so it occurs before `p`. This rules out every nondummy `r4`.

The scratch check restored every possible later nonanchor row, rather than assuming the dummy conclusion, and found the same result through depth seven.

## Exact enumeration and short-depth cases

Balanced copies contribute `m × m × 2 × m^4 = 2m^6`. The leaf column is fixed by the leaf row, each parent-minus block has exactly two positions, and the mode/parity is uniquely determined.

For an unbalanced leaf `p=2b+d`, the second anchor row and first anchor column have a fixed mode and groups. The three anchor coordinates contribute `m^3`; the dummy row and final parent-minus column contribute `2m`; the common multiplier is therefore `2m^4` for an actual `(c2,c3)` pair and a specified first-anchor mode/group. Recomputing that pair list gives:

| First-anchor family | Number of actual pairs |
| --- | --- |
| `W_(h,e)+`, group 2, leaf class | `b` for each `e≥d` |
| `W_(h,d)−`, group 1, leaf class | `b` |
| `W_(h,e)+`, group 1, full parent-plus class | `4b` for each of the two parities `e` |
| `W_(h−1,e)+`, group 2, parent-plus half-class | `4⌊b/2⌋` for `e=b mod 2`, if `h≥2` |

For leaf columns, the one at `c3` and the parent-minus upper bound force `c3=2b+e`; the earlier zero column has the same parity and contributes `b` choices. In the minus family, mode order requires `e≤d`, while `p≤c3` requires `e≥d`, hence `e=d`.

For parent-plus columns, `c3` has node `b`, while `c2` has node `a<b`. Both blocks have size two, giving factor four. The half-family restricts the nodes to equal parity. The number of smaller nonnegative integers of the same parity as `b` is exactly `⌊b/2⌋`.

There is no whole leaf support among the available column roles. The remaining whole parent-plus support is in `V_h+`, after `B`, so it cannot supply the first anchor row. In the same-mode minus family, the first anchor row's group is 1 and the second's group is 2, so anchor order holds. All other listed first anchors precede `B` in mode order. The signatures against `c4`, `c1`, and the dummy row also match; these families specify full copies, not just necessary partial configurations.

The total is `(11−d)b+4⌊b/2⌋` per leaf. If `h=1`, both leaves have `b=0`, so all unbalanced terms vanish. If `h≥2`, `t=m/2` is even and

`Σ_(b=0)^(t−1) [21b+8⌊b/2⌋] = 21t(t−1)/2 + 2t(t−2) = t(25t−29)/2`.

Multiplying by `2m^4` and adding `2m^6` gives `(33m^6−58m^5)/4`, as claimed. At `h=2`, `b∈{0,1}`, so the parent-half term remains zero; all other formulas still work. The count is positive and below `(33/4)m^6` for every `h≥2`, and the separate `h=1` count also satisfies that upper bound.

## Arbitrary binary repairs, including anchor edits

Lines 407–466 avoid the common error of treating an original-copy hitting set as a repair. Here is the probability argument reconstructed without assuming any unedited variable-variable diagonal beyond the roots.

Fix the entire edited binary matrix `B` first and its set `E`, with `|E|<m²`. Choose a uniform leaf `z`. For every nonleaf level/sign block on the ancestor path, choose its row and column representatives independently conditional on `z`; choose anchors and dummy representatives independently of everything else. Each fixed variable position has marginal probability `2^−i/(m/2^i)=1/m`. The leaf appears only once per axis.

For an anchor/dummy endpoint, the opposite endpoint's marginal multiplies by `1/m` because the anchor/dummy selection is independent of the shared path and every opposite choice. Root choices are uniform on fixed blocks and have distributions independent of `z`, so opposite-axis root choices are independent too. Every protected cell consequently has selection probability `1/m²`. A union bound over protected cells of `E` is at most `|E|/m²<1`; there is a selection with every protected cell clean. The events do not have to be mutually independent.

A fixed diagonal leaf cell instead has selection probability `1/m`, exactly as the proof warns. The argument does not protect it or any other general variable-variable cell. It is forced later by the edited matrix's assumed `H`-freeness. Anchor edits are fully included among the bad cells in the union bound; they are not disallowed.

On a clean selected path, the designated anchors and their body signatures persist. Root-plus and root-minus values are respectively one and zero. The only possible edited bits in each of the four displayed bodies are therefore exactly the indicated variables. For binary bits, avoidance of `P=[[1,0],[1,1]]` forces, in sequence, `b+=1`, `b−=0`, `c+=1`, `c−=0`. Their rows and columns are ordered because the sampled nodes are parent/child and the dummy positions are extreme. Selecting parity `a_i mod 2` puts both child positions into the needed `W` support. At the leaf, the two forced diagonal values address the same actual cell, a contradiction.

Thus every edited matrix with fewer than `m²` changes contains a new or surviving `H`; there is no restriction on the edit directions or on unprotected cells. This proves the stated lower bound, not an exact distance claim. The explicit `T_h` flip example at lines 468–473 is also correct: it creates `V_h−` bodies with parent-minus zero and newly one leaf-to-parent entry.

## Final quantifiers and sampling consequence

The theorem fixes `H` before choosing `c,C`. For `ε_h=(14h+2)^−2`, `ε_h∈(0,1)`, `n_h` is an integer, and the distance bound supplies an admissible witness. The ratio to `ε_h^C n_h^8` is bounded by `(33/4)(14h+2)^(2C−8)4^−h`, which tends to zero for every fixed real `C>0`. Consequently for every prescribed `c>0`, some sufficiently large integer `h` gives a strictly smaller ratio than `c`. No uniformity in an `h`-dependent exponent is needed or asserted.

The coarser localization estimate `2mn^6` is separately valid because fixing the images of row 3 and column 4 leaves at most `n^6` choices. It already supplies exponential decay, so the qualitative theorem would survive a count-only correction if one were found. I found no such correction necessary.

For uniform `q`-subsets on independent axes, each cell is observed with probability `(q/n)^2`. Rejection entails observing the fixed zero cell of some copy and hence a cell of `T_h`; the union bound gives `2m(q/n)^2`. Solving for `q` gives the stated factor `(14h+2)2^(h/2)`. Since `ε_h^−1/2=14h+2`, the displayed exponent `(ε_h^−1/2−2)/28` is correct. The limitation to canonical samplers and the `q²` entry cost are preserved.

## Reproducible checks and actual outputs

The separate scratch program uses Python 3.9.25 and integer/set arithmetic. Run from `/home/vercel-sandbox/open-math-problems`:

```sh
python3 .context/reviewer-four-localization.py > .context/reviewer-four-localization-output.json
python3 scripts/validate_repository.py
```

The scratch program passed. It considers all role-support pairs, checks the exact earlier nonleaf-minus support restriction, enumerates the relaxed unbalanced partial configurations, then restores `c2` and all possible `r4` to enumerate the unbalanced sector. It does **not** assume localization or dummy `r4` in those loops; those are assertions checked against the generated configurations. It does assume the anchor-count `(2,1)` sector and the group orientation after testing the contrary orientation's dummy obstruction. It is therefore not a substitute for a full-pattern census or for Lemma 3.

| h | Role-support pairs | Relaxed survivors | Complete unbalanced quotient copies | Weighted unbalanced count |
| --- | ---: | ---: | ---: | ---: |
| 1 | 288 | 9 | 0 | 0 |
| 2 | 1,152 | 22 | 9 | 10,752 |
| 3 | 2,592 | 44 | 58 | 1,163,264 |
| 4 | 4,608 | 88 | 276 | 89,653,248 |
| 5 | 7,200 | 176 | 1,192 | 6,224,347,136 |
| 6 | 10,368 | 352 | 4,944 | 413,927,473,152 |
| 7 | 14,112 | 704 | 20,128 | 26,989,574,488,064 |

All relaxed survivors were in leaf `W−` modes and localized to the prescribed parent-minus zero. All complete configurations had dummy `r4`. The weighted counts matched the unbalanced part `(25m^6−58m^5)/4`, with the separate zero case at `h=1`.

One development run of the scratch program initially omitted the proof's already-stated `K≠dummy` hypothesis and correctly failed on the spurious partial configuration described above. I added that necessary relaxation hypothesis, not an exception or hardcoded count. No counterexample to the written proof was found in that failed run.

The root repository validator returned:

```text
PASS: 34 tracks in 7 groups; catalog, prompts, artifacts, and views agree
PASS: 315 local links across 103 Markdown files
```

The package command was also launched from `.context/ordered-binary-matrix-removal`:

```sh
python3 scripts/run_checks.py
```

It exited successfully with this actual output:

```text
compression: exact checks and reference comparison passed
adversarial: exact checks and reference comparison passed
refinement: exact checks and reference comparison passed
four: exact checks and reference comparison passed
four_repair: exact checks and reference comparison passed
Package integrity passed: 52 local links; manuscript hashes; candidate status.
All checks passed. Finite checks are not a universal theorem or independent review.
```

These existing scripts share the candidate host implementation, so rerunning them is regression verification, not a separate independent implementation. The suite was run before the parent's new formal-verification artifacts were integrated into package metadata.

## Additional source-level review of the new Lean modules

At the parent's request I also read `formal/OrderedRemoval/AnchorClassification.lean`, `LocalArithmetic.lean`, `Propagation.lean`, and `ProtectedSampling.lean` as they stood after the primary written-proof audit. This was source-level semantic review; I did not independently run a Lean build or axiom audit. I found no mismatch between their theorem hypotheses/conclusions and the conditional mathematical claims described in their comments.

- `AnchorClassification.Certificate` assumes restrictions of crown exclusion, support comparability, and ordered containment on the selected copy. These are substantial structural hypotheses, not results established for the concrete host by that file. The header explicitly says so. Strict rank order is a valid extracted property only after duplicate twin blocks have been excluded using the distinct pattern rows/columns. The comment acknowledges this boundary. The crossed-one alignment argument requires only the stated mode-equality condition, not a silently omitted opposite-group premise; the two-group ranks and order are sufficient for the count conclusion.
- `LocalArithmetic` correctly treats the crucial nonleaf unbalanced parity condition as `q % 2 ≤ p % 2`. Replacing it by equality would miss possible earlier parity modes. The leaf conclusion correctly removes the parity condition. The parent-plus leaf lemma forces both parent-node equalities, and the last-row lemmas use strict leaf row order. These statements match the written argument; extracting their premises remains the principal unformalized step.
- `Propagation` has the right four bodies in the right orientation. Its cross-bit sequence index `i` represents the edge from depth `i` to depth `i+1`. The all-depth induction uses unrestricted Boolean values at every level. No `h≥1` hypothesis is missing in `exists_body`: at `h=0`, the opposite root bits and shared terminal bit are already inconsistent, so the theorem remains logically valid.
- `ProtectedSampling` proves an integer union bound and existence of an untouched sample under an incidence-frequency bound. Duplicate samples and edit-list entries do not make that upper bound unsound. The strict budget forces a nonempty sample list. Its final theorem composes clean-root values with the propagation theorem and intentionally concludes a body, not an ordered `H` copy.

One wording point should remain visible: the `m³` sample-list / frequency-`m` comment in `ProtectedSampling` refers to an intended **three-seed** parameterization. The written Section 7 instead samples many representatives independently conditional on the leaf; its full finite outcome space is not simply `m³`. A three-seed variant can reuse one uniform offset on each axis across all classes, with the leaf as the third seed, because the needed protected-cell marginals still depend on independent opposite-axis offsets. But neither that construction nor its incidence-frequency extraction is formalized in the module. It would be inaccurate to describe the module alone as a formal proof of the written sampler's concrete bound. The current comments already label the concrete incidence bound as a hypothesis; any final verification summary should preserve that qualification.

## Remaining decisive work

The next decisive assurance step is a complete formalization of the host/order/embedding definitions and the all-depth anchor classification plus localization, linked to the repair and asymptotic claims. Local arithmetic certificates or bounded enumerations alone do not cover that interface. A human expert review and a broader novelty search remain valuable and are not supplied by this report. I identified no specific unresolved mathematical gap that presently requires a changed theorem statement.

## Packaging note from the coordinating agent

The report above retains the reviewer's findings. The archived checker is now `verification/check_four_reviewer.py`; only its runtime-version output field was removed so reference comparisons work across Python versions. The review itself ran on Python 3.9.25. Reproduce the packaged checker from the standalone repository root with `python3 verification/check_four_reviewer.py`. Original scratch paths and historical validation counts above describe the actual review run.
