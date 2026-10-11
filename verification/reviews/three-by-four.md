# Separate-agent review of the 3×4 candidate

Reviewer: `/root/four_proof_reviewer`. Date: 2026-10-11.

## Verdict and scope

The construction has an all-depth localization argument: every ordered
copy of `1001/1010/0111` has one anchor row and one or two anchor columns;
its second row is a leaf, and its fourth column is the minus block of
that leaf's own parent. The last row is necessarily dummy. I found no
counterexample or unresolved anchor-count case. The arbitrary-repair
lower-bound transfer and uniform blowup argument are valid at their stated
interfaces. No exact optimal repair or exact all-depth enumeration is
established by this review.

One required correction was reported in the first written draft: the
same-level, opposite-sign column comparisons must be restricted to
nonleaf levels `j<h`. Without that restriction, one displayed equivalence
is false at the identified leaf with equal nodes. Its actual applications
in the proof are at nonleaf parent levels, so this is a statement error,
not a counterexample to localization. Final correction status and source
snapshots are recorded at the end of this report.

This is a separately executed AI review, not independent human peer
review, a new Lean verification, or a certification of worldwide novelty.
It does not transfer the older 4×4 formal certificate to the new host.

## Material inspected and work performed

I read the root `AGENTS.md`, the prior standalone track's `AGENTS.md`,
the complete new `problems/190-ordered-binary-removal/proofs/three-by-four.md`,
the construction and role definitions in the existing `host.py`, and
the discovery code `search_asymmetric_templates.py`,
`search_asymmetric_completion.py`, and `search_asymmetric_rules.py`.
I also inspected the new `verification/check_three_by_four.py`.
The supplied `simple-rule-checks.json` is reported discovery evidence;
I did not treat its empty witness lists as an all-depth proof.

Before the written draft was available, I independently worked through
the anchor-count cases, supplied the complete `(a,b)=(1,0)` exclusion,
and supplied the two- and three-anchor-row support classification to the
coordinator. I then checked the resulting written draft for omitted cases,
strict inequalities, the leaf boundary, protected sampling, and blowups.

The fresh checker
`.context/asymmetric-190/reviewer-three-by-four-checks.py` imports no
candidate or discovery code. It constructs axes recursively and scans
all column quadruples, then every matching increasing row triple. This
differs from the candidate verifier's sorted coordinate axes and weighted
subsequence dynamic programming. The checker's formulas are separately
written definitions of the stated host; agreement between finite programs
does not replace the argument below.

## All-depth case audit

Let `P_i=C_i^-`, and let `D` be the dummy column block. Apart from their
same-mode group-0 anchor column, the anchor-row supports are exactly:

| Mode | Nonanchor one-support |
| --- | --- |
| `V_i^s` | full class `C_{i-1}^s` |
| `W_{i,d}^+` | `D` and parity-d half of `C_i^+` |
| `W_{i,1}^-` | `D` and full `P_{i-1}` |
| `W_{i,0}^-`, `i<h` | `D`, full `P_{i-1}`, odd half of `P_i` |
| `W_{h,0}^-` | `D` and full `P_{h-1}` |

This review analyzes the stated rule, which has no odd-child addition at
leaves. It makes no claim about a variant adding odd leaf columns; those
columns would still be outside the even-leaf designated first column role.
The two prescribed column roles have top signature `01`, and the
two prescribed row roles have anchor-column signatures `10` and `01`.

Write `a,b` for anchor row and column counts. Anchor positions are prefixes,
and distinct rows and columns of H prohibit selecting two physical twins.

### No anchor rows

For `a=b=0`, columns 1,3,4 give an induced crown. The unchanged nonanchor
body is crown-free: same-class neighborhoods are nested, and at the class
level the only triple of column classes with pairwise nondummy common
neighbors is the leaf class and its two parent-sign classes. The leaf
traces on that triple are nested, and nonleaf rows have no leaf-column
ones, preventing the required incomparable traces.

For `a=0,b=1 or 2`, the first anchor column puts the first two rows in the
same class, while their nonanchor-column 3,4 traces are incomparable.
For `a=0,b>=3`, column supports with traces `110` and `011` cross,
contradicting the unchanged laminarity of anchor-column supports. Thus no
case with `a=0` survives.

### Two or three anchor rows

For `a>=2,b>0`, column 1 forces the first two anchor rows into the same
mode's single twin block, impossible.

Suppose `b=0`, and let `A<B` be the first two anchor modes. If `c1` is
variable, the supports have a variable intersection and exclusive columns
`c3` and `c4`, with `c4` also variable. The complete crossing-pair list is

`A=W^-_{i,0}`, `i<h`, and `B=W^-_{i+1,d}` or `V^-_{i+1}`.

The other crossing pair with variable intersection is
`W^+_{i,d},V^+_{i+1}`, whose first-only part is just dummy, excluded by
`c1<c4`. Same-level minus supports are nested, and all other choices have
disjoint variable parts or no required exclusive part. For the displayed
list, `c1` is odd `P_i`, `c4` lies in `P_{i-1}`, and `c3` lies in even
`P_i`, or possibly odd `P_{i+1}`.

For `a=2`, `c1` is variable because its bottom entry is zero. A nondummy
row cannot see both `P_{i-1}` and `P_{i+1}`, so `c3` is even `P_i` and the
last row lies in `R_i^-`. That row's entire nonanchor support is contained
in `D ∪ P_{i-1} ∪ P_i`, which is covered by the first two anchor supports.
There is therefore no column with trace `001`.

For `a=3` and variable `c1`, no anchor-row support sees both `c4` in
`P_{i-1}` and either allowed class/parity of `c3`: the only support spanning
the adjacent minus levels includes odd children, whereas `c3` is even.
The other possibility has a gap of two levels.

For `a=3` and dummy `c1`, its trace `110` forces the first two modes to be
W and the third to be V. The last three columns must lie in the V support,
one whole class K. A W support restricted to K is empty, full, or a parity
half. The two exclusive columns force opposite halves, covering K and
leaving no `001` column. This also closes the dummy exception.

### One anchor row, with zero or at least three anchor columns

For `a=1,b=4`, both columns 1 and 4 would be in the same anchor-column
twin block, impossible. For `b=3`, column 3 puts the last two rows in the
same class, but the nonanchor column 4 has lower trace `01`, contrary to
the nonincreasing same-class row entries.

For `a=1,b=0`, `c1` and `c3` are variable. The last two rows are nondummy
and in distinct classes. Their common neighbor `c3` forces adjacent signed
row classes, allowing a leaf as the child class. If `c1,c4` lie in one
column class, monotonicity contradicts lower-row entries `1,0`.
Consequently the only possible top mode is `W^-_{i,0}`, `i<h`, and the
two columns occupy `P_{i-1}` and odd `P_i` in opposite orders.

If `c1` is in `P_{i-1}` and `c4` in odd `P_i`, the possible lower classes
are `(R^-_{i-1},R^-_i)` or `(R^-_i,R^-_{i+1})`. The former places common
`c3` in the top support. In the latter, writing nodes as `c1=b,c4=q,r2=p`,
column order gives `b<floor(q/2)`, and `r2*c1=1` gives `floor(p/2)<b`.
Thus `p<q`, contradicting the zero at `(r2,c4)`.

If the two column classes are reversed, the possible lower classes are
`(R^-_i,R^-_{i-1})` or `(R^-_{i+1},R^-_i)`. The former again puts common
`c3` in the top support. In the latter, write row nodes `p,z`. The column
`c2`, with top zero and bottom one, must be an even `P_i` node `u`.
Row order gives `floor(p/2)<z`, and its bottom one gives `z<u`.
Then `(r2,c2)` is one, a contradiction. At `i+1=h` the child class is the
leaf class, with the same minus incidence and order comparisons.

The only remaining configurations are `(a,b)=(1,1),(1,2)`.

### Localization in the surviving configurations

The first column is the top anchor's own group-0 column, so `r2` belongs
to that mode's first row role. Put `c=c3,d=c4`. The generic conditions are
`c<d`, `r2*c=1`, `r2*d=0`, `c` outside the top support and `d` inside it.

For a vertical mode, these force `c` to be dummy. The plus case has
`floor(p/2)>q`; a same-level `c` would give `p<=u` and `floor(u/2)<q`,
while a leaf's minus-parent `c` would give `floor(p/2)<u<q`.
The minus case has `p>=q`, and a preceding-level `c` would give
`floor(p/2)<u<floor(q/2)`. These are contradictions. At `i=1` the minus
preceding-level option is simply absent.

For `b=1`, a nonanchor `c2` cannot precede dummy `c3`. For `b=2`, the
later last row seeing `d` must itself be dummy: every possible variable
row seeing `d` is earlier than `r2` by the threshold inequalities.
Its one at `c2` would require a W group-1 anchor column, all of which
precede the V first column. Thus the vertical dummy exception is closed.

For a positive W mode, `r2` and `d` have equal parity with `p>q`.
A same-level `c` contradicts monotonicity. A plus-parent `c` gives
`floor(p/2)<=u<=floor(q/2)`, impossible for larger same-parity `p`.
A leaf's minus-parent `c` gives the stricter contradictory inequalities.
The dummy is in the top support, so it cannot be `c`.

For a negative W mode, an added odd-child `d` would have `p>=q`, while
an eligible same-level `c` gives `u>p` and `u<q`, impossible. Therefore
`d` is a parent-minus column, node `b`, and `floor(p/2)>=b`.
Below the leaves an eligible `c` has node `q>p` with `floor(q/2)<=b`.
It follows that `p=2b` and `q=2b+1`; the row role has even parity, and
the newly added odd-child support makes this `c` ineligible. This is the
essential all-depth use of the extra ones.

At the leaf, `c` is a leaf node `q>=p` or a plus-parent node `u>=floor(p/2)`.
Column order gives respectively `floor(q/2)<=b` or `u<=b`, so in both
cases `b=floor(p/2)`. A later variable row seeing this minus-parent
column would belong to an earlier parent subtree, which is impossible;
the last row is dummy. No h=1 exception was omitted.

## Repair and quantitative interfaces

Every protected designated body remains extendible using one anchor row
and two anchor columns: the extra dummy and odd-child entries occur outside
the designated roles. The mode orders do not enter this single-mode
extension. The sampled root-to-leaf propagation still imposes opposite
values on the one common leaf diagonal.

In the new sampler a row-anchor position has marginal `1/(2m)`, while
variable, dummy, and column-anchor positions have marginal `1/m`.
The protected cells have an anchor or dummy endpoint, or are root-to-root.
Their endpoint selections have the required independence, so each has
selection probability at most `1/m^2`. This assertion correctly excludes
general variable-variable cells. For fewer than `m^2` arbitrary binary
changes, the union bound finds an untouched protected selection, and the
unchanged frame plus body induction contradict H-freeness. Anchor edits
and both directions of change are included; no monotone-repair premise
has been introduced.

Each leaf row has weight one and its own minus-parent column block has
weight two. The localized zero set therefore has exactly `2m` physical
cells. Once the distinguished zero cell is fixed, at most `n^5` choices
remain, proving `N_H<=2m n^5`. This is an upper bound, not an exact count.
Dividing by `n^7` gives `2/(d^2 m)`. With `epsilon=d^-2`, the ratio to
`epsilon^C` is at most `2d^(2C-2)2^-h`, tending to zero for every fixed
positive C. The square host size agrees on both axes: `12hm+(2h+2)m`.

A uniform positive integer blowup q changes all block sizes by q. The
same protected-cell probability bound becomes `1/(qm)^2`, giving repair
lower bound `q^2m^2`. Leaf row/column representatives are shared between
their two sign interpretations, so the terminal contradiction persists.
Distinct H rows and columns force every copy to project to distinct base
rows and columns; hence the copy count scales exactly by `q^7`.
Thus one can first fix h for the requested epsilon and density inequalities,
then choose q beyond any prescribed finite host-size threshold. No claim
about all integer host sizes, exact repair equality, or a 3×3 pattern follows.

## Executed finite checks

From the root repository, under Python 3.9.25:

```sh
python3 .context/asymmetric-190/reviewer-three-by-four-checks.py > .context/asymmetric-190/reviewer-three-by-four-output.json
```

The command exited 0. Its weighted literal census was:

| h | All copies | One anchor column | Two anchor columns | Quotient witnesses |
| --- | ---: | ---: | ---: | ---: |
| 1 | 1,632 | 32 | 1,600 | 19 |
| 2 | 101,888 | 22,016 | 79,872 | 83 |
| 3 | 4,743,168 | 1,269,760 | 3,473,408 | 306 |
| 4 | 197,525,504 | 57,016,320 | 140,509,184 | 1,092 |

Every occurrence passed the anchor-count, terminal-anchor, leaf/dummy-row,
and own-parent localization assertions. Full physical h=1 agrees with
all 1,632 occurrences. Block compression is justified here by literal
twins and distinct H rows/columns; it does not restrict arbitrary repairs
to block-constant modifications.

The support and generic-localization check exhausts h=1,...,7. The numbers
of crossing support pairs are `0,3,6,9,12,15,18`, all exactly of the form
used above. Generic surviving terminal triples number
`5,10,20,40,80,160,320`; the only other generic survivors are the vertical
dummy exceptions, numbered `1,6,28,120,496,2016,8128`. Every such exception
also passes the claim that a later row seeing the last column must be
dummy. This deliberately tests the weaker generic premises before the
full-copy argument removes the vertical exceptions.

The coordinator's h<=6 enumeration, negative controls, and project-wide
checks are separate runs. I inspected their verifier but do not present
those as executions of this reviewer. Finite checks do not establish the
unbounded statements; the arguments above supply the reviewed universal
case analysis.

## Corrections and final snapshots

I reread the corrected draft. It now explicitly restricts both same-level
cross-sign column comparisons to `j<h`, treats the absent `C_{i-2}` class
at `i=1`, and makes the blowup multiplicity a positive integer. No required
mathematical correction remains in the reviewed proof snapshot.

The coordinator also caught an incorrect counterfactual sentence in the
first version of this review: I had said adding odd-child ones at the leaf
would affect prescribed role entries. Odd leaves are outside the relevant
even-leaf role, so that assertion was wrong and has been removed. The proof
and checker consistently use the specified rule with no leaf addition;
neither depended on that mistaken sentence. No claim about the alternate
variant is needed or certified here.

Exact SHA-256 hashes are preserved in
`.context/asymmetric-190/reviewer-three-by-four-snapshots.json`.

| Artifact | SHA-256 |
| --- | --- |
| Corrected `proofs/three-by-four.md` | `e02bd9938930d043cfadd71738020b8993acfcc3ebe317f63cbcfc66520ad226` |
| Reviewer checker | `6eace45d002a86243d597dced381ea59effa83271fcf2dfb4eb55ba0410939dd` |
| Executed reviewer output | `ca9b90ef3f7a7fa2ad63c00597061417673d0fa9eff9fe5cb57ecacce2988d60` |

Root `python3 scripts/validate_repository.py` was executed and reported
only a stale generated `STATUS.md` during the coordinator's concurrent
catalog update. I did not regenerate shared views in this read-only review.
The coordinator is handling final repository validation after archiving
these artifacts. I performed no new Lean build or project-wide formal
check for this 3×4 result.
