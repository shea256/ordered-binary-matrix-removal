# A candidate 4-by-4 ordered binary removal obstruction

Date: 2026-10-10. **Candidate with a complete written proof draft.**
Independent mathematical review, end-to-end formal verification, and conclusive novelty
assessment remain pending. This further refines the earlier 5-by-5 candidate.

The tree host and arbitrary-repair propagation adapt OpenAI's September 25,
2026 manuscript at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
The ordered role-support argument comes from the preceding candidate.
The new step permits noncanonical copies of a two-by-two anchor and instead
localizes the entire four-by-four pattern to a small set of **zero** cells.
Pure anchor rigidity is neither asserted nor needed.

## Statement and explicit pattern

Let

\[
 S=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 H=\begin{pmatrix}
 0&1&1&0\\
 1&0&0&1\\
 1&0&1&0\\
 0&1&1&1
 \end{pmatrix}
 =\begin{pmatrix}S&e_1&e_2\\e_1^T&1&0\\e_2^T&1&1\end{pmatrix},
 \qquad P=\begin{pmatrix}1&0\\1&1\end{pmatrix}.
\]

H is the complete forbidden pattern; S is its two-by-two anchor component.
H has four distinct rows and four distinct columns, although S's rows and
columns are themselves unit vectors. That distinction matters below.

For every integer \(h\ge 1\), put \(m=2^h\), \(d=14h+2\), and \(n=dm\).
The explicit binary host \(A_h\) below satisfies

\[
 \operatorname{dist}_H(A_h)\ge d^{-2},\qquad
 \frac{N_H(A_h)}{n^8}\le\frac{33}{4}d^{-8}4^{-h}.
\]

For \(h=1\) its exact copy count is 128. For \(h\ge 2\) it is

\[
 N_H(A_h)=\frac{33}{4}m^6-\frac{29}{2}m^5.
\]

Copies preserve independently increasing row and column orders and match
both binary values. Distance permits arbitrary changes in both directions,
including anchor cells, and is normalized by \(n^2\). Consequently for every
\(c,C>0\) there are n, \(0<\epsilon<1\) and a binary A with distance at least \(\epsilon\)
from H-freeness but fewer than \(c\epsilon^C n^8\) ordered H copies. The same
fixed four-by-four H works for all c,C.

## 1. Mode order and anchor size

Use \(s=2\) anchor groups per mode on each axis. Order modes on both axes by
increasing depth and then

\[
 W_{i,0}^+,\ W_{i,1}^+,\ W_{i,0}^-,\ W_{i,1}^-,\ V_i^+,\ V_i^-.
\]

All anchor positions precede all nonanchor positions. The W-before-V order
preserves the containing-supports-come-later property. The order of the two
minus parity modes is also used in the new localization argument.

## 2. Host definition

At depth i of a full binary tree label nodes \(p=0,\ldots,2^i-1\). At every
depth \(i<h\) introduce row blocks \(R_i^-(p)\), \(R_i^+(p)\) and column blocks
\(C_i^-(p)\), \(C_i^+(p)\), each of size \(m/2^i\). At depth h there is a single
row and column position per node, given both sign names:

\[
 R_h^-(p)=R_h^+(p),\qquad C_h^-(p)=C_h^+(p).
\]

All other blocks on an axis are disjoint. \(R_i^\sigma\) and \(C_i^\sigma\)
denote unions over nodes at a depth; each has size m. For \(i\ge 1\) the
subscript (i,d) restricts to nodes with p congruent to d modulo 2.
There are also dummy blocks \(R_*\), \(C_*\) of size m.

Order variable rows recursively: a node's minus block, its child-0
subtree, its child-1 subtree, then its plus block. At a leaf insert
the one block once. Order columns similarly, with plus before and
minus after the subtrees. Put the dummy rows after variable rows,
and dummy columns before variable columns.

For every \(i=1,\ldots,h\) introduce these six modes:

| Mode | Row role 1 | Row role 2 | Column role 1 | Column role 2 |
| --- | --- | --- | --- | --- |
| \(V_i^+\) | \(R_i^+\) | \(R_{i-1}^+\) | \(C_*\) | \(C_{i-1}^+\) |
| \(V_i^-\) | \(R_{i-1}^-\) | \(R_i^-\) | \(C_*\) | \(C_{i-1}^-\) |
| \(W_{i,0}^+\) and \(W_{i,1}^+\) | \(R_{i,d}^+\) | \(R_*\) | \(C_{i-1}^+\) | \(C_{i,d}^+\) |
| \(W_{i,0}^-\) and \(W_{i,1}^-\) | \(R_{i,d}^-\) | \(R_*\) | \(C_{i,d}^-\) | \(C_{i-1}^-\) |

Place all mode anchor blocks before all nonanchor positions on each
axis. Within an anchor block put s consecutive groups of size m.
Use increasing i, then \(W_0^+,W_1^+,W_0^-,W_1^-,V^+,V^-\) to order modes.
Each mode's two roles on a given axis are disjoint, even at leaves.

Define every host entry as follows:

* Between anchor groups in the same mode put the corresponding S entry;
  between different modes put zero.
* A non-anchor position in role j of mode t has the unit-vector signature
  \(e_j\) against that mode's anchor groups. A position in neither role has
  the zero signature. Apply this independently on both axes.
* A non-anchor-to-non-anchor entry touching a dummy position is one.
* Variable-to-variable entries are zero except for these rules:

| Row | Column | Range | Entry |
| --- | --- | --- | --- |
| \(R_i^+(p)\) | \(C_i^+(q)\) | \(0\le i\le h\) | \(\mathbf1[p\le q]\) |
| \(R_i^-(p)\) | \(C_i^-(q)\) | \(0\le i<h\) | \(\mathbf1[p<q]\) |
| \(R_i^+(p)\) | \(C_{i-1}^+(q)\) | \(1\le i\le h\) | \(\mathbf1[\lfloor p/2\rfloor\le q]\) |
| \(R_i^-(p)\) | \(C_{i-1}^-(q)\) | \(1\le i\le h\) | \(\mathbf1[\lfloor p/2\rfloor<q]\) |

The common leaves satisfy the first rule. The second excludes them;
in the final two rules the column signs are still distinct. Hence
these assignments are consistent. There are 6hs anchor classes,
2h+1 variable classes and one dummy class of size m on each axis,
giving \(n=(6hs+2h+2)m=(14h+2)m\). No labels are part of the binary alphabet:
the block names serve only to describe actual positions and entries.

The recursive orders imply, writing \(\pi(p)=\lfloor p/2\rfloor\),

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

## 3. Inherited host properties

A nonanchor class means one level/sign class (identifying the two leaf
signs as one class L) or the dummy class. A half-class restricts a non-root
variable class to one parity of its node label. No auxiliary labels are
part of the binary alphabet.

**Lemma 1 (comparability and crown exclusion).** On nonanchor rows, any
two columns from the same nonanchor class have comparable one-sets.
The analogous statement holds for rows. Moreover, no nonanchor rows and
columns induce the three-by-three crown \(Q=J_3-I_3\), even if their orders are disregarded.

**Proof.** Within a column class, each variable row's entries form a suffix
in increasing node label; dummy rows are constant one. Within a row class,
each variable column's entries form a prefix, since all the inequalities
in Section 2 decrease as the row node increases. Dummy classes are constant.
Thus either same-class row or column pairs cannot contain both traces 10
and 01.

A Q copy has those two traces on every column pair, so its three column
classes must be distinct. It cannot include a dummy column, whose entries
are constantly one. Classify variable columns by level/sign, with the
shared leaves represented by L. Put edges between consecutive levels of
each sign, and a terminal triangle on L,(h-1,+),(h-1,-). A non-leaf variable
row can be one only in its own and the preceding class; a leaf row can
be one only in those three terminal classes.

Every pair of Q columns has a row with ones on that pair and zero on the
third. That row cannot be dummy. Hence every pair of the three column
classes must be an edge, forcing the unique terminal triangle. Select
columns L(q), \(C_{h-1}^+(b_+)\), \(C_{h-1}^-(b_-)\). A leaf row p gives the trace

\[
 (\mathbf1[p\le q],\ \mathbf1[\lfloor p/2\rfloor\le b_+],\
   \mathbf1[\lfloor p/2\rfloor<b_-]).
\]

These traces form a chain as p increases. They cannot supply both 110 and
101. Non-leaf rows have zero in the L coordinate, and dummy rows give 111.
A Q copy requires both missing traces, a contradiction. This includes \(h=1\),
when the triangle consists of the leaf class and the two root classes. QED.

**Lemma 2 (ordered laminar role supports).** Fix either axis. Every role
support is a whole nonanchor class or one of its two parity halves. Thus
any two role supports are disjoint or nested. If one is a proper subset
of another, the containing support belongs to a strictly later mode in
the order of Section 1. The two supports of one mode are disjoint.

**Proof.** The mode table gives the following exhaustive possibilities:

| Axis | Whole variable-class supports | Half-class supports |
| --- | --- | --- |
| Row | \(V_i\) on its depth-i child class; \(V_{i+1}\) on its depth-i parent class | \(W_{i,d}\) on its depth-i child class |
| Column | \(V_{i+1}\) and \(W_{i+1,d}\) on their depth-i parent class | \(W_{i,d}\) on its depth-i child class |

At depth h the sign classes coincide; full and half leaf supports are
still the same whole class and its parity halves. Omit modes with indices
outside 1,...,h. Dummy supports are the whole dummy class and are disjoint
from every variable support. At the root no half-class support occurs.

The only possible strict inclusion is a parity half of one variable class
in the whole of that class. On the row axis, its \(W_i\) mode precedes both
\(V_i\) (by the within-level order) and \(V_{i+1}\) (by level). On the column axis,
its \(W_i\) mode precedes \(V_{i+1}\) and \(W_{i+1,d}\) by level. Equality of supports
across modes, including leaf sign identifications, is harmless. The two
roles of a single mode lie in different classes: parent/child, variable/
dummy, or dummy/variable. Therefore they are disjoint. QED.

An anchor row in group j has column-role support j on the nonanchor
columns. The analogous statement holds for anchor columns and row-role
supports. Here j belongs to {1,2}; there is no third anchor group.


We also use these strict column-order comparisons, obtained directly from
the recursive traversal. At any nonleaf level j, and with a child at level i,

\[
\begin{aligned}
 C_i^\sigma(q)<C_{i-1}^+(b)&\iff \lfloor q/2\rfloor<b,\\
 C_{i-1}^-(b)<C_i^\sigma(q)&\iff b<\lfloor q/2\rfloor,\\
 C_j^+(a)<C_j^-(b)&\iff a\le b,\\
 C_j^-(a)<C_j^+(b)&\iff a<b.
\end{aligned}
\]

The first two apply to either child sign, including the shared leaf. Distinct
blocks at one level occur in increasing node order. Positions in the same
block may differ, but their entries against any fixed opposite position agree.

## 4. Every H copy has one of two anchor configurations

**Lemma 3.** If a,b count the selected anchor rows and columns of an ordered
H copy, then \((a,b)=(2,2)\) or \((2,1)\).

**Proof.** Selected anchors form prefixes. Because H has distinct rows and
columns, no two selected positions come from the same twin block.

If \(a,b\ge 2\), the crossed one-entries (1,2),(2,1) in S and the aligned mode orders
force the first two rows and columns into the same mode t: their mode labels
satisfy \(t(r_1)=t(c_2)\ge t(c_1)=t(r_2)\ge t(r_1)\). Each axis uses that
mode's two groups once, in group order. Any further selected anchor would
be in a later mode and have signature 00 against those opposite anchors,
whereas the remaining H rows and columns require 10 or 01. Hence \(a=b=2\).

Suppose \(a\le 1\). If \(b=0\), rows 2,3,4 on columns 1,3,4 are all nonanchor and form
\(\bigl(\begin{smallmatrix}1&0&1\\1&1&0\\0&1&1\end{smallmatrix}\bigr)\),
a row permutation of Q, forbidden by Lemma 1. If \(b=1\) or 2, the first anchor
column puts nonanchor rows 2,3 into one role support, hence one class. Those
rows have traces 01 and 10 on nonanchor columns 3,4, contradicting same-class
comparability. If \(b\ge 3\), the first and third anchor columns have signatures
11 and 01 on nonanchor rows 2,3. Their supports intersect, so the first
properly contains the third, contradicting Lemma 2's mode order.
Thus \(a\ge 2\).

If \(a\ge 3\) and \(b\le 1\), the first and third anchor rows have signatures 11 and 01
on nonanchor columns 2,3; Lemma 2 again gives an earlier proper container,
a contradiction. The only remaining case with \(b=0\) is \(a=2\). Then the second
anchor row puts nonanchor columns 1,4 in one class, while nonanchor rows
3,4 have traces 10 and 01 on them, contradicting comparability. These cases
leave precisely (2,2) and (2,1). QED.

## 5. Localization to a small set of zero cells

Let \(T_h\) consist of the cells with row the leaf p and column any position of
\(C_{h-1}^-(\lfloor p/2\rfloor)\). Each parent block has two positions, so
\(|T_h|=2m\). All these cells are zero by the strict minus transition rule.

**Lemma 4.** Every ordered H copy sends its fixed cell (3,4) into \(T_h\).
Its last row is dummy.

**Balanced case \(a=b=2\).** The remaining selected positions are nonanchor,
so their unit signatures force the two designated roles in mode t. The body
must be P. Write \(\pi(p)=\lfloor p/2\rfloor\). The original four-case
localization applies:

* \(V_i^+\): row order gives \(\pi(p)\le a\); the bottom-right one gives \(a\le b\), forcing
  the top-right entry to be one, contrary to P.
* \(V_i^-\): row order gives \(\pi(p)\ge a\); the top-right zero gives \(a\ge b\), forcing the
  bottom-right entry to be zero, contrary to P.
* \(W_{i,d}^+\): column order gives \(b\le \pi(q)\); the top-left one gives \(\pi(p)\le b\).
  Equal child parity forces \(p\le q\), contradicting the top-right zero.
* \(W_{i,d}^-\): column order gives \(\pi(q)\le b\) and the top-right zero gives
  \(\pi(p)\ge b\). Equal parity forces \(p\ge q\). Below the leaves the top-left entry
  \(\mathbf1[p<q]\) is zero. At the leaves it is \(\mathbf1[p\le q]\), forcing \(p=q\) and \(b=\pi(p)\).

Thus the mode is \(W_{h,d}^-\), row 3 is leaf p, column 4 is its parent-minus
block, and row 4 is dummy. There are exactly \(2m^6\) such H copies.

**Unbalanced case \(a=2,b=1\).** Let B be the mode of the second anchor row
and first anchor column; their intersection is one, so their groups are
opposite. If the row group were 1 and column group 2, then row 3 would have
row-role 2 and column 4 would have column-role 1 in B. In V modes the latter
is dummy; in W modes the former is dummy. Either way their entry would be
one, contradicting \(H(3,4)=0\). Consequently the second anchor row has group 2,
the first column has group 1, and

\[
 r_3\in\operatorname{rowrole}_1(B),\qquad
 c_4\in\operatorname{colrole}_2(B),\qquad A_h(r_3,c_4)=0.
\]

Let A be the mode of the first anchor row. Its role support contains both
\(c_2\) and \(c_3\), so these columns belong to one class K. The entries against
\(r_3\) are 0 and 1, so K is not dummy. The mode order gives \(A\le B\).
If \(A=B\), increasing anchor row order forces the first row into group 1.
We now treat each possible B; all selected columns satisfy \(c_3<c_4\).

* **\(B=V_i^+\).** Write \(r_3=R_i^+(p)\), \(c_4=C_{i-1}^+(b)\). The zero gives
  \(\pi(p)>b\). If K is the parent-plus class, the one at \(c_3\) gives \(\pi(p)\le a\)
  with \(a\le b\) by column order. If K is the own class, the one gives \(p\le q\)
  while \(c_3<c_4\) gives \(\pi(q)<b\). Both contradict \(\pi(p)>b\). At leaves the
  only additional class is parent-minus: its one gives \(\pi(p)<a\) and its
  preceding the parent-plus column gives \(a<b\), also a contradiction.
* **\(B=V_i^-\).** Write \(r_3=R_{i-1}^-(p)\), \(c_4=C_{i-1}^-(b)\). The zero gives
  \(p\ge b\). In the own class a one at \(c_3\) requires \(p<a\le b\), impossible. In the
  preceding minus class it requires \(\pi(p)<a\); column order requires
  \(a<\pi(b)\), again impossible. The preceding class is absent when \(i=1\).
* **\(B=W_{i,d}^+\).** Here \(r_3=R_{i,d}^+(p)\), \(c_4=C_{i,d}^+(q)\), and the zero
  gives \(p>q\). In the own class a one at \(c_3\) requires \(p\le q'\le q\). In the
  parent-plus class it requires \(\pi(p)\le a\le \pi(q)\); equal parity of p,q makes
  this impossible. At leaves a parent-minus \(c_3\) would require
  \(\pi(p)<a<\pi(q)\), also impossible.
* **\(B=W_{i,d}^-\).** Write \(r_3=R_{i,d}^-(p)\), \(c_4=C_{i-1}^-(b)\), so
  \(\pi(p)\ge b\). The parent-minus class cannot contain \(c_3\): a one there would
  give \(\pi(p)<a\le b\). In the own class, column order gives \(\pi(q)\le b\). If \(i<h\),
  the one requires \(p<q\). Because \(A\le B\), a role support for this own minus
  class can only be a child half-class of \(W_{i,e}^-\) with \(e\le d\). Whole-class
  supports occur at level i+1. Thus q has parity \(e\le d\), and
  \(\pi(p)\ge b\ge \pi(q)\) forces \(p\ge q\), a contradiction. Therefore \(i=h\). In the
  leaf class the one instead gives \(p\le q\), hence \(\pi(p)\le \pi(q)\le b\le \pi(p)\), so
  \(b=\pi(p)\). The only remaining possibility is a parent-plus \(c_3\). Its one
  gives \(\pi(p)\le a\), while its position before the parent-minus \(c_4\) gives
  \(a\le b\). Again \(b=\pi(p)\).

This proves localization in both cases. In the unbalanced case K is either
the leaf class or the parent-plus class. If K is the leaf class, \(c_2\) is a
leaf \(q_1<p\) because \(A_h(r_3,c_2)=0\). A nonanchor row one at \(c_2\) must be a leaf
of index at most \(q_1\), or dummy; a later row \(r_4\) cannot be such a leaf. If K
is parent-plus, \(c_2\) has parent node \(a<\pi(p)\). A nondummy row one at both \(c_2\)
and the parent-minus \(c_4\) must be a leaf. Its being one at \(c_2\) gives parent
node at most \(a<\pi(p)\), incompatible with its occurring after leaf p. Hence
\(r_4\) is dummy in both cases. QED.

In particular, the old leaf-diagonal hitting set is insufficient: unbalanced
copies can have no leaf column at all. The new fixed-cell localization is
to zeros, and remains useful because induced copies must match zeros too.

Localization alone already gives \(N_H(A_h)\le |T_h|n^6=2mn^6\), hence
\(N_H(A_h)/n^8\le 2d^{-2}2^{-h}\). Together with the distance bound below,
this suffices to refute every polynomial removal bound. The exact enumeration
in the next section strengthens the density estimate; the qualitative
obstruction does not depend on that enumeration.

## 6. Exact copy count, including the additional copies

The balanced count is \(2m^6\): m leaf choices, m dummy row choices, two
parent-column positions, and four independent size-m anchor choices.

For an unbalanced copy, fix its leaf \(p=2b+d\), with \(d\in\{0,1\}\). Its second
anchor row and first anchor column have mode \(B=W_{h,d}^-\) and groups 2,1.
Its last column has two positions in the parent-minus block b, and its last
row has m dummy choices. The three anchors contribute \(m^3\). Thus each pair
of actual positions \((c_2,c_3)\), together with the first anchor's mode and
group, contributes \(2m^4\) copies. The following list is exhaustive:

| Class K | First anchor mode/group | Allowed pair count |
| --- | --- | --- |
| Leaf | \(W_{h,e}^+\), group 2, \(e\ge d\) | b for each e |
| Leaf | \(W_{h,d}^-\), group 1 | b |
| Parent-plus | \(W_{h,e}^+\), group 1, either e | 4b for each e |
| Parent-plus | \(W_{h-1,e}^+\), group 2, \(e=b\bmod 2\), if \(h\ge 2\) | \(4\lfloor b/2\rfloor\) |

For the leaf class, \(c_3\) is the unique leaf 2b+e, while \(c_2\) can be any earlier
leaf of parity e below p, giving b choices. The minus mode order and the
required one imply \(e=d\) in the minus case. For parent-plus columns, \(c_3\)
has node b and \(c_2\) has node \(a<b\); each parent block has two actual positions,
so a node pair has multiplicity four. Half-class supports restrict a and b
to the same parity. The remaining possible full parent-plus support belongs
to \(V_h^+\), later than B, so cannot occur. Whole leaf supports do not exist
on the column axis within the available levels.

The parent-half family contributes zero at \(h=2\), when \(b\in\{0,1\}\);
its first positive contribution is at \(h=3\).

Conversely every pair listed gives the displayed H, in order: the first
anchor mode is earlier than B (or is B with group 1), all required role
signatures hold, the dummy row gives its three nonanchor ones, and the
leaf thresholds give entries 0,1,0 on columns 2,3,4. Thus no overcount or
missing family is hidden in the enumeration.

For \(p=2b+d\) the total pair count is
\((11-d)b+4\lfloor b/2\rfloor\). At \(h=1\), \(b=0\) for both leaves, so there are
no unbalanced copies. For \(h\ge 2\) let \(t=m/2\), which is even. Summing both parities,

\[
\begin{aligned}
 \sum_{b=0}^{t-1}\bigl(21b+8\lfloor b/2\rfloor\bigr)
 &=\frac{21t(t-1)}2+2t(t-2)\\
 &=\frac{t(25t-29)}2.
\end{aligned}
\]

Multiplication by \(2m^4\), then addition of \(2m^6\), gives
\(N_H=\frac{33}{4}m^6-\frac{29}{2}m^5\) for \(h\ge 2\). At \(h=1\), \(N_H=128\).
In every case \(N_H\le\frac{33}{4}m^6\).

## 7. Distance against arbitrary binary repairs

Let B differ from \(A_h\) on a set E of \(M<m^2\) cells. Partition each axis
into the size-m anchor groups, dummy group, the two sign classes at
each depth below h, and the single shared leaf class.

Choose a uniform leaf z in {0,...,m-1} and its ancestor \(a_i=\lfloor z/2^{h-i}\rfloor\).
Choose one uniform position \(x_i^\sigma,y_i^\sigma\) from the row and column
blocks with that ancestor at each level and sign. At the leaf use one
common position for both signs on each axis. Conditional on z, make
all other choices independently. Also choose independently one uniform
representative of every anchor and dummy group on each axis.

Each variable position has marginal sampling probability
\(2^{-i}/(m/2^i)=1/m\). Anchor and dummy selections are independent of
every opposite-axis selection. The root selections, whose node is
always 0, are independent uniform choices too. Therefore every cell
with an anchor or dummy endpoint, and every root-to-root cell, is
selected with probability exactly \(1/m^2\). Within each class there is
only one selection. A union bound over edited cells of these types
gives probability at most \(M/m^2<1\) that any such selected cell was
edited. Fix a selection with none edited.

This statement does NOT apply to arbitrary variable-to-variable cells:
for example a fixed diagonal leaf cell is selected with probability
1/m, because the two axes share z. No such independence is used below.

This argument uses only the designated mode embeddings; it does not
require all copies of S to be rigid. Suppose B were H-free. Its selected
anchors still form S, and their signatures against selected body positions
and all dummy incidences
are unchanged. Thus whenever a mode's selected body is P, it extends
to H in B. Its absence forces the following implications.

The unchanged root-plus diagonal is one and root-minus diagonal is
zero. Suppose at depth i-1 these values are still one and zero.
The \(V_i^+\) and \(V_i^-\) bodies respectively have form

\[
 \begin{pmatrix}1&b_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}1&0\\1&b_-\end{pmatrix}.
\]

Avoiding P forces \(b_+=1\) and \(b_-=0\). These are the entries from selected
depth-i rows to selected depth-(i-1) columns. Next use the W modes
with \(d=a_i\bmod 2\). Their bodies respectively have form

\[
 \begin{pmatrix}1&c_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}c_-&0\\1&1\end{pmatrix}.
\]

Avoiding P forces \(c_+=1\) and \(c_-=0\) at the depth-i diagonals. All four
bodies are in increasing row/column order because their selected
nodes are parent and child, and dummy positions have the stipulated
extreme orders. Induction carries opposite values to depth h. At
that depth the plus and minus diagonals are the same cell, a
contradiction. Hence B is not H-free.

Every H-free repair requires at least \(m^2\) changes. Dividing by
\(n^2=d^2m^2\) gives \(\operatorname{dist}_H(A_h)\ge d^{-2}\). No restrictions were imposed on
unprotected entries or on the directions of the changes.

For a concrete distinction between hitting and repairing, flipping every
cell of \(T_h\) from zero to one destroys all original copies but creates new
ones. In mode \(V_h^-\) choose body rows \(R_{h-1}^-(b)\), \(R_h^-(p)\) with \(\pi(p)=b\),
and body columns \(C_*\), \(C_{h-1}^-(b)\). Their entries after these flips are P:
the parent-minus diagonal remains zero and the leaf-to-parent entry is now
one. The unchanged designated anchors extend this body to H.

## 8. Final implication and sampling consequence

For \(\epsilon_h=(14h+2)^{-2}\), the exact count gives, for every fixed \(C>0\),

\[
 \frac{N_H(A_h)}{\epsilon_h^C n_h^8}
 \le\frac{33}{4}(14h+2)^{2C-8}4^{-h}\longrightarrow0.
\]

Choosing h sufficiently large for any prescribed \(c>0\) proves the announced
failure of every polynomial removal bound, with H fixed first.

For canonical sampling, choose a uniform q-element subset of rows and,
independently, a uniform q-element subset of columns, with \(0\le q\le n\).
Observing H requires sampling a cell in \(T_h\). Therefore

\[
 \Pr(\text{reject})\le2m(q/n)^2=2\epsilon_h2^{-h}q^2.
\]

Rejection probability at least \(\rho>0\) requires

\[
 q\ge\sqrt{\rho/2}\,(14h+2)2^{h/2}
 =\sqrt{\rho/2}\,\epsilon_h^{-1/2}
   2^{(\epsilon_h^{-1/2}-2)/28}.
\]

There are \(q^2\) observed entries. This is a canonical sampler statement, not a
claim about all adaptive or two-sided testers. The dependence remains
\(\exp(\Omega(\epsilon^{-1/2}))\); the new result is the smaller forbidden pattern.

## Verification boundary and comparison

The pinned primary obstruction is 66×66. The earlier local candidates were
15×15 and 5×5, with anchors of size 13 and 3. This candidate uses a 4×4
pattern with a 2×2 anchor component, and allows genuine unintended anchor
copies. The previous limitation on pure two-by-two anchor rigidity remains
true; it does not preclude this whole-pattern localization argument.

[check_four.py](../verification/check_four.py) exhaustively checks the full
pattern through depth 4 without assuming localization, including exact
weights of twin blocks. A separate node-pair summation checks the closed
count through depth 8. The checker also tests the required tree orders,
nonanchor crown exclusion, laminar role supports, protected sampling
probabilities, and arbitrary path assignments. The all-depth proof above
is separate from finite evidence. A subsequent separate-agent adversarial
review found no material error; it is not independent mathematical peer
review. Lean now defines the concrete host and its two orders and proves
anchor-count classification, fixed-zero localization, and a dummy last row
for every actual ordered copy at every depth. The zero-set cardinality upper
bound of 2m, arbitrary-depth propagation, and inherited sampling lemmas are
also checked. Copy counting, concrete arbitrary-repair connections, and the
final removal theorem remain unformalized; novelty screening remains
inconclusive. See the
[assurance checkpoint](../verification/reviews/four-assurance.md).

[check_four_repair.py](../verification/check_four_repair.py) additionally
checks the explicit new copies produced by flipping \(T_h\), for every leaf
through depth 8.

[check_four_literal.py](../verification/check_four_literal.py) reconstructs
the host without importing the original code and repeats the full census
through depth 4, including an expanded depth-one check and negative controls.
[check_four_reviewer.py](../verification/check_four_reviewer.py) preserves
the separate reviewer's support and unbalanced-copy checks through depth 7.
