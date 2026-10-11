Coordinator archive note: the reviewer's original execution paths below were
in ignored scratch space. The unchanged checker is archived as
[check_optimized_order_reviewer.py](../check_optimized_order_reviewer.py), and its
output as [optimized-order-reviewer-report.json](../reference/optimized-order-reviewer-report.json).
Reviewed file hashes are in [optimized-order-reviewed-snapshots.json](../reference/optimized-order-reviewed-snapshots.json).
From this project directory, reproduce the checker with
`python3 verification/check_optimized_order_reviewer.py`.

# Adversarial review of the global minus-first mode order

Date: 2026-10-11. Reviewer: `/root/four_proof_reviewer`.

**Verdict:** I found no mathematical gap in the proposed all-depth argument.
The new order gives exactly

\[
N_H(A_h)=\frac52m^6-m^5,\qquad
\min_{B\ H\text{-free}}|A_h\triangle B|=m^2
\quad(h\ge1,\ m=2^h).
\]

Its count is minimal among hosts obtained by independently permuting intact
anchor-mode blocks on the two axes, with the raw entries, nonanchor
orders, group sizes, and within-mode group order fixed. This is a restricted
optimality result and a constant improvement over the pinned Erebos host.
The numerical comparison needs the word **asymptotically**: 75.6% is not a
uniform finite-depth reduction.

This is a separate AI agent's adversarial mathematical review, **not
independent human peer review, a new Lean build, or proof by finite census**.
The new order is not the order encoded by the existing formal `modeRank`.
The prior formalization does not automatically certify this refinement.
No main proof, metadata, or formal implementation file was edited by me.

## Sources and exact candidate

The final actual candidate text reviewed is
`.context/ordered-binary-matrix-removal/proofs/optimized-order.md`, including
all nine sections, the new repair proof in Section 8, independently permuted
axes in Section 6, and the uniform blowup/threshold quantifiers in Section 9.
I also checked the synchronized `manuscript.md` overview and proof body.
The mathematical discussion below concerns that actual text after the
corrections recorded near the end of this report, not merely the proposed
order described in the task message.

The Erebos checkout inspected was
`.context/erebos-ordered-matrix-removal-4x4` at
`6d21ce36e83b71d8a44015016cf3ac77e44b55ff`. I read the host/order and exact
enumeration in `paper/report.tex`, the entire
`paper/terminal-anchor-proof.md`, and the terminal-anchor Lean statements
and proof structure in `TerminalAnchorRepair.lean` and
`TerminalAnchorCount.lean`. I also checked that `GeneralOrder.lean` concerns
tree traversal inequalities; it does not state the proposed anchor-mode
permutation optimization. This pass is not an exhaustive priority search.

The comparison is with the **same** literal pattern
`0110 / 1001 / 1010 / 0111`, independent increasing row/column choices,
all sixteen bits, unrestricted binary repairs, and host order
`n=(14h+2)2^h`. Erebos's count is 128 at h=1 and
`(41m^6−74m^5)/4` for h≥2; its terminal-anchor follow-up proves exact
repair distance `m²`, not just a lower bound. The previous local order has
count 128 at h=1 and `(33m^6−58m^5)/4` for h≥2.

The new order, on **both** axes, is:

1. all `W−_(i,d)`, increasing i and then d;
2. all `W+_(i,d)`, increasing i and then d;
3. all `V_i+`, `V_i−`, increasing i and then sign as specified.

Each mode retains consecutive groups 0 then 1, all anchors precede all
nonanchors, and all raw entry formulas and nonanchor tree/dummy orders are
unchanged. Moving only the minus modes before plus modes **within each
depth** is a different construction and does not attain this count at
depth three. The global order across depths is essential to excluding
earlier positive-parent supports.

## 1. Anchor classification survives the new order

The nonanchor crown exclusion and same-class comparability depend only on
unchanged entries, so do not require a new mode-order argument. The only
proper inclusion between role supports is a child parity half inside a
whole class. On the row axis each such W-mode half precedes both available
V-mode whole supports because all W modes precede all V modes. At a shared
leaf this remains true for both signs; equal or disjoint parity halves
introduce no extra proper inclusion.

On the column axis, a nonleaf signed half from `W_i^sign` can be contained
in the whole parent role of `W_(i+1)^sign` or `V_(i+1)^sign`. The first is
later inside its own sign family; the second is in the final V family.
Whole leaf column supports do not occur. Dummy supports are equal or
disjoint from other supports. Thus every proper container is still later,
including both axis-specific cases and the shared leaves.

I rechecked the complete anchor-count exhaustion, rather than assuming
that the previous list of configurations is preserved:

- If a,b≥2, the crossed leading ones and the common mode order force the
  first two selected rows and columns into one mode and opposite groups.
  Distinct H rows/columns prevent reuse of a twin block. Any further anchor
  would have the wrong zero signature, so a=b=2.
- If a≤1 and b=0, the prescribed nonanchor 3×3 crown is impossible.
- If a≤1 and b=1 or 2, the first anchor column puts rows 2 and 3 into one
  class, but their traces on nonanchor columns 3 and 4 are incomparable.
- If a≤1 and b≥3, anchor columns 1 and 3 would give a proper container
  before the support it contains, contradicting the revised support order.
- If a≥3 and b≤1, anchor rows 1 and 3 give the analogous contradiction.
- The remaining case (a,b)=(2,0) is excluded because anchor row 2 puts
  columns 1 and 4 into one class while their nonanchor traces cross.

These are all possibilities, so exactly (2,2) and (2,1) remain. This uses
the rank in the **new common order**, not a numerical assumption that mode
depths increase globally.

## 2. Localization: every order-sensitive case checked

The balanced four-mode analysis uses designated roles and the unchanged
tree orders, not relative order between different modes. It therefore still
forces a terminal minus-horizontal mode, leaf p, its negative parent column,
the same leaf column p, and a dummy last row.

For the unbalanced case, let B be the second anchor row/first anchor column
mode. The fixed zero forces the second row's group to be 1 and first column's
group to be 0: the reverse orientation would make one of the zero's
endpoints dummy. Let A be the first anchor row's mode. Then A≤B in the new
order, and its positive support contains the two middle selected columns.
They lie in one nondummy class. Write r for leaf-candidate row 3, c for
column 3, and d for column 4. The needed hypotheses are
`r∈rowrole_0(B)`, `d∈colrole_1(B)`, `c∈colrole_g(A)`,
`A(r,c)=1`, `A(r,d)=0`, and `c<d`.

The exhaustive B-mode analysis remains valid:

| B | Exclusion or localization |
| --- | --- |
| V+ | The zero says parent(p)>b. A one in the own-plus, parent-plus, or extra leaf parent-minus class, together with c<d, forces parent(p)≤b. |
| V− | The zero says p≥b. An own-minus one requires p<a≤b; a preceding-minus one requires parent(p)<a<parent(b). Both are impossible. There is no preceding class at the root. |
| W+ | The zero says p>q with equal parity. Own-class or parent-plus ones and c<d force p≤q; the extra leaf parent-minus case gives an even stronger strict contradiction. |
| W− | Parent-minus c is impossible. An internal own-minus one would require p<q while parent(p)≥b≥parent(q), forcing p even and q odd. But an earlier mode supporting this class must be W− at the same depth with parity at most B's; later W− parent roles and all V roles are excluded by the new order. This contradicts the required parities. |

Thus W− is terminal. Its remaining own-leaf or positive-parent c yields
`parent(p)=b` exactly as in the prior proof. No argument here assumes that
an arbitrary A≤B has smaller depth. That tempting implication is false
under the new global order and is not needed.

The new order gives a stronger terminal conclusion. A positive-parent c
would require a support from a plus W mode or V mode, all later than the
terminal minus B, so it is excluded. A leaf c can only have support from
`W−_(h,e)` group 0 among modes no later than B. Hence e≤d, where p=2b+d.
The leaf one and localization give p≤q and parent(q)=b, forcing e≥d.
Consequently e=d, q=p, and A=B with group 0.

The second selected column is therefore an earlier leaf q0 of the same
parity, with q0<p. A variable row one at q0 must itself be a leaf of index
at most q0. It cannot occur after leaf row p. Thus the last row is dummy.
This directly re-establishes the last-row claim under the new order.

In fact the weaker local premises above already imply A=B, a terminal
minus mode, g=0, c=leaf p, and d=the matching negative-parent block. The
finite generic audit tested this stronger conclusion without imposing all
other constraints of a full copy.

## 3. Exact enumeration and small depths

There are exactly two disjoint families. Write p=2b+d,
`0≤b<m/2`, `d∈{0,1}`.

- Balanced: both anchor groups on each axis belong to `W−_(h,d)`;
  the other rows are leaf p and dummy, and the other columns are leaf p
  and its negative-parent block. There are m leaf choices, four independent
  anchor representatives of size m, m dummy choices, and two parent-column
  choices: `2m^6`.
- Unbalanced: rows are mode-B group 0, mode-B group 1, leaf p, dummy;
  columns are mode-B group 0, an earlier same-parity leaf q0, leaf p,
  and the negative-parent block b. There are b choices for q0. The three
  independent anchor representatives, dummy representative, and two parent
  positions contribute `2m^4` for each choice of p,q0.

Every listed selection satisfies all sixteen entries and both independent
orders. Conversely the preceding classification forces exactly these
selections. The multiplicity is over actual positions, not just block names.
The families are disjoint by their anchor-column counts, and each copy's
parameters and representatives are uniquely recoverable.

Putting t=m/2 gives

\[
2m^4\sum_{b=0}^{t-1}\sum_{d=0}^1 b
=2m^4t(t-1)=\frac12m^6-m^5.
\]

Adding the balanced contribution gives the announced count. This formula
is valid **already at h=1**, where b=0 and the unbalanced family is empty:
`(5/2)·2^6−2^5=128`. There is no inherited h=2 parity exception or missing
parent-half family, because every positive-parent family is now excluded.

## 4. Exact unrestricted repair distance transfers with a proof

The lower bound m² is unaffected by changing relative mode order. Each
protected path uses a designated anchor frame within a single mode; its
group order, position before the body, tree body order, and entries are
unchanged. The original probability/fiber bound also does not depend on
relative mode order. Its contradiction applies to every binary repair,
including arbitrary anchor edits and both directions of bit changes.

For the upper bound, use **Erebos's terminal-first-anchor-column repair**:
zero the entire nonanchor-row portion of group 0 of `W−_(h,0)` and
`W−_(h,1)`. Its only changed cells are the initially-one incidences from
leaf p to the m columns of the group indexed by p's parity. Thus it makes
exactly m² distinct physical edits. This repair and its idea must remain
attributed to Erebos; they are not a new invention of this refinement.

I checked each step needed to transfer freeness, rather than using old
localization on the edited matrix:

1. Any matrix agreeing on every anchor row has nonanchor third and fourth
   rows in every H copy. If row 3 were anchor, the first three rows would
   be anchor. An anchor first column would force rows 2 and 3 into one
   twin group despite their distinct traces. A nonanchor first column
   would put the first three columns in one class through overlapping
   anchor supports. That class has at most two full anchor-row signatures
   (parity determines variable signatures; dummy has one), whereas the
   three required traces are 011,100,101. Neither argument uses relative
   order of different modes.
2. In the proposed repair, terminal group-0 columns are zero on every
   nonanchor row. Every H column has a one in its last two rows. Hence no
   copy in the repaired matrix can use any of these columns. Outside
   them the matrix is unchanged, so any new copy would be an old copy.
3. Every old copy, by the new classification above, uses group 0 of its
   terminal minus mode as its first column. This contradicts step 2.

The repaired matrix is therefore H-free at every depth, and the unrestricted
lower bound makes its m² edits optimal. The normalized distance equals
`(14h+2)^−2`. No compression restriction is imposed on competing repairs.

The actual candidate's Section 8 uses a shorter alternative to step 1's
two-signatures argument when the first column is nonanchor. The first and
third selected anchor rows have overlapping nonanchor supports, with the
first containing column 2 that the third omits. Laminarity forces the first
support to be a **proper** container. Lemma 2 says that container's mode is
later, contrary to the order of the two anchor rows. This is valid because
these complete anchor rows remain unchanged, so their original supports can
be used. It does not assume the edited matrix itself retains laminarity for
other rows or retains original-copy localization. The claim needed here is
for this new order; it need not extend to every permutation in the larger
restricted-optimality comparison class.

## 5. Restricted optimality: valid and carefully bounded

For **any** independent mode-block permutations on the two axes, every balanced family member
above still exists. So does every unbalanced member described above. All
selected anchors in each member lie in **one** terminal minus mode; no
comparison between different modes appears in either embedding. The two
anchor groups remain ordered 0<1, anchors remain before nonanchors, and
the nonanchor orders and entry formulas remain fixed.

Consequently every member of this restricted family has at least
`2m^6 + (m^6/2−m^5)` copies, whether or not its other copies localize and
whether or not its support order is laminar. The global minus-first order
attains this lower bound, proving optimality within the stated class. This
is a mathematical lower bound from unavoidable explicit copies, not a
claim inferred from searching a finite list of permutations.

The argument does not assert uniqueness of the minimizing order. It does
not cover changing within-mode group order, interleaving anchor groups,
moving anchors among nonanchors, changing tree orders or entries, changing
group sizes, or arbitrary matrices at the same repair distance. No global
copy-density optimum or forbidden-pattern minimality follows. Independent
permutations do not require re-proving a common-mode anchor classification
for arbitrary members of the comparison class: the lower bound uses the
explicit two single-mode families only. This is why the expanded statement
in the actual Section 6 is justified.

## 6. Uniform blowups and stronger size quantifiers

The actual Section 9 blowup argument is sound. Interpret the blowup factor
as a positive integer ℓ and replace each physical row and column by ℓ
consecutive identical clones. Every H-copy uses distinct original row
fibers and distinct original column fibers, since two clones from one
fiber would give equal H rows or columns. Projection is thus strictly
increasing on both axes and gives an original copy. Each original copy has
exactly ℓ⁸ lifts. This argument also applies to the H-free repaired base
matrix, so blowing up that repair is H-free and costs exactly ℓ²m².

For the lower bound, let an arbitrary H-free binary matrix B on the blowup
axes have M edits relative to the blown-up original host. Choose one uniform
row representative from each original row fiber and one uniform column
representative from each original column fiber, with the two choices
independent. Each physical changed cell is sampled with probability ℓ⁻²,
so the expected edit count of the restriction relative to the original host
is M/ℓ². Every restriction is H-free, since an ordered copy would lift to B.
If M<ℓ²m², some restriction would violate the unrestricted base lower bound.
Thus the exact normalized distance, as well as density, is preserved.

For any c,C,η>0 and finite-valued threshold function L on (0,1), choose h
sufficiently large to have epsilon_h<η and density<c epsilon_h^C. Then
choose a positive integer ℓ so that ℓn_h≥L(epsilon_h). This ordering of
choices establishes arbitrarily small positive epsilon and arbitrarily
large allowed matrix size after epsilon is chosen. There is no unjustified
interchange of the epsilon and size quantifiers, nor a claim that every
large integer size is realized without padding.

## 7. Honest quantitative announcement

For h≥2, the ratio to Erebos's exact count at the same h is

\[
\frac{N_{\rm new}}{N_{\rm Erebos}}
=\frac{10m-4}{41m-74}\longrightarrow\frac{10}{41}.
\]

The relative reduction is `(31m−70)/(41m−74)`, approaching
`31/41 ≈ 75.609756%` from below. It is 60% at h=2, about 70.0787% at
h=3, and about 73.1959% at h=4. At h=1 the two hosts have equal counts.
Using Erebos's h≥2 formula at h=1 would give an incorrect comparison.

The exact new normalized density is

\[
(\tfrac52-2^{-h})(14h+2)^{-8}4^{-h}
=(\tfrac52-2^{-h})\epsilon_h^4 4^{-h}.
\]

The same fixed H4, n, exact epsilon, and exponent make the count comparison
meaningful, but the improvement is in the leading constant. The qualitative
failure of polynomial removal and the exponential scale are unchanged.
An accurate concise announcement would be:

> A candidate refinement of the same 4×4 obstruction has asymptotically
> 75.6% fewer ordered copies at identical host size and exact repair distance.
> Its count is optimal among permutations of the fixed anchor-mode blocks.

The proof/checking stage should be stated alongside that announcement:
this newly ordered host currently has a written all-depth argument and
separate-agent exact checks; prior Lean verification is for the earlier
order. A statement that this new refinement is already Lean-certified
would need a new order-specific build and theorem audit.

The corrected Section 9 also states two valid consequences of its stronger
shape theorem. Every copy contains the actual leaf-row/leaf-column cell p
at pattern position (3,3). Hence those m cells form an original-copy hitting
set, giving `N_H≤m n^6` and canonical sampling rejection probability at most
`m(q/n)^2` for independent uniform q-row and q-column subsets. Reusing this
as an unrestricted repair claim would be invalid; the text explicitly
distinguishes those statements. The count and probability bounds concern
the base host and valid sample sizes `0≤q≤n`.

## Corrections found in the actual text

I reported the following issues in the first `optimized-order.md` snapshot;
all substantive corrections were confirmed by rereading the changed text.

- **False inherited sentence, corrected:** original lines 350–352 said
  that the leaf-diagonal hitting set was insufficient and that some
  unbalanced copies lacked a leaf column. This was true for the previous
  order but false here: Section 6 forces the leaf-diagonal cell in every
  copy. It did not invalidate the main proof, but contradicted the new
  classification and obscured the sharper hitting-set corollaries. The
  replacement correctly distinguishes the old and new orders.
- **Proof-stage overstatement, corrected:** the end of Section 7 originally
  concluded exact distance from its lower-bound argument alone. It now
  states `≥`, with equality supplied by Section 8's explicit repair.
- **Notation, corrected:** the inherited host-size discussion used `s`
  without first saying `s=2`; Section 1 now does so. The arbitrary blowup
  multiplicity is now explicitly a fresh integer `ℓ≥1`, and the threshold
  function is explicitly `L:(0,1)→ℕ`, as needed for the quantifiers above.

After those corrections I found **no material mathematical issue** in the
reviewed argument. This verdict is limited to the stated construction and
comparison class and is not worldwide novelty certification.

## Executed checks and reproducibility

The independently written standard-library checker is
`.context/refinement-work/reviewer-global-order-checks.py`; output is
`.context/refinement-work/reviewer-global-order-output.json`. It imports no
candidate or Erebos implementation. Unlike the existing row-quadruple
checker, it constructs recursive axes, scans **all column quadruples**, and
enumerates every matching increasing row quadruple from four bitmasks.
It checks all entries before examining any proposed structural property.

Run from the root repository:

```sh
python3 .context/refinement-work/reviewer-global-order-checks.py > .context/refinement-work/reviewer-global-order-output.json
```

Executed under Python 3.9.25, exit code 0:

| h | New copies | Balanced | Unbalanced | Copies after repair | Actual edits |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 128 | 128 | 0 | 0 | 4 |
| 2 | 9,216 | 8,192 | 1,024 | 0 | 16 |
| 3 | 622,592 | 524,288 | 98,304 | 0 | 64 |
| 4 | 40,894,464 | 33,554,432 | 7,340,032 | 0 | 256 |

The same scan independently reproduces Erebos and previous local counts
through h=3. A full physical scan at h=1 agrees with compression for both
the original and repaired host. Compression here is valid because entries
are constant on twin blocks, even after the explicit repair, and H has
distinct rows and columns. It is **not** a reduction of arbitrary optimal
repairs to block-constant repairs.

For every h=1,...,7 the checker also exhausts all role-support pairs on each
axis, verifies laminarity/proper-container order, and tests the generic
localization premises over all A≤B and both first-anchor groups. There are
respectively 2,4,8,16,32,64,128 surviving generic triples, all satisfying the
stronger terminal single-mode conclusion. This does not assume the full-copy
signature exclusions or the exact enumerated families.

Finite checks provide implementation and boundary evidence, not proof of
the unbounded statements. The all-depth conclusions reviewed above come
from the explicit classification, enumeration, repair, and unavoidable-family
arguments. No new formal build, unrestricted global optimality, or conclusive
worldwide novelty assessment is claimed.

## Final reviewed snapshots and repository check

The proof and synchronized manuscript bodies were compared directly; they
agree apart from the necessary relative-link prefixes. Exact SHA-256
snapshots of the proof, manuscript, inspected Erebos proof/Lean sources,
the unchanged prior `ConcreteHost.lean`, and the executed checker/output
are preserved in
`.context/refinement-work/reviewer-optimized-order-snapshots.json`.

| Artifact | SHA-256 |
| --- | --- |
| `proofs/optimized-order.md` | `b9999c71e37e41430b8094cd41494ffddfbec2200db2cb88b71fbbcf8df78ce4` |
| `manuscript.md` | `e0ec4e87fc4d1d638fa1d257794b8d1a5f28dcadcaa079100dc8eb900af302e3` |
| Reviewer checker | `e07c6a8598e2ceba68d76dfb6e4cfd3b89733335ef2dc1c31ea98c6574d91f5f` |
| Actual reviewer output | `338f54f83aecbedd8217270c42c7c35faa2c9e09e3ce0321bb1e8230427f4bfb` |

Root `python3 scripts/validate_repository.py` passed after the review:
34 tracks in 7 groups and 401 local links across 112 Markdown files.
This command checks repository consistency, not the universal mathematics.
I did not execute a Lean build for the new order or alter prior formal
verification records. The project-wide candidate checker/build run is
separate from the specifically executed reviewer checks reported above.
