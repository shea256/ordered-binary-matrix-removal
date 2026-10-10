# A Five-by-Five Obstruction to Polynomial Ordered Binary Matrix Removal

**Ryan Shea**

October 10, 2026

**Candidate research manuscript.** Complete written argument and exact finite
checks; independent mathematical review, end-to-end formalization, and
conclusive novelty assessment remain pending. Developed with Codex assistance.

## Abstract

We propose an explicit fixed **5×5 binary pattern** with no polynomial
ordered induced removal bound. Its **3×3 anchor** is supplemented by two
rows and two columns. The construction refines OpenAI's 66×66 obstruction
and our earlier 15×15 candidate. The new ingredients are exclusion of a
three-row crown from the nonanchor host and a mode order in which properly
containing role supports come later. These give a rigidity proof for the
3×3 anchor without the earlier density-prefix argument.

For every integer \(h\ge1\), the host has order \((20h+2)2^h\), normalized
repair distance at least \((20h+2)^{-2}\), and exactly \(2\cdot2^{8h}\)
ordered copies. Copies match both zeros and ones and preserve independent
row and column orders; repairs allow arbitrary binary entry changes in
either direction. The fixed pattern is independent of the host depth.
Finite checks support the argument but do not establish its universal claim.

## Source and contribution

The tree host, four-step propagation mechanism, sampling argument against
arbitrary repairs, and diagonal-leaf localization adapt OpenAI,
*Polynomial removal fails for ordered binary matrices*, September 25, 2026,
at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. The qualitative failure
of polynomial removal and the exact \(4^{-h}\) density-decay mechanism
are inherited. The proposed refinement is the much smaller fixed pattern.

See [BASELINE.md](BASELINE.md) and [ATTRIBUTION.md](ATTRIBUTION.md) for the
source and theorem comparisons. The earlier 15×15 candidate remains in
[the historical proof draft](proofs/compressed-pattern.md) and repository
history. The released formalization of the original 66×66 construction
has not been rebuilt here and does not certify either new pattern.

## Statement

There is a fixed binary matrix H of order 5 such that for every integer
h >= 1, with m=2^h, d=20h+2 and n=dm, the explicit binary host A_h satisfies

\[
 \operatorname{dist}_H(A_h)\ge d^{-2},\qquad
 N_H(A_h)=2m^8,\qquad
 \frac{N_H(A_h)}{n^{10}}=2d^{-10}4^{-h}.
\]

Here copies preserve independently increasing row and column orders and
match both zero and one entries. Distance is the minimum number of arbitrary
binary entry changes, in either direction and anywhere in the host, divided
by n^2. In particular, for every c,C>0 there are n, 0<epsilon<1 and A with
\(\operatorname{dist}_H(A)\ge\epsilon\) and
\(N_H(A)<c\epsilon^C n^{10}\). The same fixed H works for every c,C.

## 1. Pattern and changed mode order

Put s=3 and let S=J_3-I_3, where J_3 is the all-one matrix. The pattern is

\[
 H=\begin{pmatrix}S&e_1&e_2\\e_1^T&1&0\\e_2^T&1&1\end{pmatrix}
  =\begin{pmatrix}
 0&1&1&1&0\\
 1&0&1&0&1\\
 1&1&0&0&0\\
 1&0&0&1&0\\
 0&1&0&1&1
 \end{pmatrix},\qquad
 P=\begin{pmatrix}1&0\\1&1\end{pmatrix}.
\]

Every S row and column has two ones, so none equals a unit vector or zero.
All rows and columns of S are distinct. Each mode's anchor contains three
size-m groups on each axis, with between-group matrix S.

**Essential change:** order modes by increasing level i and, within a level,

\[
 W_{i,0}^+,\ W_{i,1}^+,\ W_{i,0}^-,\ W_{i,1}^-,\ V_i^+,\ V_i^-.
\]

Use this same mode order on both axes. All anchors precede all nonanchors.
The V-before-W order in the 15-by-15 construction fails to give rigidity
for S_3: an explicit unintended copy occurs at h=2 in the verification
report. The W-before-V order is part of the new construction.

## 2. Host definition

At depth i of a full binary tree label nodes p=0,...,2^i-1. At every
depth i<h introduce row blocks R_i^-(p), R_i^+(p) and column blocks
C_i^-(p), C_i^+(p), each of size m/2^i. At depth h there is a single
row and column position per node, given both sign names:

\[
 R_h^-(p)=R_h^+(p),\qquad C_h^-(p)=C_h^+(p).
\]

All other blocks on an axis are disjoint. R_i^sigma and C_i^sigma
denote unions over nodes at a depth; each has size m. For i>=1 the
subscript (i,d) restricts to nodes with p congruent to d modulo 2.
There are also dummy blocks R_*, C_* of size m.

Order variable rows recursively: a node's minus block, its child-0
subtree, its child-1 subtree, then its plus block. At a leaf insert
the one block once. Order columns similarly, with plus before and
minus after the subtrees. Put the dummy rows after variable rows,
and dummy columns before variable columns.

For every i=1,...,h introduce these six modes:

| Mode | Row role 1 | Row role 2 | Column role 1 | Column role 2 |
| --- | --- | --- | --- | --- |
| V_i^+ | R_i^+ | R_{i-1}^+ | C_* | C_{i-1}^+ |
| V_i^- | R_{i-1}^- | R_i^- | C_* | C_{i-1}^- |
| W_{i,0}^+ and W_{i,1}^+ | R_{i,d}^+ | R_* | C_{i-1}^+ | C_{i,d}^+ |
| W_{i,0}^- and W_{i,1}^- | R_{i,d}^- | R_* | C_{i,d}^- | C_{i-1}^- |

Place all mode anchor blocks before all nonanchor positions on each
axis. Within an anchor block put s consecutive groups of size m.
Use increasing i, then W_0^+,W_1^+,W_0^-,W_1^-,V^+,V^- to order modes.
Each mode's two roles on a given axis are disjoint, even at leaves.

Define every host entry as follows:

* Between anchor groups in the same mode put the corresponding S entry;
  between different modes put zero.
* A non-anchor position in role j of mode t has the unit-vector signature
  e_j against that mode's anchor groups. A position in neither role has
  the zero signature. Apply this independently on both axes.
* A non-anchor-to-non-anchor entry touching a dummy position is one.
* Variable-to-variable entries are zero except for these rules:

| Row | Column | Range | Entry |
| --- | --- | --- | --- |
| R_i^+(p) | C_i^+(q) | 0<=i<=h | 1[p<=q] |
| R_i^-(p) | C_i^-(q) | 0<=i<h | 1[p<q] |
| R_i^+(p) | C_{i-1}^+(q) | 1<=i<=h | 1[floor(p/2)<=q] |
| R_i^-(p) | C_{i-1}^-(q) | 1<=i<=h | 1[floor(p/2)<q] |

The common leaves satisfy the first rule. The second excludes them;
in the final two rules the column signs are still distinct. Hence
these assignments are consistent. There are 6hs anchor classes,
2h+1 variable classes and one dummy class of size m on each axis,
giving n=(6hs+2h+2)m=(20h+2)m. No labels are part of the binary alphabet:
the block names serve only to describe actual positions and entries.

The recursive orders imply, writing pi(p)=floor(p/2),

\[
\begin{aligned}
 R_i^+(p)<R_{i-1}^+(a)&\iff\pi(p)\le a,&
 R_{i-1}^-(a)<R_i^-(p)&\iff a\le\pi(p),\\
 C_{i-1}^+(b)<C_i^+(q)&\iff b\le\pi(q),&
 C_i^-(q)<C_{i-1}^-(b)&\iff\pi(q)\le b.
\end{aligned}
\]

This follows because the subtrees at a fixed depth occur as consecutive
intervals in increasing node order, and each child's block lies between
its own parent's two signs. These comparisons include the shared leaves.

## 3. Three structural properties

A nonanchor class means one level/sign class (identifying the two leaf
signs as one class L) or the dummy class. A half-class restricts a non-root
variable class to one parity of its node label. No auxiliary labels are
part of the binary alphabet.

**Lemma 1 (comparability and crown exclusion).** On nonanchor rows, any
two columns from the same nonanchor class have comparable one-sets.
The analogous statement holds for rows. Moreover, no nonanchor rows and
columns induce S=J_3-I_3, even if their orders are disregarded.

**Proof.** Within a column class, each variable row's entries form a suffix
in increasing node label; dummy rows are constant one. Within a row class,
each variable column's entries form a prefix, since all the inequalities
in Section 2 decrease as the row node increases. Dummy classes are constant.
Thus either same-class row or column pairs cannot contain both traces 10
and 01.

An S copy has those two traces on every column pair, so its three column
classes must be distinct. It cannot include a dummy column, whose entries
are constantly one. Classify variable columns by level/sign, with the
shared leaves represented by L. Put edges between consecutive levels of
each sign, and a terminal triangle on L,(h-1,+),(h-1,-). A non-leaf variable
row can be one only in its own and the preceding class; a leaf row can
be one only in those three terminal classes.

Every pair of S columns has a row with ones on that pair and zero on the
third. That row cannot be dummy. Hence every pair of the three column
classes must be an edge, forcing the unique terminal triangle. Select
columns L(q), C_{h-1}^+(b_+), C_{h-1}^-(b_-). A leaf row p gives the trace

\[
 (\mathbf1[p\le q],\ \mathbf1[\lfloor p/2\rfloor\le b_+],\
   \mathbf1[\lfloor p/2\rfloor<b_-]).
\]

These traces form a chain as p increases. They cannot supply both 110 and
101. Non-leaf rows have zero in the L coordinate, and dummy rows give 111.
An S copy requires both missing traces, a contradiction. This includes h=1,
when the triangle consists of the leaf class and the two root classes. QED.

**Lemma 2 (ordered laminar role supports).** Fix either axis. Every role
support is a whole nonanchor class or one of its two parity halves. Thus
any two role supports are disjoint or nested. If one is a proper subset
of another, the containing support belongs to a strictly later mode in
the order of Section 1. The two supports of one mode are disjoint.

**Proof.** The mode table gives the following exhaustive possibilities:

| Axis | Whole variable-class supports | Half-class supports |
| --- | --- | --- |
| Row | V_i on its depth-i child class; V_{i+1} on its depth-i parent class | W_{i,d} on its depth-i child class |
| Column | V_{i+1} and W_{i+1,d} on their depth-i parent class | W_{i,d} on its depth-i child class |

At depth h the sign classes coincide; full and half leaf supports are
still the same whole class and its parity halves. Omit modes with indices
outside 1,...,h. Dummy supports are the whole dummy class and are disjoint
from every variable support. At the root no half-class support occurs.

The only possible strict inclusion is a parity half of one variable class
in the whole of that class. On the row axis, its W_i mode precedes both
V_i (by the within-level order) and V_{i+1} (by level). On the column axis,
its W_i mode precedes V_{i+1} and W_{i+1,d} by level. Equality of supports
across modes, including leaf sign identifications, is harmless. The two
roles of a single mode lie in different classes: parent/child, variable/
dummy, or dummy/variable. Therefore they are disjoint. QED.

An anchor row's support on nonanchor columns is one of these column-role
supports if its group is 1 or 2, and empty if its group is 3. The analogous
statement holds for anchor columns and row-role supports.

**Lemma 3 (rigidity).** Every ordered S copy in A_h uses exactly one
representative of each anchor group of one mode on both axes.

**Proof.** Let a,b be the numbers of selected anchor rows and columns.
They form prefixes of the selected axes. Twin anchor positions in one
group cannot both occur, because S has distinct rows and columns.

If a,b >= 2, the one-entries (1,2) and (2,1) force the mode identities
\(t(r_1)=t(c_2)\) and \(t(r_2)=t(c_1)\). Anchor order on the two axes gives
\(t(r_1)\le t(r_2)\) and \(t(c_1)\le t(c_2)\). Therefore all four modes
are equal to one t. The third column must have ones against both first
anchor rows. It cannot be nonanchor, whose signature has at most one one
among t's distinct groups; if anchor, it must also belong to t. The same
reasoning forces the third row into t. All three distinct groups occur.

If a >= 2 and b <= 1, columns 2 and 3 are nonanchor. The first two anchor
rows restrict to 11 and 01 on these columns. Their nonanchor supports
intersect, so by Lemma 2 they are nested. The earlier support properly
contains the later one, contradicting the strict-containment mode order.
The case a <= 1 and b >= 2 is identical after transposition: columns 1
and 2 have supports 11 and 01 on nonanchor rows 2 and 3.

It remains that a,b <= 1. If a=1, the first anchor row has ones in columns
2 and 3, putting those two nonanchor columns in a single role support and
therefore one class. Rows 2 and 3 are nonanchor and require the traces 01
and 10 on those columns, contradicting Lemma 1's comparability. If a=0
and b=1, transpose this argument using the first anchor column and the
last two rows. Finally, a=b=0 contradicts Lemma 1's crown exclusion.
These cases exhaust a,b in {0,1,2,3}, proving rigidity. QED.

## 4. Roles of the remaining body positions

In any H copy, Lemma 3 forces its first three rows and columns into one
mode's three anchor groups. The last two rows and columns have signatures
e_1 and e_2 against those anchors. An anchor from another mode has zero
signature; an anchor from the same mode has an S row/column of weight two.
Neither can equal a unit vector. Among nonanchors exactly the prescribed
role-j support gives e_j. Thus every H body is in one mode's designated
roles, on both axes. No minimum-density or four-incidence bound is needed.

## 5. Localization and exact number of copies

Consider an H copy and its mode, using the role corollary. Its body
must be P. Write p for its child-level row node, q for its child-level
column node, a for its parent-level row node and b for its parent-level
column node, as applicable.

* In V_i^+, row order gives pi(p)<=a. The bottom-right one gives a<=b.
  The top-right entry is consequently one, contradicting P.
* In V_i^-, row order gives pi(p)>=a. The top-right zero gives a>=b.
  The bottom-right entry is consequently zero, contradicting P.
* In W_{i,d}^+, column order gives b<=pi(q), and the top-left one gives
  pi(p)<=b. Since p,q have the same parity, p<=q. The top-right entry
  is one, contradicting P. This applies at the leaves too.
* In W_{i,d}^-, column order gives pi(q)<=b, and the top-right zero
  gives pi(p)>=b. Common parity implies p>=q. For i<h the top-left
  entry 1[p<q] is zero. For i=h it is instead 1[p<=q], and can be one
  only if p=q. The parent column then has b=pi(p).

Conversely, in W_{h,d}^- each leaf p of parity d, any dummy row, and
any parent-minus column in C_{h-1}^-(pi(p)) produce exactly P, in the
required order. Any representatives of that mode's three anchor
groups complete an H copy.

There are m leaf choices, m dummy row choices, two parent column
choices, and m^{6} anchor choices. Each embedding has a unique mode
and leaf, so

\[
 N_H(A_h)=m\cdot m\cdot2\cdot m^{6}=2m^{8}.
\]

Every copy sends the fixed pattern cell (4,4) into the m-cell leaf
diagonal L_h. This also gives the coarser bound N_H(A_h)<=m n^{8},
which already suffices for nonpolynomial removal.

## 6. Distance against arbitrary binary repairs

Let B differ from A_h on a set E of M<m^2 cells. Partition each axis
into the size-m anchor groups, dummy group, the two sign classes at
each depth below h, and the single shared leaf class.

Choose a uniform leaf z in {0,...,m-1} and its ancestor a_i=floor(z/2^{h-i}).
Choose one uniform position x_i^sigma,y_i^sigma from the row and column
blocks with that ancestor at each level and sign. At the leaf use one
common position for both signs on each axis. Conditional on z, make
all other choices independently. Also choose independently one uniform
representative of every anchor and dummy group on each axis.

Each variable position has marginal sampling probability
2^{-i}/(m/2^i)=1/m. Anchor and dummy selections are independent of
every opposite-axis selection. The root selections, whose node is
always 0, are independent uniform choices too. Therefore every cell
with an anchor or dummy endpoint, and every root-to-root cell, is
selected with probability exactly 1/m^2. Within each class there is
only one selection. A union bound over edited cells of these types
gives probability at most M/m^2<1 that any such selected cell was
edited. Fix a selection with none edited.

This statement does NOT apply to arbitrary variable-to-variable cells:
for example a fixed diagonal leaf cell is selected with probability
1/m, because the two axes share z. No such independence is used below.

Suppose B were H-free. Its selected anchors still form S, and their
signatures against selected body positions and all dummy incidences
are unchanged. Thus whenever a mode's selected body is P, it extends
to H in B. Its absence forces the following implications.

The unchanged root-plus diagonal is one and root-minus diagonal is
zero. Suppose at depth i-1 these values are still one and zero.
The V_i^+ and V_i^- bodies respectively have form

\[
 \begin{pmatrix}1&b_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}1&0\\1&b_-\end{pmatrix}.
\]

Avoiding P forces b_+=1 and b_-=0. These are the entries from selected
depth-i rows to selected depth-(i-1) columns. Next use the W modes
with d=a_i mod 2. Their bodies respectively have form

\[
 \begin{pmatrix}1&c_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}c_-&0\\1&1\end{pmatrix}.
\]

Avoiding P forces c_+=1 and c_-=0 at the depth-i diagonals. All four
bodies are in increasing row/column order because their selected
nodes are parent and child, and dummy positions have the stipulated
extreme orders. Induction carries opposite values to depth h. At
that depth the plus and minus diagonals are the same cell, a
contradiction. Hence B is not H-free.

Every H-free repair requires at least m^2 changes. Dividing by
n^2=d^2m^2 gives dist_H(A_h)>=d^{-2}. No restrictions were imposed on
unprotected entries or on the directions of the changes.

## 7. Final asymptotic implication and sampling scope

For epsilon_h=d^{-2} the exact density gives, for every fixed C>0,

\[
 \frac{N_H(A_h)}{\epsilon_h^C n^{10}}
   =2(20h+2)^{2C-10}4^{-h}\longrightarrow0.
\]

An exponential in h beats every fixed power of h; choosing h sufficiently
large for any c>0 proves the theorem. Also 0<epsilon_h<1 for h>=1.
The constants are uniform over the unbounded sequence, not just finitely
many tested hosts.

For canonical sampling of q uniform rows and, independently, q uniform
columns, rejection on observing H implies sampling one of L_h's m cells.
Thus Pr(reject)<=m(q/n)^2=epsilon_h 2^{-h}q^2. Rejection probability
at least rho>0 requires q>=sqrt(rho)(20h+2)2^{h/2}. Equivalently
q>=sqrt(rho) epsilon_h^{-1/2} 2^{(epsilon_h^{-1/2}-2)/40}
along this sequence. There are q^2 observed entries. This does not claim
a lower bound for arbitrary adaptive or two-sided testers.

Changing every original leaf-diagonal one to zero destroys the old copies,
but creates a new W_{h,d}^+ copy at each leaf: its parent-plus entry
is one, the changed leaf entry is zero, and its dummy bottom row is
11. This makes explicit why the m-cell hitting set is not an m-cell
repair, and why both directions of binary edits must be allowed.

## Verification boundary and comparison

The prior 15-by-15 candidate used s=13 and d=80h+2; the pinned original
66-by-66 manuscript uses s=64 and d=386h+2. The new candidate has s=3,
k=5 and d=20h+2. The qualitative failure and the exact 4^{-h} decay
mechanism are inherited. The sharper result is the fixed forbidden
pattern size, with all model assumptions and asymptotic quantifiers intact.

The all-depth proof above, rather than extrapolation from finite examples,
is the proposed justification. [check_refinement.py](verification/check_refinement.py)
checks crown exclusion, the role table and its laminar order, every ordered
S_3 embedding through depth 6, every ordered H_5 embedding through depth 2,
and weighted body counts through depth 6. Existing path checks exercise
all free path assignments through depth 4. These are same-agent checks;
no independent reviewer or Lean kernel has verified the new theorem.

All 16 binary 2-by-2 matrices occur among nonanchors already at h=2, as
certified by the checker. Thus a 2-by-2 anchor cannot satisfy the same
pure-anchor rigidity requirement in this nonanchor host. This is a
limitation of this approach, not a proof that no 4-by-4 obstruction exists.
