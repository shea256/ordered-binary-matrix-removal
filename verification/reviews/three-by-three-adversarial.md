# Fresh adversarial review of the 3×3 crown candidate

Date: 2026-10-11. Reviewer: a separate Claude session (Claude Fable 5.1) that
did not write the proof, the discovery code, or the earlier checkers. This is a
separate-agent review, **not** independent human peer review, not a Lean
certificate, and not a novelty assessment.

## Verdict

**Argument survives scrutiny. I found no gap, missing case, or counterexample
in [proofs/three-by-three.md](../../proofs/three-by-three.md).** The all-depth
case analysis in Sections 3–7 reconstructs correctly from the host definition
alone, and an independent rebuild of the host from the prose reproduces every
finite claim. Two minor exposition points are listed below; neither needs a
new lemma.

Reviewed snapshot: `proofs/three-by-three.md` with SHA-256
`1a84af8a7fcc997036256160c1c2a8fc6f0d7fea4fafcf52b8f3ab6e19082f48`.

## What I did

1. **Rebuilt the host from the written Section 2 only.** My checker,
   [check_three_by_three_reviewer.py](../check_three_by_three_reviewer.py),
   imports nothing from `experiments/` or the earlier checkers and uses a
   different axis representation (label lists, run-length collapse of twins
   instead of weighted quotient positions). Agreement with the earlier two
   implementations therefore also confirms that the prose and the code
   describe the same matrix.
2. **Brute-forced every crown copy with no block assumptions** on the actual
   n×n matrix at h=1,2,3 (n=20, 72, 208), and on the collapsed-twin matrix
   at h=1..6 (n up to 3,200). Collapsing is sound because the crown has
   pairwise distinct rows and columns, so a copy cannot reuse a twin.
3. **Classified every copy** against the Section 5 description. All copies
   use X of mode W⁻ at the leaf level, a leaf row, the dummy row, the leaf's
   own parent-minus column, and the matching Y column; the first column is
   a same-parent leaf at or after the leaf, or that parent's plus column.
4. **Checked the Section 3 facts mechanically** through h=6: class node
   order, all six displayed order comparisons, row/column monotonicity along
   classes, the crossing-support lemma (every ordered crossing is the stated
   W⁻ᵢ,₀ / {W⁻ᵢ₊₁,ₑ, V⁻ᵢ₊₁} configuration with v∈C⁻ᵢ₋₁, w odd in C⁻ᵢ), and
   the per-class shape of U supports (empty, full, or one parity half).
5. **Checked the Section 6 frames** for every leaf path and mode through
   h=6: the five anchor incidences and the dummy incidences carry the crown
   entries and the rows/columns are in the required order, so each P body
   really completes to K.
6. **Computed the exact minimum repair distance by SAT** (lazy copy-clause
   generation, arbitrary binary edits anywhere, including anchors and
   dummies): D_K(A₁)=4 and D_K(A₂)=16, both equal to m². The proof claims
   only ≥m²; these show the bound is tight at small depth. A depth-3 run
   (n=208, budget 63) reached 250 lazy-clause rounds without a verdict and
   was stopped by its 25-minute limit, so no exact depth-3 value is recorded.

Actual output: [three-by-three-reviewer-report.json](../reference/three-by-three-reviewer-report.json).

| h | n | copies found | 7m⁴ | plus-parent family | leaf family | non-canonical |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 | 112 | 112 | 64 | 48 | 0 |
| 2 | 72 | 1,792 | 1,792 | 1,024 | 768 | 0 |
| 3 | 208 | 28,672 | 28,672 | 16,384 | 12,288 | 0 |
| 4 | 544 | 458,752 | 458,752 | 262,144 | 196,608 | 0 |
| 5 | 1,344 | 7,340,032 | 7,340,032 | 4,194,304 | 3,145,728 | 0 |
| 6 | 3,200 | 117,440,512 | 117,440,512 | 67,108,864 | 50,331,648 | 0 |

Rows h≤3 were also counted physically (every ordered row triple of the
full matrix) with identical results.

## All-depth case audit

I re-derived each step from the entry tables rather than trusting the text.

**Section 3.** Within a column class the one-sets on nonanchor rows are
nested in the node index (e.g. C⁺ᵢ(q) is one on R⁺ᵢ(p) iff p≤q and on
R⁺ᵢ₊₁(p) iff ⌊p/2⌋≤q); the same holds for minus classes and for leaf
columns, which are one only on leaf rows p≤q and the dummy. The class
incidence graph of nondummy rows is two paths joined at the leaf class, so
the only triangle is {L_C, C⁺ₕ₋₁, C⁻ₕ₋₁}. The crossing-support lemma is a
finite check over the eleven support shapes; plus and minus variable supports
never meet because the odd-child addition stops before the shared leaves.

**Section 4.** Anchor rows are a prefix and anchor columns a suffix of any
copy. The cases (a,b)=(0,0), (0,≥1), (≥1,≥2), (≥2,1), (≥2,0) and (1,0)
are each closed as written. The delicate ones:

- (0,b≥1): r₁,r₂ share a variable class because Y_t's variable support is
  one class or one parity half, and r₂≠R_* since r₃ is a later nonanchor
  row. For b≤2 the first column's trace 01 contradicts class monotonicity;
  for b=3 the two Y supports would be opposite parity halves of one class,
  and are then disjoint on r₃.
- (≥2,0): the row traces force u∈T_B∖T_A, v∈T_A∖T_B, w∈T_A∩T_B, so the
  crossing lemma applies; the dummy column is excluded by the W-before-V
  mode order. For a=2 the third row must be one on both C⁻ᵢ₋₁ and an even
  C⁻ᵢ node, forcing R⁻ᵢ, and then monotonicity forces a one on w. For a=3
  no support spans C⁻ᵢ₋₁ and C⁻ᵢ₊₁, and the only one spanning C⁻ᵢ₋₁ and
  C⁻ᵢ adds odd children only.
- (1,0): c₂,c₃ in one class contradicts r₃'s trace 10; the two-class
  support W⁻ᵢ,₀ then forces c₁ into {C⁻ᵢ₋₁, C⁻ᵢ} (I confirmed the
  "no third class" claim including the leaf case i+1=h, where a leaf row's
  classes {L_C, C⁺ₕ₋₁, C⁻ₕ₋₁} meet the other row's classes only in C⁻ₕ₋₁),
  and either placement gives a forbidden trace 10 inside a class.

**Section 5.** With r₁=X_t and c₃=Y_t of the same mode:

- V⁺ᵢ: ⌊p/2⌋>q from the zero, r₃=R⁺ᵢ₋₁(a) from its one on c₂ and its zero
  on Y_t (this is where the dummy-row one on vertical Y blocks is used),
  then ⌊p/2⌋≤a≤q. Contradiction.
- V⁻ᵢ: p≥q, r₃=R⁻ᵢ(a), p≤⌊a/2⌋<q. Contradiction.
- W⁺ᵢ,ₑ: c₂ is a same-parity child with p>q (c₂≠C_* because the entry is
  zero); c₁ in the child class, the plus parent, or at the leaf level the
  minus parent all contradict order plus positivity.
- W⁻ᵢ,ₑ: an odd-child c₂ is excluded by p≥q and u<q; so c₂=C⁻ᵢ₋₁(b) with
  b≤⌊p/2⌋. For i<h the only candidate c₁ is C⁻ᵢ(q), q>p, ⌊q/2⌋≤b, forcing
  q=p+1 with p even, which is exactly an odd child in T_t. So i=h, and the
  leaf-level analysis pins b=⌊p/2⌋ and c₁ to the two stated families. r₃
  must be the dummy row because no later variable row is one on
  C⁻ₕ₋₁(⌊p/2⌋).

Conversely each described sextuple is a copy, and the count
(m/2)·2m³·(4+3)=7m⁴ is right.

**Section 6.** For every mode on a path, the frame cells (X_t,c₁)=0,
(X_t,c₂)=1, (X_t,Y_t)=1, (r₁,Y_t)=1, (r₂,Y_t)=0 and the dummy body cells
are correct in A (checked mechanically, item 5 above). Each such cell has
an anchor or dummy endpoint, so it is selected with probability exactly
1/m² (block representative 1/m on each axis, independent), as are the two
root cells. The union bound over M<m² edited cells leaves a selection with
no edited protected cell. The four Boolean propagation steps are exactly
as displayed, the diagonal cells reused between the vertical body at depth
i and the horizontal body at depth i−1 are the same selected cells, and
the shared leaf cell is forced to 1 by W⁺ₕ and to 0 by W⁻ₕ. Edits in
either direction at any cell are allowed throughout.

**Section 7.** ε_h=(8h+2)⁻² gives m²=ε_h n². Blowups multiply the exact
count by q⁶ (a copy cannot use two identical rows) and the repair bound by
q², leaving both normalized quantities fixed.

## Findings

| Severity | Finding | Location |
| --- | --- | --- |
| Fatal / major | None found. | — |
| Minor correctness | None found. | — |
| Exposition | In the W⁺ and W⁻ cases of Section 5, say explicitly that c₂≠C_* because (r₂,c₂)=0 while every variable row is one on the dummy column. The text uses this silently. | Section 5 |
| Exposition | "Elsewhere the class-incidence graph is two paths" is more precisely "two paths joined at the leaf class"; the conclusion (only one triangle) is unchanged. | Section 3 |
| Observation | The repair lower bound m² is attained at h=1 and h=2 (exact SAT). The optimal repairs found flip anchor-column and dummy-row entries, not the leaf diagonals, which illustrates why hitting original copies and arbitrary repair must be kept separate. No exact-distance claim for general h is made or certified here. | Section 6 |

## Boundaries

- Finite agreement through h=6 and the SAT distances are evidence for the
  written all-depth argument, not a replacement for it; my favourable
  reading of that argument is subject to ordinary reviewer fallibility.
- I did not build Lean or assess worldwide novelty of a 3×3 obstruction; the
  bounded search recorded in `BASELINE.md` stands as written.
- I did not modify the proof or the earlier checkers. My artifacts are this
  report, the reviewer checker, and its output. The `--sat` option needs the
  third-party `python-sat` package; everything else is standard library.
