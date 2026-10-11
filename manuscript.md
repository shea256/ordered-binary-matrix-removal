# A 3×4 ordered binary removal obstruction

October 11, 2026. **Candidate result with a written all-depth proof.**
The exact finite checks use two implementations. A separate agent reviewed
the argument; this is not independent mathematical peer review. This new
host and main theorem are now checked in Lean, including the full quantifiers.
See the source-bound audit and verification scope in Section 8.

The tree, threshold entries, mode roles, and arbitrary-repair sampler are
inherited from OpenAI's September 25 manuscript. Erebos previously proved
the 4×4 obstruction and exact repair equality. Our construction changes the
anchor encoding, retaining the globally ordered modes from the preceding
[4×4 quantitative refinement](proofs/optimized-order.md). The new ingredient is
one anchor row with nonuniform extra ones, described explicitly below.

## Statement

The fixed rectangular pattern is

\[
 H=\begin{pmatrix}1&0&0&1\\1&0&1&0\\0&1&1&1\end{pmatrix},
 \qquad P=\begin{pmatrix}1&0\\1&1\end{pmatrix}.
\]

For every integer h≥1, set m=2^h, d=14h+2, n=dm. The square binary host
A_h below satisfies

\[
 \operatorname{dist}_H(A_h)\ge d^{-2},\qquad
 N_H(A_h)\le 2mn^5,\qquad
 \frac{N_H(A_h)}{n^7}\le 2d^{-2}2^{-h}.
\]

Copies use three increasing distinct rows and four increasing distinct
columns and match all twelve entries. Distance allows arbitrary binary
changes in either direction anywhere in the host, normalized by n².
No equality for repair distance or exact all-depth copy count is claimed.

Consequently, for all c,C>0 and every ε₀>0, there exists 0<ε<ε₀ such that
hosts of arbitrarily large order are ε-far from H-freeness and have fewer
than c ε^C n^7 copies. In particular H admits no polynomial removal bound.
This reduces the pattern from the known 4×4 to 3×4 (16 to 12 entries);
it does not establish a 3×3 obstruction or minimality.

## 1. The host, including every binary entry

Use a complete binary tree of height h, with nodes p=0,…,2^i−1 at depth i.
For i<h put row blocks R_i^−(p),R_i^+(p) and column blocks
C_i^−(p),C_i^+(p), each of size m/2^i. At depth h identify the two signs:
R_h^−(p)=R_h^+(p)=L_R(p) and C_h^−(p)=C_h^+(p)=L_C(p), each of size one.
Add dummy blocks R_*,C_* of size m. A class omits the node index and
denotes the union over its level; a parity subscript restricts node parity.

Rows follow recursive order: minus block, left subtree, right subtree,
plus block. Columns follow plus block, left subtree, right subtree, minus
block. A leaf block occurs once. Dummy rows are last, dummy columns first
among nonanchors. Positions within a block are twins.

Every nonanchor entry meeting a dummy is one. All variable entries are
zero except the following threshold entries:

| Row / column | Value | Range |
| --- | --- | --- |
| R_i^+(p), C_i^+(q) | 1[p≤q] | 0≤i≤h |
| R_i^−(p), C_i^−(q) | 1[p<q] | 0≤i<h |
| R_i^+(p), C_{i−1}^+(q) | 1[⌊p/2⌋≤q] | 1≤i≤h |
| R_i^−(p), C_{i−1}^−(q) | 1[⌊p/2⌋<q] | 1≤i≤h |

The last two rules both apply to a leaf row, with different column signs.
There is no conflicting minus diagonal rule at leaves.

There are six modes at each i=1,…,h, with these disjoint roles:

| Mode | Row role 1 | Row role 2 | Column role 1 | Column role 2 |
| --- | --- | --- | --- | --- |
| V_i^+ | R_i^+ | R_{i−1}^+ | C_* | C_{i−1}^+ |
| V_i^− | R_{i−1}^− | R_i^− | C_* | C_{i−1}^− |
| W_{i,d}^+ | R_{i,d}^+ | R_* | C_{i−1}^+ | C_{i,d}^+ |
| W_{i,d}^− | R_{i,d}^− | R_* | C_{i,d}^− | C_{i−1}^− |

For each mode t add **one row anchor block X_t of size 2m** and **two
column anchor blocks Y_{t,0},Y_{t,1}, each of size m**. Put anchors before
all nonanchors. On both axes order modes as

\[
 (W^-_{1,0},W^-_{1,1},\ldots,W^-_{h,0},W^-_{h,1}),\quad
 (W^+_{1,0},W^+_{1,1},\ldots,W^+_{h,0},W^+_{h,1}),\quad
 (V^+_1,V^-_1,\ldots,V^+_h,V^-_h).
\]

Within each column mode, group 0 precedes group 1. Anchor row X_t is one
on Y_{t,0}, zero on every other anchor column. A nonanchor row in row
role j∈{1,2} of t has signature e_j against (Y_{t,0},Y_{t,1}); a row
in neither role has signature 00.

It remains to specify each anchor row on nonanchor columns. Write D=C_*.
Its one-set T_t is exactly:

| Anchor row mode | T_t |
| --- | --- |
| V_i^σ | C_{i−1}^σ |
| W_{i,d}^+ | D ∪ C_{i,d}^+ |
| W_{i,1}^− | D ∪ C_{i−1}^− |
| W_{i,0}^−, i<h | D ∪ C_{i−1}^− ∪ C_{i,1}^− |
| W_{h,0}^− | D ∪ C_{h−1}^− |

In particular the odd-child addition is **absent at the common leaves**.
All unspecified entries are zero. The added dummy and odd-child ones
are outside the designated column roles. On those roles each X_t still
has signature (0,1), as required by H's last two columns. Together with
the prescribed row signatures, every ordered designated P extends to H.

Each axis has 12hm anchor positions and (2h+2)m nonanchor positions.
Thus the host is square with n=(14h+2)m.

## 2. Elementary support and order facts

At a fixed signed level, blocks occur in increasing node order. For a
fixed nonanchor row, entries along a column class are nondecreasing;
for a fixed nonanchor column, entries along a row class are nonincreasing.
Thus same-class rows or columns have nested neighborhoods.

Nonanchor rows and columns contain no unordered 3×3 crown J₃−I₃.
Here is the inherited argument. Same-class columns cannot occur in a crown.
A nondummy nonleaf row is supported on its own and preceding signed column
classes. A leaf row is supported on L_C,C_{h−1}^+,C_{h−1}^−. Hence three
distinct classes with pairwise common nondummy neighbors must be those
three terminal classes. On fixed columns from those classes, leaf traces
are nested as the leaf node increases, and nonleaf rows have zero on L_C.
They cannot provide both required incomparable traces with a one on L_C.

The one-set of any anchor column on nonanchor rows is a whole class or
a parity half-class. Any two such sets are disjoint or nested. No mode
order assumption is needed for this laminarity statement.

We repeatedly use the recursive-order comparisons, with π(p)=⌊p/2⌋:

\[
\begin{aligned}
 C_{i-1}^+(b)<C_i^\sigma(q)&\iff b\le\pi(q),&
 C_i^\sigma(q)<C_{i-1}^+(b)&\iff\pi(q)<b,\\
 C_i^\sigma(q)<C_{i-1}^-(b)&\iff\pi(q)\le b,&
 C_{i-1}^-(b)<C_i^\sigma(q)&\iff b<\pi(q),\\
 C_j^+(a)<C_j^-(b)&\iff a\le b,&
 C_j^-(a)<C_j^+(b)&\iff a<b,\\
 R_i^+(p)<R_{i-1}^+(a)&\iff\pi(p)\le a,&
 R_{i-1}^-(a)<R_i^-(p)&\iff a\le\pi(p).
\end{aligned}
\]

The two same-level cross-sign comparisons require j<h; at depth h the
signs are identified. Child signs in the parent/child comparisons may be
the common leaf sign. Reversing a strict block comparison
gives its complementary strict inequality. These facts follow directly
from the consecutive left-to-right subtree intervals.

## 3. Exactly one anchor row and one or two anchor columns

Consider a copy on rows r₁<r₂<r₃ and columns c₁<c₂<c₃<c₄. Let a,b count
the selected anchors on each axis. Anchors are prefixes. H has three
distinct rows and four distinct columns, so no twin block can be reused.

**No anchor rows (a=0).** If b=0, columns 1,3,4 form a crown, impossible.
If b=1 or 2, column 1 places rows 1 and 2 in one class, but their traces
on nonanchor columns 3,4 are 01 and 10. If b≥3, anchor columns 1 and 3
have traces 110 and 011, contradicting laminarity.

**At least two anchor rows with b>0.** Column 1 is one on the first two
anchor rows. It can only meet one mode's row block, so those rows would
be twins, impossible. Hence a≥2 requires b=0.

For the next cases let A<B be the modes of the first two anchor rows.
Their supports must have a common c₁ and exclusive columns c₃∈T_B∖T_A,
c₄∈T_A∖T_B. If c₁ is variable, c₄ cannot be dummy since c₁<c₄.
Inspection of the explicit support table leaves precisely

\[
 A=W^-_{i,0},\quad i<h,\qquad
 B=W^-_{i+1,d}\ \text{or}\ V^-_{i+1}.
\]

Indeed the only other crossing pair with variable intersection is
W_{i,d}^+,V_{i+1}^+, whose first-only part is dummy. Same-level minus
supports are nested, disjoint-level supports have no variable intersection,
and vertical supports are single distinct classes. For the displayed pairs,
c₁ is in odd C_i^−, c₄ in C_{i−1}^−, and c₃ in even C_i^−, or possibly
odd C_{i+1}^− when B=W^-_{i+1,0} with i+1<h.

**Two anchor rows (a=2,b=0).** Column c₁ is variable since its bottom
entry is zero. In the displayed pair classification, a nondummy row
cannot be one on both C_{i−1}^− and C_{i+1}^−. Therefore c₃ is in even
C_i^− and r₃ must be in R_i^−. Its entire nonanchor one-support lies in
D∪C_{i−1}^−∪C_i^−, covered by T_A∪T_B. This contradicts c₂'s trace 001.

**Three anchor rows (a=3,b=0).** If c₁ is variable, the same pair
classification applies. No anchor row is one both on c₄∈C_{i−1}^− and
c₃ in even C_i^− or odd C_{i+1}^−: the sole support spanning the adjacent
minus classes adds only odd children. If c₁ is dummy, its trace 110
forces the first two modes to be W and the last to be V. The V support
is one full class K, so c₂,c₃,c₄ all lie in K. A W support restricted
to K is empty, all of K, or one parity half. The exclusive c₃,c₄ force
opposite halves, whose union covers K; there is no c₂ with trace 001.

It follows that a=1. If b=4, c₁ and c₄ must both be the sole group-0
anchor class on which r₁ is one; these are twins, impossible. If b=3,
column c₃ places r₂,r₃ in one row class, whereas the nonanchor c₄ has
trace 01 on them, contradicting nonincreasing same-class row entries.

**No anchor columns (a=1,b=0).** Column c₁ is not dummy, since its bottom
entry is zero; c₃ is not dummy either, since c₁<c₂<c₃. Both lower rows
are nondummy and lie in different classes, since their column traces
include both 10 and 01. Their common one at c₃ forces adjacent signed
row classes, possibly including the terminal leaf class.

For a V mode, a W^+ mode, or an unextended W^− mode, c₁,c₄ lie in one
column class. Their order contradicts r₂·c₁=1,r₂·c₄=0. The sole remaining
mode is W^-_{i,0}, i<h. Put P₀=C_{i−1}^− and Q₀=odd C_i^−; c₁,c₄ must
lie in different classes.

If c₁∈P₀ and c₄∈Q₀, the lower row classes are either
(R_{i−1}^−,R_i^−), forcing their common c₃ into P₀ where its top entry
is one, or (R_i^−,R_{i+1}^−). In the latter case, write c₁=P₀(b),
c₄=Q₀(q), r₂=R_i^−(p). Column order gives b<π(q), while r₂·c₁=1 gives
π(p)<b. Hence p<q, contradicting r₂·c₄=0.

If c₁∈Q₀ and c₄∈P₀, the lower row classes are either
(R_i^−,R_{i−1}^−), again forcing c₃ into P₀, or
(R_{i+1}^−,R_i^−). In the latter case let r₂ have node p and r₃ node z.
Since c₂ has top zero and bottom one, it must be an even C_i^− column
with node u: dummy and P₀ are in the top support. Row order gives
π(p)<z; the bottom entry gives z<u. Thus r₂·c₂=1, contradicting its
required zero. If i+1=h, the same minus incidences and row-order comparison
hold with the common leaf class. This finishes the b=0 exclusion.

We have proved (a,b)∈{(1,1),(1,2)}.

## 4. Every copy uses its own terminal minus parent

Let t be r₁'s mode. Column c₁ is Y_{t,0}, so r₂ belongs to row role 1
of t. The remaining conditions include

\[
 c_3<c_4,\quad A(r_2,c_3)=1,\quad A(r_2,c_4)=0,
 \quad c_3\notin T_t,\quad c_4\in T_t.
\]

Both c₃,c₄ are nonanchors. Column c₄ is not dummy, since c₃<c₄.

**Vertical t.** For V_i^+, r₂ is R_i^+(p) and c₄=C_{i−1}^+(q) with
π(p)>q. A nondummy c₃ outside T_t with a one on r₂ would be in C_i^+
(or, at a leaf, C_{h−1}^−). Its order before c₄ contradicts the threshold
inequalities. Explicitly a C_i^+ node u requires p≤u and π(u)<q;
a terminal minus-parent node u requires π(p)<u<q. For V_i^−, r₂ is
R_{i−1}^−(p) and c₄=C_{i−1}^−(q) with p≥q. A nondummy c₃ outside T_t
could only be C_{i−2}^−(u) when i≥2, requiring π(p)<u<π(q), also impossible.
At i=1 that preceding class is absent.
Thus c₃ must be dummy.

When b=1, the nonanchor c₂<c₃ rules that out. When b=2, a later
nondummy r₃ with a one on c₄ is impossible by the same threshold and
row-order inequalities: in the plus case its row class is R_{i−1}^+
or R_i^+, and in the minus case R_{i−1}^− or R_i^−. Hence r₃ is dummy.
Its one at anchor c₂ would require a W group-1 column. Every W anchor
precedes the V column c₁, contradicting c₁<c₂.

**Positive horizontal t=W_{i,d}^+.** Column c₄ is in C_{i,d}^+, as is
the class of r₂. Write their nodes p,q. The zero requires p>q. A c₃
in the same child class is excluded by monotonicity and c₃<c₄. A plus
parent c₃=C_{i−1}^+(u) requires π(p)≤u≤π(q). Equal floors would make
p,q unequal siblings, contradicting their common parity d. At the
terminal level a minus-parent c₃ instead requires π(p)<u<π(q), impossible.
The dummy is in T_t and cannot be c₃. No copy occurs in this mode.

**Negative horizontal t=W_{i,d}^−.** The row r₂ is R_{i,d}^−(p), or
L_R(p) if i=h. If c₄ is an added odd child, then i<h,d=0. Its node q
satisfies p≥q. Column c₃ outside T_t with a one on r₂ can only be an
own-level node u>p; c₃<c₄ would give u<q, impossible.

Thus c₄=C_{i−1}^−(b), with π(p)≥b. For i<h, a c₃ outside T_t with a
one on r₂ must be C_i^−(q), where q>p and π(q)≤b. These inequalities
force π(q)=b=π(p), p even and q=p+1 odd. The row role then has d=0,
but this odd c₃ was added to T_t, a contradiction. This is the precise
use of the new odd-child ones.

Therefore i=h. Here c₃ can only be a leaf column q with p≤q, or a
plus-parent column C_{h−1}^+(a) with π(p)≤a. In the first case its order
before c₄ gives π(q)≤b; in the second it gives a≤b. Together with
π(p)≥b, both cases imply b=π(p).

Every copy consequently sends its fixed zero H(2,4) to

\[
 T_h=\{(L_R(p),c):c\in C_{h-1}^-(\lfloor p/2\rfloor)\}.
\]

There are exactly 2m cells in T_h, because each terminal parent block
has two positions. Fixing this cell leaves at most n⁵ choices for the
other two rows and three columns. Thus N_H(A_h)≤2mn⁵.

## 5. Arbitrary repairs still cost at least m²

Let a binary B differ from A_h on M<m² cells. Sample a uniform leaf z
and its ancestor at each level. Independently choose one uniform position
from each signed row and column block on this path, identifying the two
sign selections at the leaf. Choose independent uniform representatives
of each anchor block and each dummy block.

A variable or dummy position has marginal probability 1/m. A column
anchor position has probability 1/m, and a row anchor position 1/(2m).
Selections with an anchor or dummy endpoint are independent across axes;
root selections are also independent. Therefore any protected cell
(anchor endpoint, dummy endpoint, or root-to-root) is selected with
probability at most 1/m². The union bound supplies a selection with no
edited protected cell. This probability assertion is not made for
arbitrary variable-variable cells or for shared leaf diagonals.

Suppose B is H-free. The unchanged designated anchors extend every
ordered P body on the selected role representatives to H. Therefore
all those bodies must avoid P. The root-plus diagonal is one and the
root-minus diagonal zero. If the selected parent diagonals have these
values, the vertical bodies are

\[
 \begin{pmatrix}1&b_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}1&0\\1&b_-\end{pmatrix}.
\]

Their P-freeness forces b_+=1,b_−=0. The horizontal modes matching the
child parity next have bodies

\[
 \begin{pmatrix}1&c_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}c_-&0\\1&1\end{pmatrix},
\]

forcing child diagonal values c_+=1,c_−=0. The recursive axis orders
put all these role bodies in increasing order. Induction reaches the
common leaf diagonal, which cannot simultaneously be one and zero.
Thus B is not H-free. All M edits were arbitrary, including anchor edits
and both directions of binary change. This proves the m² lower bound.

## 6. Quantifiers and comparison

With ε_h=(14h+2)^−2, the density-to-power ratio is at most

\[
 \frac{N_H(A_h)}{n_h^7\epsilon_h^C}
 \le 2(14h+2)^{2C-2}2^{-h}\longrightarrow0.
\]

Given c,C,ε₀>0, choose h with ε_h<ε₀ and this ratio<c. Replace every
physical row and column by q identical consecutive twins, for any positive
integer q. The same
sampler gives repair lower bound q²m². Since H has distinct rows and
columns, a copy cannot reuse a projected row or column, so its count
scales exactly by q⁷. Both normalized bounds are unchanged. Choosing q
arbitrarily large gives the required host sizes, including a prescribed
threshold depending on ε_h.

The improvement is rectangular pattern size: 3×4 rather than the known
4×4. Copy densities have different normalizations n⁷ and n⁸, so the
raw count is not a multiplicative improvement to the old fixed-H bound.
The earlier 4×4 exact-distance and optimized-count results remain separate.
Neither the exact repair equality nor its existing Lean certificate has
been transferred to this host.

## 7. Reproduction and verification scope

`experiments/asymmetric_candidate.py` enumerates all ordered quotient
copies with exact twin multiplicities through h=6.
`verification/check_three_by_four.py` separately constructs the host and
uses weighted subsequence dynamic programming. It checks the same depths,
a fully expanded h=1 matrix, designated anchor signatures, and adverse
variants omitting each of the two anchor-row changes. The latter variants
have nonlocalized copies. See the archived exact report and separate
agent review. These finite computations support this written argument;
they do not supply its universal quantifiers or independent peer review.


## 8. Lean formalization

The main theorem is checked in Lean 4.34.1 with the pinned Mathlib dependency.

`no_polynomial_removal_bound` in the `OrderedRemoval.Rectangular`
namespace states the full quantifier order: for every c,C,ε₀>0, choose a fixed 0<ε<ε₀; for every host
threshold N, there is an n≥max(1,N) square binary matrix with at least εn²
edits in every H-free repair and fewer than c ε^C n⁷ copies.

The proof constructs the literal host and both orders, excludes every
unwanted anchor configuration, localizes the fixed zero, counts copies,
and proves the arbitrary-repair bound before normalizing. The uniform-blowup
lemmas preserve the normalized bounds. They prove the sufficient q⁷ copy
upper bound; the exact blowup-count equality in Section 6 is not needed
by the formal capstone. No exact all-depth enumeration or repair equality
is asserted for this host.

The formal sampler is an alternative to Section 5's independent sampler:
it retains the inherited three seeds and selects representatives from both
m-sized row subgroups of each 2m anchor block. Copy completion uses the
second representative. Its anchor-row marginal is 1/m, and every protected
cell still has probability at most 1/m². This distinction changes no bound.

The [audit](verification/reference/rectangular-formal-audit.json) binds all
project source files. It checks transitive axiom dependencies and replays
each project module into its imported Lean environment. This does not
freshly replay all Mathlib or constitute independent mathematical peer review.
Only `propext`, `Quot.sound`, and `Classical.choice` occur as axioms.
The separate-agent semantic review is archived alongside the finite checks.
