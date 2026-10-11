# An optimized anchor order for the known 4×4 removal obstruction

October 11, 2026. **Candidate quantitative refinement; written all-depth proof.**
The 4×4 obstruction is prior work. The new ordering and exact comparison below
are not yet formalized in Lean. Independent mathematical review remains pending.

The tree and arbitrary-repair propagation originate in OpenAI's September 25,
2026 manuscript. Erebos's October 9 releases establish the same H4 and the exact
terminal-anchor repair. The global mode ordering and count below are the local
refinement, with those methods explicitly retained and credited.

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
 \operatorname{dist}_H(A_h)=d^{-2},\qquad
 \frac{N_H(A_h)}{n^8}\le\frac{5}{2}d^{-8}4^{-h}.
\]

For every \(h\ge1\), its exact copy count is

\[
 N_H(A_h)=\frac{5}{2}m^6-m^5.
\]

Copies preserve independently increasing row and column orders and match
both binary values. Distance permits arbitrary changes in both directions,
including anchor cells, and is normalized by \(n^2\). Consequently for every
\(c,C>0\) there are n, \(0<\epsilon<1\) and a binary A with distance at least \(\epsilon\)
from H-freeness but fewer than \(c\epsilon^C n^8\) ordered H copies. The same
fixed four-by-four H works for all c,C.

## 1. Mode order and anchor size

Use s=2 anchor groups of size m per mode on each axis. Put all anchors
before all nonanchors and retain group 1 before group 2 inside each mode.
On both axes order the complete mode blocks in three successive families:

\[
 (W^-_{1,0},W^-_{1,1},\ldots,W^-_{h,0},W^-_{h,1}),\quad
 (W^+_{1,0},W^+_{1,1},\ldots,W^+_{h,0},W^+_{h,1}),\quad
 (V^+_1,V^-_1,\ldots,V^+_h,V^-_h).
\]

Thus all minus-horizontal modes precede every plus-horizontal mode, and all
horizontal modes precede every vertical mode. This is a global reordering
across levels, not merely a permutation of the six modes at each level.
All block multiplicities, entry values on named positions, and nonanchor
orders remain as in the earlier host. The independently ordered physical
matrices change when their anchor positions are reindexed.

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
Use the global three-family mode order of Section 1.
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
in the whole of that class. On the row axis, its \(W_i\) mode precedes every V mode, including \(V_i\) and \(V_{i+1}\).
On the column axis, its \(W_i\) mode precedes every V mode and the
same-sign \(W_{i+1,d}\) modes by increasing level inside that sign family. Equality of supports
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

This localization uses zeros, which induced copies must match. Section 6
will show that the global order further forces every copy to contain a
leaf-diagonal one. The absence of leaf columns in some unbalanced copies
of the previous order does not persist in this construction.

Localization alone already gives \(N_H(A_h)\le |T_h|n^6=2mn^6\), hence
\(N_H(A_h)/n^8\le 2d^{-2}2^{-h}\). Together with the distance bound below,
this suffices to refute every polynomial removal bound. The exact enumeration
in the next section strengthens the density estimate; the qualitative
obstruction does not depend on that enumeration.

## 6. Exact copy count and optimality among block permutations

The balanced count is \(2m^6\): m leaf choices, m dummy row choices, two
parent-minus column positions, and four independent size-m anchor choices.
These copies use the mode \(W^-_{h,d}\), where d is the leaf parity.

For an unbalanced copy fix its leaf \(p=2b+d\). Its second anchor row and
first anchor column belong to \(B=W^-_{h,d}\), groups 2 and 1. Its first
anchor row belongs to a mode A with \(A\le B\). By Section 5, the class K
containing its second and third columns is either the leaf class or the
parent-plus class. Every anchor support on the parent-plus class belongs
to a W-plus or V mode; all such modes occur after B in the new order.
Hence K must be the leaf class.

A leaf column support in a mode no later than B must be group 1 of
\(W^-_{h,e}\), with \(e\le d\). Let q be the node of the third column.
The pattern one there gives \(p\le q\), and its position before the
parent-minus column gives \(\lfloor q/2\rfloor\le b\). Together with
\(p=2b+d\) and \(e\le d\), this forces q=p and e=d. Thus A=B, and the
first anchor row is its group 1. The second column is any leaf
\(q_1<p\) of parity d, giving exactly b choices.

Conversely each of these choices gives all sixteen bits of H in the required
orders. The second column has a zero against leaf row p, the third column
has its diagonal one, and the last column has the required strict-transition
zero. The dummy row supplies the three remaining nonanchor ones.
No other copy family remains.

Each choice of \((p,q_1)\) has three size-m anchor choices, m dummy row
choices, and two parent-column positions, giving multiplicity \(2m^4\).
Writing t=m/2, the number of such pairs is

\[
 \sum_{d=0}^1\sum_{b=0}^{t-1} b=t(t-1).
\]

Therefore, for every \(h\ge1\), including t=1,

\[
 N_H(A_h)=2m^6+2m^4t(t-1)=\frac52m^6-m^5.
\]

**Restricted optimality.** Keep the raw entries, nonanchor orders, weights,
anchor prefix, and group order inside each mode fixed. Permute intact mode
blocks arbitrarily on each axis, even using different permutations on the
two axes. The balanced copies counted above still exist: all their anchors
lie in one mode. The unbalanced copies just enumerated also still exist for
the same reason. Their increasing embeddings depend only on the internal
order of that mode and the unchanged nonanchors. The two families are
disjoint because they use two versus one anchor columns.

Every host in this explicitly restricted class consequently has at least
\((5/2)m^6-m^5\) copies. The global order attains that bound for every h.
This does not optimize over different entries, multiplicities, within-mode
group orders, nonanchor orders, forbidden patterns, or all binary matrices.

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

## 8. Exact repair distance

This upper bound adapts Erebos's previously published terminal-anchor repair;
it is not a new repair method. We check why it survives the new order.
Let U consist of group-1 anchor columns of \(W^-_{h,0}\) and \(W^-_{h,1}\).
Retain every anchor row and replace all entries on nonanchor rows and U
columns by zero, producing B. The original ones there occur exactly at
leaf row p and its parity's mode, with m anchor choices per leaf. Exactly
\(m^2\) entries change, all from one to zero.

First, in any H copy in a matrix agreeing with A on anchor rows, the third
and fourth selected rows must be nonanchor. If the third were anchor, so
would the first two. If the first column were anchor, its ones at rows 2
and 3 would force these anchor rows into one twin group, contradicting
their different entries at column 4. If the first column were nonanchor,
all columns would be nonanchor. The first anchor row's support contains
columns 2 and 3, while the third anchor row's support contains column 3
but not column 2. This is an earlier proper container, contradicting
Lemma 2. Only the unchanged anchor rows were used in either argument.

The last two rows of H have positive union 1111. Therefore a copy in B
could use no column of U, since those columns are zero on every nonanchor
row. Outside U the two matrices agree, so every hypothetical copy in B
would already be a copy in A. The classification in Sections 5–6 shows
that every original copy has its first column in U. This contradiction
proves that B is H-free without assuming localization persists after edits.

Together with Section 7's unrestricted lower bound,

\[
 \min_{B\text{ H-free}} |\{(r,c):A_h(r,c)\ne B(r,c)\}|=m^2,
 \qquad \operatorname{dist}_H(A_h)=(14h+2)^{-2}.
\]

## 9. Quantitative comparison and final theorem

The strongest located 4×4 comparison is
[Erebos’s pinned v1.1.0 release](https://github.com/erebos-labs/ordered-matrix-removal-4x4/tree/6d21ce36e83b71d8a44015016cf3ac77e44b55ff).
Its manuscript gives, for \(h\ge2\),

\[
 N_E=\frac{41}{4}m^6-\frac{37}{2}m^5.
\]

Its v1.1.0 terminal-anchor theorem gives the same exact repair cost \(m^2\).
Our hosts have exactly the same n=(14h+2)m, the same H, both binary labels,
independent increasing axes, and arbitrary binary repairs. Consequently
both raw counts and normalized densities can be compared directly:

\[
 \frac{N_H(A_h)}{N_E}=\frac{10m-4}{41m-74}\longrightarrow\frac{10}{41}.
\]

Thus the limiting reduction is \(31/41\), approximately 75.6098%.
This is not the reduction at every finite depth: it is 60% at h=2 and
about 70.08% at h=3. At h=1 both constructions have 128 copies. At every
\(h\ge2\) the new count is strictly smaller, since

\[
 N_E-N_H(A_h)=\frac{m^5(31m-70)}4>0.
\]

Our previous within-depth order had count \((33m^6-58m^5)/4\) for \(h\ge2\).
The new leading coefficient is 10/33 of that value. These are improvements
in the constant of the density bound, not in its exponent, the size of H,
or the already established failure of polynomial removal.

For \(\epsilon_h=(14h+2)^{-2}\), the exact new bound is

\[
 \frac{N_H(A_h)}{n_h^8}
 =\left(\frac52-2^{-h}\right)(14h+2)^{-8}4^{-h}
 =\left(\frac52-2^{-h}\right)\epsilon_h^4 4^{-h}.
\]

For every fixed C>0 its ratio to \(\epsilon_h^C\) tends to zero. Therefore
for every c,C>0 this same fixed H has a binary counterexample to the
proposed bound \(N_H(A)\ge c\operatorname{dist}_H(A)^C n^8\).

The stronger size quantifiers also survive. For any integer \(\ell\ge1\),
replace every position by \(\ell\) consecutive identical positions on each
axis. Since H has distinct rows and columns, its count multiplies exactly
by \(\ell^8\). Blowing up the explicit repair costs \(\ell^2m^2\).
Conversely, if an H-free repair cost fewer than \(\ell^2m^2\), selecting one
uniform representative of each row and column fiber would have expected
cost less than \(m^2\). Some restriction would be an H-free repair of A
with cost less than \(m^2\), contradicting Section 7. Hence exact normalized
distance and copy density are unchanged. Given any \(\eta>0\) and any
threshold function \(L:(0,1)\to\mathbb N\), first choose h large enough that
\(\epsilon_h<\eta\) and the desired density inequality holds, then choose
\(\ell\) so that \(\ell n_h\ge L(\epsilon_h)\). This matches the stronger
quantifiers of the comparison.

The stronger shape statement in Section 6 makes the m leaf-diagonal cells
an original-copy hitting set: every copy uses (leaf p, leaf p) at pattern
cell (3,3). Hence the coarse count can be sharpened to \(mn^6\). Sampling q
uniform rows and, independently, q uniform columns detects H only if one
of these m cells is selected, so rejection probability is at most
\(m(q/n)^2\). This concerns the canonical sampler inspecting \(q^2\) entries,
not arbitrary adaptive testers; it does not say that flipping the hitting
set produces an H-free matrix. No improved sampling exponent is claimed here.

## Verification boundary and provenance

Erebos publicly released the same H4 and its qualitative Lean theorem on
October 9, before our 4×4 PR on October 10. Its October 9 follow-up proves
exact repair distance for its order. An earlier October 7 ProveIt manuscript
proves a 5×5 obstruction, exact repair, and stronger canonical-sampling
results, and displays the same H4 as a candidate. Our earlier search missed
these sources. They are now credited as prior work; their release records
do not establish worldwide priority. See [BASELINE.md](../BASELINE.md).

The contribution assessed here is the global mode order, the exact count
\((5/2)m^6-m^5\), its optimality within the specified permutation class,
and transfer of the known exact repair. It does not claim a new H4 or the
first Lean proof of its qualitative obstruction.

[check_optimized_order.py](../verification/check_optimized_order.py) recomputes
all copies using a column-quadruple/row-DP census, without assuming
localization, for all four compared orders through depth 4. It also checks
the terminal-anchor repair through depth 4, expanded physical copies at
depth 1, the intrinsic-family sum through depth 10, and 24 within-depth
horizontal-mode permutations at depth 2. These finite checks support the
implementation; the all-depth proof is the argument above.

The retained Lean development proves the qualitative H4 theorem using our
previous within-depth order. It does not yet certify this globally reordered
host, its exact count, exact repair equality, or restricted optimality.
The previous source-bound Lean audit remains valid for those unchanged
sources. Independent mathematical peer review and further novelty screening
remain open. A separate AI review is not peer review.
