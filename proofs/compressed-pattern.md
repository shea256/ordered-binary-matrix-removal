# A 15-by-15 ordered binary removal obstruction

Date: 2026-10-10. Category: candidate result with a complete human-readable
proof draft; not independently reviewed or machine checked. All claims in
this file concern induced copies preserving independently increasing row
and column indices, and arbitrary binary entry changes in both directions.

The tree construction and repair mechanism below are adapted from OpenAI,
*Polynomial removal fails for ordered binary matrices*, September 25, 2026,
at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. The proposed new parts
are the three-column nonshattering lemma and the 13-by-13 anchor rigidity
argument. This is a modification of that construction, not a transfer from
ordered graphs. Local source snapshots and their hashes are in
[the manifest](../verification/source_manifest.json).

## Statement

There is an explicit fixed binary matrix H of order 15 such that, for every
integer h >= 1, with m = 2^h, d = 80h+2 and n = dm, there is a binary n-by-n
matrix A_h satisfying

\[
 \operatorname{dist}_H(A_h)\ge d^{-2},\qquad
 N_H(A_h)=2m^{28},\qquad
 \frac{N_H(A_h)}{n^{30}}=2d^{-30}4^{-h}.
\]

Consequently, for all real c,C > 0 there exist n, 0 < epsilon < 1 and A
with dist_H(A) >= epsilon and N_H(A) < c epsilon^C n^30. The pattern is
fixed before c,C,h are chosen. The density normalization is n^30,
not the number of possible submatrices; this is the baseline convention.

## 1. Explicit pattern

Indices in this proof are one based, except for tree nodes and word labels.
Let s=13. For 1 <= u,v <= 13 put

\[
 S(u,v)=
 \begin{cases}
  \left\lfloor (u-6)/2^{13-v}\right\rfloor\bmod 2,
       &6\le u\le13,\quad11\le v\le13,\\
  \mathbf1[u\ne v],&\text{otherwise}.
 \end{cases}
\]

Thus rows 6 through 13 on columns 11 through 13 list 000,001,...,111.
With e_1,e_2 the first two standard unit vectors in {0,1}^13, put

\[
 H=\begin{pmatrix}S&e_1&e_2\\ e_1^T&1&0\\ e_2^T&1&1\end{pmatrix},
 \qquad P=\begin{pmatrix}1&0\\1&1\end{pmatrix}.
\]

S has the following checked elementary properties:

1. Its rows are distinct: rows 1 through 10 have distinct zero positions
   in columns 1 through 10; rows 11 through 13 are all one there and
   have distinct last-three-bit words 101,110,111.
2. Its columns are distinct: columns 1 through 10 have single distinct
   zeros. Each of the last three columns has four zeros, and their
   word-coordinate vectors are distinct.
3. Every column has at most one zero in rows 1 through 6. For columns
   1 through 10 this is the diagonal zero, if present. For columns
   11 through 13 it is precisely the zero in row 6 (word 000).
4. Every row has at most one zero in columns 1 through 6, since this
   region avoids the replacement columns.
5. Every row and column has at least nine ones. Rows 1 through 10
   have at least nine among their first ten entries; the other rows
   have ten there. The last-three columns have nine ones in total.

In particular every column has at least five ones in the first six
rows, and every row has at least five in the first six columns. Any
two columns share a one in the first six rows, and any two rows share
a one in the first six columns (at most two excluded positions).

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

Place one anchor block per mode before every non-anchor position on
each axis. Within an anchor block put s consecutive groups of size m.
Use increasing i, then V^+,V^-,W_0^+,W_1^+,W_0^-,W_1^- to order modes.
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
giving n=(6hs+2h+2)m=(80h+2)m. No labels are part of the binary alphabet:
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

## 3. Stronger non-anchor trace lemma

**Lemma.** No three non-anchor columns are shattered by the non-anchor rows,
for any h>=1. Columns need not be in increasing order.

**Proof.** A dummy column is constantly one, so cannot belong to a
shattered set. Otherwise classify columns by level and sign, counting
the common leaf class L only once. In a class the ones of every variable
row form a suffix when columns are sorted by node; dummy rows are all one.
Thus two columns from the same class cannot be shattered: the word one
on the earlier and zero on the later cannot occur. Equal node indices
or repeated positions also cannot be separated.

It remains to treat three distinct classes. Define a graph on the column
classes: join (i,sigma) to (i-1,sigma) for 1<=i<h, and make a triangle
on L,(h-1,+),(h-1,-). These are two paths ending at that triangle.
For a non-leaf variable row, the only possible nonzero column classes
are its own class and the immediately preceding class of the same sign.
For a leaf row they are exactly among L,(h-1,+),(h-1,-). Consequently
if a variable row is one in two distinct classes those classes are
adjacent in this graph.

If three distinct classes were shattered, each two-one/one-zero word
would require a variable row (a dummy row cannot supply the zero).
Every pair of the three classes would therefore be adjacent. The only
triangle is L,(h-1,+),(h-1,-): a path contains no triangle, and no
earlier-level vertex has two neighbors in the terminal triangle.

Now select columns from those three classes, with node labels q,b_+,b_-
respectively. Only leaf rows can be one in the leaf column. A leaf row
with node p has the three entries

\[
 (\mathbf1[p\le q],\ \mathbf1[\lfloor p/2\rfloor\le b_+],\
   \mathbf1[\lfloor p/2\rfloor<b_-]).
\]

These traces are coordinatewise nonincreasing as p increases, so form
a chain under coordinatewise comparison. They cannot include both
(1,1,0) and (1,0,1), which are incomparable. Non-leaf rows have zero
in the first coordinate, and dummy rows give (1,1,1). Thus the full
trace family cannot contain both words either. This contradicts
shattering and proves the lemma. QED.

The strengthening is sharp for this host: for h>=2, root-plus column
node 0 and level-1 plus column node 0 are shattered. Rows at root plus
and level-1 plus node 0 give 10 and 11. At h=2, leaf nodes 0 and 2
give 01 and 00; at h>2, level-2 plus nodes 0 and 2 give those words.
Thus two-column nonshattering is false.

## 4. Rigidity of the smaller anchor

A variable row or column belongs to the roles of at most four modes.
For a non-leaf row at depth i, these are V_i^sigma,V_{i+1}^sigma and
W_{i,d}^sigma, omitting out-of-range levels. A leaf row belongs to
V_h^+,V_h^- and W_{h,d}^+,W_{h,d}^-. A non-leaf column belongs to
V_{i+1}^sigma,W_{i+1,0}^sigma,W_{i+1,1}^sigma,W_{i,d}^sigma;
a leaf column belongs only to W_{h,d}^+,W_{h,d}^-.
Against a collection using at most one representative per anchor group,
each variable position therefore has at most four ones.

**Lemma.** Every ordered copy of S in A_h uses exactly one representative
of each anchor group of a single mode on each axis, in group order.

**Proof.** Two positions in the same anchor group are twins throughout
the host. Dummy positions on the same axis are also twins. Since S has
distinct rows and columns, a copy uses at most one position from each
anchor group and at most one dummy per axis.

If a copy used at most five anchor rows and at most ten anchor columns,
its last eight rows and last three columns would all be non-anchor:
anchors precede all non-anchors. They would realize all eight words
by S's word rectangle, contradicting Section 3. Thus either at least
six selected rows or at least eleven selected columns are anchors.

First suppose at least six selected rows are anchors, so the first
six are anchors. A selected variable column has at most four ones
against these representatives, but every S column has at least five
ones there. There are no variable columns. Since at most one selected
column is dummy, at least twelve selected columns are anchors. Any
two of them share a one in the first six selected rows, and hence
belong to the same mode t (different modes have zero anchor incidences).
An anchor row of another mode would have at most one one in the copy,
contradicting the minimum nine ones of every S row. Thus all selected
anchor rows belong to t.

A dummy column has at most one one against the first six selected
anchor rows of this mode, since its signature is a unit vector or
zero. This contradicts the required five ones. Therefore all columns
are anchors of t. Any non-anchor row then has at most one one against
them, so all rows are anchors of t too.

If instead there are at least eleven selected anchor columns, use the
first six selected columns and interchange the axes in the argument:
each S row has at least five ones there; variable rows have at most
four; at least twelve rows are anchors; any two share a one among those
six columns; the remaining dummy row and non-anchor columns are excluded
by unit-vector sparsity and the minimum row/column density. Thus this
case also forces both axes into a single mode.

There are thirteen selected positions and exactly thirteen anchor
groups per axis in that mode, with no group repeated. Every group
is therefore represented, in order. QED.

**Corollary.** In every H copy, the first thirteen rows and columns
belong to one mode's anchor. The last two rows and columns belong to
that mode's roles 1 and 2 respectively. Indeed their anchor signatures
must be e_1,e_2. An anchor from another mode gives zero; an anchor from
the same mode gives a dense S row/column; and only the designated
non-anchor role j gives e_j. This proves the corollary for both axes.

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
required order. Any representatives of that mode's thirteen anchor
groups complete an H copy.

There are m leaf choices, m dummy row choices, two parent column
choices, and m^{26} anchor choices. Each embedding has a unique mode
and leaf, so

\[
 N_H(A_h)=m\cdot m\cdot2\cdot m^{26}=2m^{28}.
\]

Every copy sends the fixed pattern cell (14,14) into the m-cell leaf
diagonal L_h. This also gives the coarser bound N_H(A_h)<=m n^{28},
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
 \frac{N_H(A_h)}{\epsilon_h^C n^{30}}
   =2(80h+2)^{2C-30}4^{-h}\longrightarrow0.
\]

An exponential in h beats every fixed power of h; choosing h sufficiently
large for any c>0 proves the theorem. Also 0<epsilon_h<1 for h>=1.
The constants are uniform over the unbounded sequence, not just finitely
many tested hosts.

For canonical sampling of q uniform rows and, independently, q uniform
columns, rejection on observing H implies sampling one of L_h's m cells.
Thus Pr(reject)<=m(q/n)^2=epsilon_h 2^{-h}q^2. Rejection probability
at least rho>0 requires q>=sqrt(rho)(80h+2)2^{h/2}. Equivalently
q>=sqrt(rho) epsilon_h^{-1/2} 2^{(epsilon_h^{-1/2}-2)/160}
along this sequence. There are q^2 observed entries. This does not claim
a lower bound for arbitrary adaptive or two-sided testers.

Changing every original leaf-diagonal one to zero destroys the old copies,
but creates a new W_{h,d}^+ copy at each leaf: its parent-plus entry
is one, the changed leaf entry is zero, and its dummy bottom row is
11. This makes explicit why the m-cell hitting set is not an m-cell
repair, and why both directions of binary edits must be allowed.

## Verification boundary

The proof is all-depth mathematics; finite exact checks exercise its
inputs and boundaries but are not its justification. Source hashes,
anchor properties, non-anchor triples, mode bodies and weighted counts
are checked by [check_compression.py](../verification/check_compression.py).
No independent reviewer, Lean kernel build, or equivalence check of a
new formal statement has been performed. The released 66-by-66 Lean
proof is not a formal proof of this 15-by-15 construction.
