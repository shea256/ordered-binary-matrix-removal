# Baseline audit — OPENAI-190


## October 11 — chart timestamp audit

The dated chart uses GitHub record times and labels the event type.
Erebos Labs' v1.0.0 `published_at` is **2026-10-09T12:40:51Z**, for commit
`45248e57ab1c2197419981bba04e1cde050494ca`; its repository creation time is
12:39:06Z. The result-bearing public release is the chart milestone.
This establishes availability by that time, not the private discovery time
or whether a social announcement happened.

OpenAI's paper is dated September 25, but the Git commit adding it is
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, dated October 6 at 21:58:50Z.
ProveIt's pinned 5×5 manuscript commit is dated October 7 at 21:24:26Z.
The chart explicitly uses those GitHub commit records, whose dates alone
cannot establish first public visibility. Our 3×4 PR opened October 11
at 18:38:32Z. See [the timestamp table](assets/README.md) and archived
[event data](assets/pattern-size-events.json) for all seven points.

## October 11 — rectangular refinement baseline

The strongest verified external pattern baseline for this attempt remains
Erebos's **4×4**, at `6d21ce36e83b71d8a44015016cf3ac77e44b55ff`;
OpenAI remains at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` and the relevant
ProveIt path at `bfbfe915186310fdf745a7a089e7dd88eeb773b1`. The versions,
exact statements, stronger companion results, and verification differences
are recorded below. They were rechecked before this search. Additional
phrase searches for ordered removal and 3×4 patterns found no matching
primary result; this bounded search is not proof of novelty.

The new [3×4 candidate](proofs/three-by-four.md) changes the host's anchor
encoding, rather than simply deleting a row of the previous host. Its fixed
pattern is `1001/1010/0111`, on square n×n binary hosts. The intended advance
is one fewer forbidden row and 12 instead of 16 specified entries; it is
not a 3×3 or a smaller maximum side length. Distances still allow all
binary edits, and the same arbitrarily-small-ε/arbitrarily-large-n
quantifiers are retained. Densities now normalize by n⁷ rather than n⁸.

**Proof map:** one row anchor plus two column anchors, with W-dummy ones
and nonterminal even-W-minus/odd-child ones → every full H copy has one
anchor row and one or two anchor columns → its fixed zero uses a leaf
and its own parent-minus column → at most 2mn⁵ copies. Prescribed role
signatures survive → inherited guarded propagation against arbitrary
repairs still gives m² edits → density ≤2ε_h 2⁻ʰ at ε_h=(14h+2)⁻².
Uniform blowups preserve the bounds. This is a written candidate theorem;
the old H4 Lean certificate does not verify it. Exact repair equality
and the earlier H4 exact count are not transferred.


## Previous checkpoint record

# Baseline audit — OPENAI-190

## Current baseline correction — October 11, 2026

The prior searches recorded below missed two relevant public sources. Their
historical “no stronger follow-up found” statements are superseded. The same
4×4 pattern and qualitative Lean theorem were published before our 4×4 PR.
The present contribution is a narrower copy-density refinement of that known
pattern. It is not a new pattern-size record or the first formal proof.

| Primary source | Version / public record | Relevant result |
| --- | --- | --- |
| [ProveIt research manuscript](https://github.com/VladimirReshetnikov/ProveIt/tree/bfbfe915186310fdf745a7a089e7dd88eeb773b1/Combinatorics/OrderedMatrices/Research/ordered-matrix-removal) | `bfbfe915186310fdf745a7a089e7dd88eeb773b1`, October 7 | 5×5 obstruction, exact m² repair, canonical sampling threshold; displays the same H4 candidate |
| [Erebos v1.0.0](https://github.com/erebos-labs/ordered-matrix-removal-4x4/releases/tag/v1.0.0) | `45248e57ab1c2197419981bba04e1cde050494ca`, published October 9 at 12:40:51 UTC | Same H4, complete localization, qualitative Lean obstruction, exact written copy count |
| [Erebos v1.1.0](https://github.com/erebos-labs/ordered-matrix-removal-4x4/releases/tag/v1.1.0) | `6d21ce36e83b71d8a44015016cf3ac77e44b55ff`, published October 9 at 15:12:02 UTC | Exact unrestricted repair distance m² via terminal-anchor repair; Lean theorem |
| [Our first 4×4 PR](https://github.com/shea256/ordered-binary-matrix-removal/pull/1) | Created October 10 at 18:48:25 UTC | Later H4 construction with a different mode order |

Erebos's current pinned [theorem](https://github.com/erebos-labs/ordered-matrix-removal-4x4/blob/6d21ce36e83b71d8a44015016cf3ac77e44b55ff/THEOREM.md)
and [paper](https://github.com/erebos-labs/ordered-matrix-removal-4x4/blob/6d21ce36e83b71d8a44015016cf3ac77e44b55ff/paper/report.tex)
use m=2^h, n=(14h+2)m, the literal H=0110/1001/1010/0111, independently
increasing axes, all sixteen binary constraints and arbitrary binary repairs.
Their count is 128 at h=1 and (41m⁶−74m⁵)/4 at h≥2. The exact repair distance
is (14h+2)⁻². Their qualitative capstone uses the coarser count 2mn⁶; do not
compare only against that weaker number. The stronger quantifiers permit
ε arbitrarily small and n beyond any prescribed ε-dependent threshold.
Their exact count is written mathematics, not the count used in their Lean
capstone. We inspected sources and published audit records, but did not rerun
the Erebos or ProveIt Lean builds. These public records establish precedence
relative to our PR, not worldwide priority or independent peer review.

We rechecked Erebos main at the v1.1.0 hash on October 11; ProveIt's path history
still showed the pinned October 7 intake. OpenAI CONTENTS still lists one
#190 manuscript; its pinned baseline below remains relevant to provenance.
Phrase searches for follow-ups were unproductive and are not exhaustive.
The two finite physical hosts exported by Erebos (h=1,2) match our transcription
of its mode order entry for entry, including all 1,024 and 14,400 entries.
The new comparison checker also reproduces its count through h=4.

**New proof map:** global minus-before-plus-before-vertical mode order →
ordered support property and zero localization survive → every unbalanced
copy uses one terminal minus mode and two same-parity leaf columns →
N=(5/2)m⁶−m⁵. Inherited arbitrary-repair lower bound + transferred Erebos
terminal-anchor upper bound → exact m² edits. Hence the limiting copy-density
ratio to Erebos is 10/41 at the same n and exact distance. Intrinsic copies
survive arbitrary permutations of intact mode blocks on each axis, proving
optimality only within that fixed class. The new order/count/equality are
written claims pending independent mathematical review and Lean formalization.


Audit date: 2026-10-10. Upstream `openai/math` commit:
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, dated 2026-10-08.
The repository checkout used for this attempt initially had HEAD
`ba5e2d17e78abe08ea5d33875f06c2ae02dc026d`.

## Primary release and versions

[CONTENTS.md](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/CONTENTS.md)
lists exactly one manuscript under #190:
[Polynomial removal fails for ordered binary matrices](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-removal-fails-for-ordered-binary-matrices-September-25-2026/paper.pdf),
September 25, 2026. Its complete six-section LaTeX source, bibliography,
scope notes, comparator, and 61 implementation modules were downloaded at
that commit; see [manifest.json](verification/source_manifest.json).
No additional #190 companion or correction appears in that pinned entry.

The source defines a binary 66-by-66 pattern with a 64-by-64 anchor S and
body P=((1,0),(1,1)). Row and column choices are independently increasing;
all zero and one constraints must match. For a square host A of order n,
N_H(A) counts such choices and dist_H(A) is the minimum Hamming distance
to an H-free *binary* host, divided by n^2. All cells may change in either
direction, including anchor cells. Hosts do not have a third symbol.

Theorem 1.1 states: for every integer h>=1, set

\[
 m=2^h,\quad d_h=386h+2,\quad n_h=d_hm,\quad\epsilon_h=d_h^{-2}.
\]

There exists an explicitly defined binary A_h such that

\[
 \operatorname{dist}_H(A_h)\ge\epsilon_h,\qquad
 N_H(A_h)/n_h^{132}\le\epsilon_h2^{-h}.
\]

It follows that for **every** c,C>0 there exist n>=1,
0<epsilon<1 and a binary host A with dist_H(A)>=epsilon but
N_H(A)<c epsilon^C n^132. The fixed pattern is not allowed to depend on
c,C. Epsilon varies along the sequence and tends to zero: this is not
a failure of qualitative removal at a fixed positive epsilon.

The manuscript also proves a lower bound for the canonical sampler
choosing q uniform rows and q independent uniform columns and rejecting
only upon observing H. Its rejection probability is at most
epsilon_h 2^{-h} q^2; positive fixed rejection probability rho requires
q>=sqrt(rho)(386h+2)2^{h/2}. The sampler observes q^2 entries. Neither
the manuscript statement nor this attempt establishes an arbitrary
adaptive/two-sided tester lower bound.

## Verification stages

The scope page reports a Lean formalization. The comparator file contains
`sorry` because it specifies the challenge statement; its JSON points
to `OAI.Combinatorics.MatrixRemoval.Main` as the solution. This template
hole is not evidence of a hole in the implementation.

The solution's `counterexample_sequence` and `no_polynomial_removal_bound`
state the advertised sequence and final quantifiers for `fixedH`. All 61
MatrixRemoval source modules were scanned: no lexical `sorry`, `axiom`,
or `admit` hits. Their imports outside that namespace are only Mathlib.
The comparator allows `propext`, `Quot.sound`, and `Classical.choice`.
The pinned toolchain is Lean 4.34.1; the Mathlib revision is recorded in
the downloaded lake manifest. At that initial source audit no Lean/lake
executable was installed, and no upstream build, kernel axiom audit, or
Comparator run was performed. Source inspection and lexical checks are
weaker than a build. The later partial development below is separate.

The paper's construction, arbitrary-repair propagation, mode localization
and asymptotic calculation were recalculated in this attempt; a second
pass used separate integer-threshold and Boolean checks. These are
same-agent checks, not independent peer review.

## Relevant strongest positive and adjacent baselines

* Alon–Ben-Eliezer, [Efficient Removal Lemmas for Matrices](https://arxiv.org/html/1609.04235v3),
  arXiv v3 dated 2017-06-12; journal version *Order* 37 (2020), 83–101.
  Also checked the [author-hosted June 1, 2019 revision](https://web.math.princeton.edu/~nalon/PDFS/testmatrixf4.pdf):
  Theorems 1.2 and 1.5 retain the quantifiers and assumptions below.
  Theorem 1.2: for each fixed s-by-t binary pattern, epsilon n^2
  entry-disjoint ordered copies force at least delta n^{s+t} copies,
  where delta^{-1} is polynomial in epsilon^{-1}. This is a packing/
  original-copy hitting statement, not an arbitrary binary repair bound.
  Theorem 1.5 is stronger than merely treating unordered matrices:
  each fixed finite binary forbidden family closed under **row**
  permutations has polynomial induced removal; column closure follows
  by transposition. A singleton with an ordered anchor need not satisfy
  that closure assumption. Section 5.1's counterexample uses ternary
  hosts and the permutation-closed pair of 2-by-2 identity/anti-identity
  patterns, so it does not settle the binary singleton model.
* Alon–Ben-Eliezer–Fischer, [Testing Hereditary Properties of Ordered Graphs and Matrices](https://arxiv.org/html/1704.02367v1),
  arXiv v1, 2017-04-07; FOCS 2017. Theorem 1.8: for every fixed finite
  alphabet, finite or infinite family F of ordered matrices, and
  epsilon>0, there exist q_0,delta>0 such that every epsilon-far host
  contains delta n^{q+q'} copies of some q-by-q' member of F with
  q,q'<=q_0. This qualitative theorem survives the obstruction.
* Gishboliner–Tomon, [Polynomial removal lemmas for ordered graphs](https://arxiv.org/html/2110.03577v2),
  arXiv v2, 2023-03-10; *Combinatorial Theory* 2(3), 2022. Polynomial
  induced removal holds exactly for two-vertex patterns or the
  three-vertex graph with edges xy,xz for x<y<z, up to complementation
  and order reversal (in the nontrivial size range considered there).
  This uses one shared vertex order and symmetric adjacency and cannot
  be transferred to independent row/column orders without a proof.
* Gishboliner–Shapira, [Polynomial Property Testing](https://arxiv.org/html/2508.16878v1),
  arXiv v1, 2025-08-23, listed as the only arXiv version when checked;
  journal version *Computer Science Review* 58 (2025), 100806.
  Conjecture 4.5 is the binary singleton polynomial removal conjecture.
  Its statement that even the 2-by-2 identity case was unknown predates
  the 2026 release and is not a current verification of that case.

The publisher DOI endpoints for the Order article and Fischer–Rozenberg
2007 returned access errors through the browsing tool. The arXiv source
and Alon–Ben-Eliezer's explicit ternary construction were accessible.
No direct inspection of the unavailable Fischer–Rozenberg paper is claimed.

Searches for the exact 2026 title, corrections, smaller patterns and
ordered binary matrix removal found no stronger direct primary follow-up.
Secondary October 2026 indexes repeat the release and explicitly disclaim
independent rebuilding/review. This search is a novelty screen, not a
proof that no unpublished or poorly indexed stronger result exists.

Local notes mention #190 only as a reserve direction; they supply no
argument used here. No #109/#130/matrix-multiplication/attention note is
used as a mathematical premise.

## Recalculated strongest bound of the same construction

The manuscript uses the coarse leaf-cell bound N_H<=m n^{130}. Its
localization proof actually identifies exactly these bodies: mode
W_{h,d}^-, leaf p on both axes, parent-minus column node floor(p/2),
and a dummy row. There are m leaf choices, two parent column positions,
m dummy row positions and m^{128} anchor choices. Thus the same
baseline construction gives exactly

\[
 N_{H_{66}}(A_h)=2m^{130},\qquad
 N_{H_{66}}(A_h)/n_h^{132}=2d_h^{-132}4^{-h}.
\]

This is a direct derived strengthening of the baseline's stated count,
not the proposed new construction or a claim of a new asymptotic mechanism.
It was checked by exact weighted enumeration of designated bodies at
depths 1 through 6, together with the all-depth localization calculation.
The proposed result must be compared to this stronger consequence too.

## Proof map and improvement parameter

The baseline chain is: five-column nonshattering + anchor density/twins
-> anchor rigidity -> designated body roles -> only diagonal-leaf copies
-> density bound. Separately, size-m group sampling protects anchors,
dummy incidences and roots -> four P-avoidance implications per level
-> contradictory shared-leaf value -> at least m^2 repair edits.

The proposed replacement is **three-column** nonshattering, using the
actual support graph and threshold structure, then a **13-by-13** anchor.
The six modes per depth remain. Generally d_h=(6s+2)h+2 and k=s+2;
the replacement makes d_h=80h+2 and k=15. All-depth rigidity must be
proved anew; substituting 13 for 64 in the existing Lean code is invalid.
The final implication is a smaller fixed forbidden pattern, with the
same binary model and every-c,C quantifiers, not a smaller finite host.


## Second refinement audit — 2026-10-10

Rechecked `openai/math` main through the GitHub API: it remains
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, dated 2026-10-08. Revisited
CONTENTS and the pinned manuscript's exact introductory definitions and
quantifiers. The source baseline and companion coverage above are unchanged.
Searches for the exact title, smaller ordered binary removal patterns, and
5×5 / 5-by-5 variants did not find a stronger direct primary follow-up.
The absence of search results is not proof of novelty.

The 15×15 result is an earlier *candidate*, not independently verified SOTA.
Its proof has been reread; the new proof states and justifies the required
host properties again. The current candidate improves the primary 66×66
pattern and the earlier candidate to **5×5**. Its 3×3 anchor is J_3-I_3.
The local improvement is not two-column nonshattering (which remains false):
it uses only the three weight-two traces from the old eight-word witness,
plus an ordering in which strictly containing role supports occur later.

New proof map: nonanchor crown exclusion + ordered laminar role supports
+ aligned anchor mode orders -> 3×3 anchor rigidity -> unit body signatures
-> original leaf localization -> exact density 2(20h+2)^−10 4^−h. Separately,
unchanged protected-cell sampling and four implications per level ->
arbitrary repair distance at least (20h+2)^−2. The full draft is
[five-by-five.md](proofs/five-by-five.md). The qualitative obstruction and
4^−h decay mechanism remain inherited; the fixed pattern size is the
proposed new theorem refinement.

## Third refinement audit — 2026-10-10

Rechecked upstream main through the GitHub API: it still matches the pinned
commit above, dated 2026-10-08. Searches for the original title with refinement
and for ordered binary removal with 4×4 did not identify a stronger direct
primary follow-up. The prior companion audit is retained; a conclusive
novelty assessment is still outstanding. Neither earlier local candidate
is treated as independently verified SOTA.

The new candidate reduces the fixed forbidden pattern from 5×5 to **4×4**,
with S=((0,1),(1,0)). The 2×2 component is not rigid. Instead the proof map is:

crown exclusion + ordered laminar supports -> full H copies have anchor
counts (2,2) or (2,1) -> both configurations use a fixed zero at a leaf row
and its immediate parent-minus column -> exact count at most (33/4)m^6
-> density at most (33/4)(14h+2)^−8 4^−h.

Separately, protected sampling and the designated modes still imply at
least m² arbitrary repair edits, hence distance at least (14h+2)^−2.
The all-c,C conclusion follows with the same fixed 4×4 H. See
[four-by-four.md](proofs/four-by-four.md). The 5×5 pure-anchor proof and
its two-by-two limitation are preserved as history: this refinement
changes the localization requirement, not that limitation's truth.

## Assurance checkpoint — 2026-10-10

Both the coordinating agent and a user-authorized separate reviewer rechecked
upstream main; it still matched the pinned commit. The reviewer also inspected
the primary introduction, localization, and arbitrary-repair sections.
Additional title/correction/4×4 searches found no stronger direct primary
follow-up. The previous companion audit remains; novelty is unresolved.

The separate reviewer found no material error in the 4×4 written argument.
The new local Lean 4.34.1 development proves conditional parts of that
argument using Std only. It does not rebuild or supersede the original
61-module formalization and does not certify the final 4×4 theorem.
See the [assurance checkpoint](verification/reviews/four-assurance.md).

### Localization checkpoint source recheck — 2026-10-11

`gh api repos/openai/math/commits/main --jq '.sha'` again returned
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. This checkpoint extends
formal verification of the existing 4×4 candidate; it makes no new
pattern-size or novelty claim. The strongest baseline comparison and
outstanding independent-review/novelty qualifications above are unchanged.

### End-to-end certificate source recheck — 2026-10-11

Upstream main was rechecked through the GitHub API and still matched
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. The selected original source files
were also checked against the 78-file manifest by the separate reviewer. This
checkpoint completes Lean verification of the qualitative 4×4 obstruction;
it makes no new size or novelty claim. It uses the weaker but sufficient
copy estimate 2mn⁶, not the manuscript's sharper exact enumeration. The earlier
partial-coverage statements above describe historical checkpoints. The
current coverage and inherited-module attribution are in
[formal/README.md](formal/README.md) and [ATTRIBUTION.md](ATTRIBUTION.md).


## Formalization checkpoint source refresh — October 11

A fresh GitHub API read still gives OpenAI main as
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` and Erebos main as
`6d21ce36e83b71d8a44015016cf3ac77e44b55ff`. OpenAI's pinned CONTENTS.md
lists the September 25 manuscript and its Lean documentation for #190,
with no additional companion result in that family. The known H4 baseline
and priority attribution above remain unchanged.

Additional searches for ordered matrix removal with “3x4”, “3×4”, and
OpenAI #190 smaller patterns returned no additional primary smaller-pattern
result. This is a bounded search, not a certification of worldwide novelty.
