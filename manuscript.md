# A 3×3 ordered binary matrix removal obstruction

Ryan Shea, with Codex assistance. October 12, 2026.

**Candidate result with a Lean-checked qualitative theorem.** The forbidden
pattern has nine entries, down from twelve in our previous 3×4 construction.
We retain arbitrary binary repairs, arbitrarily small distance parameters,
and arbitrarily large hosts at the same chosen parameter. Independent
mathematical peer review is pending; no global minimality or worldwide
priority is claimed.

The written construction below has n=(8h+2)m and exactly 7m⁴ copies. A separate
AI reviewer found no gap in this argument. The Lean proof establishes the same
qualitative theorem using doubled anchor blocks, n=(14h+2)m, and the sufficient
bound 2mn⁴. It does not certify the written exact count or smaller host size.
Section 8 specifies the formal statement and evidence.

The signed tree, threshold entries, mode roles and protected-path argument
build on OpenAI's #190 manuscript and formalization. The row supports adapt
our [3×4 construction](proofs/three-by-four.md); the new changes are one
anchor on each axis, suffix column anchors and vertical-dummy ones.
Erebos Labs' earlier 4×4 theorem, ProveIt's 5×5 work and Zinan Wang's 4×4
quantitative result are credited in [BASELINE.md](BASELINE.md) and
[ATTRIBUTION.md](ATTRIBUTION.md). In particular, Wang's manuscript also gives
the exact count of our preceding 4×4 refinement, with a different mode order.

## 1. Statement and quantitative implication

Let

\[
 K=J_3-I_3=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix}.
\]

For every integer h≥1, put m=\(2^h\), d=8h+2 and n=dm. The square binary
host \(A_h\) defined below satisfies

\[
 D_K(A_h)\ge m^2,\qquad N_K(A_h)=7m^4,
 \qquad \frac{N_K(A_h)}{n^6}=7d^{-6}4^{-h}.
\]

\(D_K\) minimizes **all binary edits in both directions, at arbitrary cells**.
Copies preserve independent increasing row and column orders and match all
nine entries. No exact minimum repair distance is claimed.

Consequently, for every c,C,ε₀>0 there exists a fixed 0<ε<ε₀ such that,
for every N, some n≥max(1,N) and binary n×n host require at least εn²
edits to become K-free and have fewer than c \(ε^C\) n⁶ copies. This is a
3×3 pattern, with 9 rather than the preceding 3×4 pattern's 12 entries.

Bitwise complementation gives the same statement for the **3×3 identity
matrix**: every K-copy in A corresponds to an I₃-copy in 1−A, and
B↦1−B preserves edit distance and exchanges the two freeness conditions.

## 2. Complete host specification

At each depth 0≤i<h and node p∈{0,…,\(2^i−1\)}, create blocks \(R_i^−\)(p),
\(R_i^+\)(p), \(C_i^−\)(p), \(C_i^+\)(p), each of size m/\(2^i\). At depth h, identify
both signs with leaf blocks \(L_R\)(p), \(L_C\)(p), of size one. Create dummy
blocks \(R_*\), \(C_*\) of size m.

The recursive row order is minus block, left subtree, right subtree, plus
block. The column order is plus block, left subtree, right subtree, minus
block. Dummy rows follow all variable rows; dummy columns precede all
variable columns. Every nonanchor entry incident to a dummy is one.
All variable entries are zero except these threshold entries:

| Row / column | Entry | Range |
| --- | --- | --- |
| \(R_i^+\)(p), \(C_i^+\)(q) | 1[p≤q] | 0≤i≤h |
| \(R_i^−\)(p), \(C_i^−\)(q) | 1[p<q] | 0≤i<h |
| \(R_i^+\)(p), \(C_{i−1}^+\)(q) | 1[⌊p/2⌋≤q] | 1≤i≤h |
| \(R_i^−\)(p), \(C_{i−1}^−\)(q) | 1[⌊p/2⌋<q] | 1≤i≤h |

At i=h the first rule means the leaf-to-leaf matrix, and both parent
rules apply to the shared leaf row. Write π(p)=⌊p/2⌋. A class is the
union over all nodes at a fixed signed depth; a parity subscript restricts
the node parity.

There are six modes at each i=1,…,h:

| Mode | Row role 1 | Row role 2 | Column role 1 | Column role 2 |
| --- | --- | --- | --- | --- |
| \(V_i^+\) | \(R_i^+\) | \(R_{i−1}^+\) | \(C_*\) | \(C_{i−1}^+\) |
| \(V_i^−\) | \(R_{i−1}^−\) | \(R_i^−\) | \(C_*\) | \(C_{i−1}^−\) |
| \(W_{i,e}^+\) | \(R_{i,e}^+\) | \(R_*\) | \(C_{i−1}^+\) | \(C_{i,e}^+\) |
| \(W_{i,e}^−\) | \(R_{i,e}^−\) | \(R_*\) | \(C_{i,e}^−\) | \(C_{i−1}^−\) |

Add one row block \(X_t\) and one column block \(Y_t\) of size m per mode t.
All X blocks precede all nonanchor rows. All Y blocks follow all
nonanchor columns. The mode order on each axis is \(W^−\) in increasing
(i,e), then \(W^+\) in increasing (i,e), then \(V_1^+\),\(V_1^−\),…,\(V_h^+\),\(V_h^−\).

Set A(\(X_s\),\(Y_t\))=1[s=t]. On nonanchor rows, the one-set of \(Y_t\) is exactly

\[
 U_t=(\text{row role 1 of }t)\ \cup\
 \begin{cases}R_* & t\text{ vertical},\\\varnothing&t\text{ horizontal}.\end{cases}
\]

The one-set \(T_t\) of \(X_t\) on nonanchor columns is:

| t | \(T_t\) |
| --- | --- |
| \(V_i\)^σ | \(C_{i−1}\)^σ |
| \(W_{i,e}^+\) | \(C_*\) ∪ \(C_{i,e}^+\) |
| \(W_{i,1}^−\) | \(C_*\) ∪ \(C_{i−1}^−\) |
| \(W_{i,0}^−\), i<h | \(C_*\) ∪ \(C_{i−1}^−\) ∪ \(C_{i,1}^−\) |
| \(W_{h,0}^−\) | \(C_*\) ∪ \(C_{h−1}^−\) |

All unspecified entries are zero. In particular, the odd-child addition
is absent at the shared leaves. Each axis has 6hm anchor positions and
(2h+2)m nonanchor positions, so n=(8h+2)m.

On the two column roles \(X_t\) has signature 01; on the two row roles \(Y_t\)
has signature 10. The added dummy one for vertical \(Y_t\) is outside both
row roles. Thus every ordered role body P=((1,0),(1,1)) extends to K
using \(X_t\) as the first row and \(Y_t\) as the last column.

## 3. Elementary order and support facts

Blocks in a fixed class occur in increasing node order. A fixed nonanchor
row is nondecreasing along a column class; a fixed nonanchor column is
nonincreasing along a row class. These follow from the four thresholds.
For the comparisons used below, the recursive order gives

\[
\begin{aligned}
 C_{i-1}^+(a)<C_i^\sigma(q)&\iff a\le\pi(q),\\
 C_i^\sigma(q)<C_{i-1}^-(b)&\iff\pi(q)\le b,\\
 C_{i-1}^-(b)<C_i^\sigma(q)&\iff b<\pi(q),\\
 C_j^+(a)<C_j^-(b)&\iff a\le b,\\
 R_i^+(p)<R_{i-1}^+(a)&\iff\pi(p)\le a,\\
 R_{i-1}^-(a)<R_i^-(p)&\iff a\le\pi(p).
\end{aligned}
\]

Child signs can be the common leaf sign; the same-level cross-sign
comparison has j<h. Reverse comparisons have the complementary inequalities.

**Nonanchor crown exclusion.** A dummy cannot occur in a crown, since
each crown row and column contains a zero. Two crown columns cannot be
in one variable class, because their one-sets would be nested. The classes
on which a nondummy row can be one are its own and preceding signed
classes, or, for a leaf row, \(L_C\),\(C_{h−1}^+\),\(C_{h−1}^−\). Three distinct
column classes with a common nondummy neighbor for each pair must
therefore be this last triple: elsewhere the class-incidence graph is
two paths. The two crown rows incident to the leaf column must both be
leaves. Their nonanchor neighborhoods are nested as the leaf index
increases, contradicting the crown's incomparable row traces. This
excludes every row/column permutation of the crown in the nonanchor body.

**Crossing anchor supports.** Suppose modes A<B have ordered variable
columns u<v<w with

\[
 u\in T_B\setminus T_A,\quad v\in T_A\setminus T_B,
 \quad w\in T_A\cap T_B.
\]

Then A=\(W_{i,0}^−\) for i<h, and B is \(W_{i+1,e}^−\) or \(V_{i+1}^−\).
Moreover v∈\(C_{i−1}^−\), w∈\(C_{i,1}^−\), and u is in \(C_{i,0}^−\) or,
when B=\(W_{i+1,0}^−\) and i+1<h, in \(C_{i+1,1}^−\).

Here is an exhaustive justification from the support table. At one minus
level the supports are nested. Distinct minus levels have a variable
intersection only at successive levels with the earlier mode's odd-child
addition. A minus mode can cross a later vertical support only when that
support is its full child class. Plus horizontal supports at distinct
levels have no variable intersection; at one level they are disjoint
apart from \(C_*\). A plus horizontal support and a later vertical support
can cross only in the former's parity class, leaving \(C_*\) as the first
support's exclusive part. It cannot be v, since u<v and \(C_*\) is first.
Vertical supports are distinct full classes. Plus and minus variable
supports do not intersect: the minus odd-child addition never reaches
the shared leaf class. These exhaust the mode types and their order.

## 4. Every copy has exactly one anchor on each axis

Write a copy on r₁<r₂<r₃ and c₁<c₂<c₃. Let a,b count its anchor
rows and columns. Rows and columns of K are pairwise distinct, so no
twin block can be used twice. Row anchors form a prefix of the copy;
column anchors form a suffix.

**a=0.** If b=0, use nonanchor crown exclusion. Otherwise c₃=\(Y_t\).
Its ones on r₁,r₂ put them in the same variable class: neither can
be the last nonanchor row type, the dummy. If b=1 or 2, c₁ is
nonanchor, and its trace 01 on r₁<r₂ contradicts nonincreasing
entries within their row class. If b=3, c₁ and c₂ have opposite
traces 01 and 10 on those two rows. On one variable class a U support
is empty, full, or one parity half. Thus these two supports must be
the two opposite parity halves, both belonging to horizontal modes.
They are disjoint even on the dummy, contradicting their two ones on r₃.

**a≥1, b≥2.** Row r₁ is an X block and is one on both c₂,c₃.
It is one on only one Y block, so these columns would be twins.

**a≥2, b=1.** Column c₃ is one on both r₁,r₂. Its unique matching
X block makes these rows twins.

**a≥2, b=0.** Put (u,v,w)=(c₁,c₂,c₃). The common w and the middle
v cannot be dummy because earlier columns exist. If u were dummy,
the earlier anchor would be vertical and the later one horizontal,
contrary to the global mode order. Thus all three columns are variable,
and the first two supports give the crossing configuration of Section 3.
If a=2, r₃ is
nondummy (it is zero on w). It must be one on u,v. When u is at level
i+1, the two levels i+1 and i−1 are too far apart for one nonanchor
row support. When u is in even \(C_i^−\), r₃ must be in \(R_i^−\). Since
u<w within that class, its one on u forces a one on w, a contradiction.
If a=3, no anchor support contains both \(C_{i−1}^−\) and \(C_{i+1}^−\).
The only anchor support spanning \(C_{i−1}^−\) and \(C_i^−\) adds odd
children, not the required even u. This is also impossible.

We are left with a=1 and b≤1. Suppose b=0. Now c₂,c₃ lie in \(T_t\)
for r₁=\(X_t\). They are variable, since a smaller c₁ exists. If they
belong to the same class, the trace 10 of r₃ on c₂<c₃ is impossible.
The only remaining support is T_{\(W_{i,0}^-\)}, i<h, and their classes
are \(C_{i−1}^−\),\(C_i^−\) in some order. The common positive column c₁
of r₂,r₃ is not dummy, since this \(T_t\) contains \(C_*\). Both lower rows
are nondummy. Inspection of their own/parent supports puts the class
of c₁ in {\(C_{i−1}^−\),\(C_i^−\)}: a row incident to the former has depth
i−1 or i, and a row incident to the latter has depth i or i+1;
intersections have no third class, including when i+1=h. If c₁ has
c₂'s class, row r₂ has forbidden trace 10 on c₁<c₂. If it has
c₃'s class, row r₃ has that trace on c₁<c₃. Therefore b=1.

## 5. Localization and exact enumeration

We now have r₁=\(X_t\) and c₃=\(Y_t\), with the same mode because their
corner entry is one. Row r₂ is variable, lies in row role 1 of t,
and satisfies

\[
 c_1\notin T_t,\quad c_2\in T_t,\quad
 A(r_2,c_1)=1,\quad A(r_2,c_2)=0.
\]

The later row r₃ is one on both nonanchor columns and zero on \(Y_t\).

**t=\(V_i^+\).** Here r₂=\(R_i^+\)(p), c₂=\(C_{i−1}^+\)(q), and π(p)>q.
Since r₃ is zero on \(Y_t\), it is neither dummy nor in \(R_i^+\).
Its one on c₂ forces r₃=\(R_{i−1}^+\)(a). Row order gives π(p)≤a,
while that one gives a≤q, a contradiction.

**t=\(V_i^−\).** Now r₂=\(R_{i−1}^−\)(p), c₂=\(C_{i−1}^−\)(q), p≥q.
The zero on \(Y_t\) excludes the dummy and \(R_{i−1}^−\), so r₃ must
be \(R_i^−\)(a), allowing a leaf. Row order and its one on c₂ give
p≤π(a)<q, a contradiction. These two exclusions use the new dummy
ones on vertical Y blocks.

**t=\(W_{i,e}^+\).** The row r₂ and column c₂ are in the same plus
child class and parity; their nodes p,q satisfy p>q. A positive c₁
outside \(T_t\) cannot be dummy. If c₁ is in the child class, monotonicity
contradicts c₁<c₂. If it is a plus parent with node u, positivity and
order give π(p)≤u≤π(q), impossible for p>q of equal parity. At the
leaf level a minus parent is additionally possible, but then
π(p)<u<π(q), also impossible.

**t=\(W_{i,e}^−\).** Write r₂=\(R_i^−\)(p), or \(L_R\)(p) when i=h.
If c₂ is an added odd child, then i<h, e=0, and its node q satisfies
p≥q. The only positive c₁ outside \(T_t\) is an own-level node u>p;
its order before c₂ gives u<q, impossible. Thus c₂=\(C_{i−1}^−\)(b)
and π(p)≥b.

For i<h, a positive c₁ outside \(T_t\) must be \(C_i^−\)(q), with q>p.
Its position before c₂ gives π(q)≤b. Thus π(q)=b=π(p), p is even,
and q=p+1 is odd. But this odd child belongs to \(T_t\), a contradiction.
This is the precise use of the nonterminal odd-child addition.

Consequently i=h. Column c₁ is either a leaf q≥p or a plus-parent
\(C_{h−1}^+\)(u) with π(p)≤u. Its order before c₂ gives π(q)≤b in
the first case and u≤b in the second. Combining with π(p)≥b forces

\[
 b=\pi(p),\qquad
 c_1\in\{L_C(q):p\le q,\ \pi(q)=\pi(p)\}
          \ \cup\ C_{h-1}^+(\pi(p)).
\]

Finally r₃ must be dummy. A variable row one on \(C_{h−1}^−\)(π(p))
is either a leaf v or \(R_{h−1}^−\)(a). A later leaf has v>p and
cannot satisfy π(v)<π(p). A later parent-minus row has a>π(p)
and cannot satisfy a<π(p). No other variable row can be one there.

We have classified every copy: for a leaf p, it uses X_{\(W_{h,p mod 2}^-\)},
\(L_R\)(p), \(R_*\); \(C_{h−1}^−\)(π(p)); the matching Y block; and either
a leaf q≥p in that parent's two-leaf interval or \(C_{h−1}^+\)(π(p))
as its first column. Conversely these choices have the required order
and all nine entries, directly by the host rules.

Three anchor/dummy choices contribute m³, and the minus-parent column
contributes 2. The first column has 2 plus-parent choices and 2 leaf
choices for even p, or 2 plus-parent choices and 1 leaf choice for odd p.
There are m/2 leaves of each parity, so

\[
 N_K=\frac m2\cdot2m^3(4+3)=7m^4.
\]

The two families contribute 4m⁴ and 3m⁴ respectively. In particular
every copy's middle zero lies in the 2m-cell leaf-to-own-minus-parent set.

## 6. Lower bound against arbitrary repairs

Let a binary B differ from \(A_h\) on M<m² cells. Sample a uniform leaf z
and its ancestor path. Independently choose a uniform representative
from each signed row and column block on the path, identifying the two
sign choices at the shared leaf on each axis. Choose independent uniform
representatives from every anchor and dummy block.

Every variable or dummy position has marginal probability 1/m, and each
anchor position has probability 1/m. A cell with an anchor or dummy
endpoint has selection probability 1/m², since that representative is
independent of the other axis. The same holds for either root-to-root
cell. Protect all such selected cells. The union bound gives a selection
with no edited protected cell. We make no such probability assertion for
general variable-variable cells or the shared leaf diagonal.

If B is K-free, every selected ordered role body must avoid P, by the
unchanged five anchor incidences completing it to K. The root-plus
diagonal is one and root-minus diagonal zero. Assuming these values at
a parent, the two vertical bodies are

\[
 \begin{pmatrix}1&b_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}1&0\\1&b_-\end{pmatrix}.
\]

P-freeness forces b_+=1,b_−=0. The horizontal bodies of the selected
child parity are then

\[
 \begin{pmatrix}1&c_+\\1&1\end{pmatrix},\qquad
 \begin{pmatrix}c_-&0\\1&1\end{pmatrix},
\]

forcing c_+=1,c_−=0. All four bodies are ordered by the recursive
tree order and have their dummy entries protected. Induction reaches
the common leaf diagonal, a contradiction. Therefore \(D_K\)(\(A_h\))≥m².
Edits to anchors, dummies and either binary label were never restricted.

## 7. Final quantifiers and blowups

Set \(ε_h\)=(8h+2)⁻². For every fixed C>0,

\[
 \frac{N_K(A_h)}{n_h^6\epsilon_h^C}
 =7(8h+2)^{2C-6}4^{-h}\longrightarrow0.
\]

Given c,C,ε₀>0, choose h with \(ε_h\)<ε₀ and this ratio<c. Replace each
physical row and column by q consecutive identical twins. The pattern's
distinct rows and columns prevent a copy from reusing a projected row
or column, so its count multiplies exactly by q⁶. The repair sampler
works with blocks q times larger: protected-cell probabilities are
(qm)⁻², and the lower bound is q²m². Both normalized bounds are unchanged.
Arbitrarily large q yields every prescribed lower threshold on host size
at the **same** \(ε_h\).

## 8. Verification and formal theorem

The [original proof snapshot](proofs/three-by-three.md) is retained byte for
byte at the SHA-256 recorded in the
[separate-agent adversarial review](verification/reviews/three-by-three-adversarial.md).
Sections 1–7 above reproduce its mathematical argument. The review found no
gap and suggested two clarifications: the class-incidence paths meet at the
leaf class, and the middle column in the W cases cannot be the dummy column
because its middle-row entry is zero. These observations are already implied
by the definitions. Separate-agent review is not human mathematical peer review.

The [discovery census](experiments/three_by_three_candidate.py) and
[literal checker](verification/check_three_by_three.py) agree through h=7,
including hosts of order 7,424. The latter checks expanded h=1, three-seed
repair guards through h=4, all Boolean propagation states, and negative
controls omitting each essential added support. The
[reviewer's independent implementation](verification/check_three_by_three_reviewer.py)
rebuilds the host from the prose, with complete weighted censuses through h=6
and physical censuses through h=3. Its optional SAT check establishes exact
repair distances only at h=1 and h=2. Finite checks do not prove the universal
statement or exact repair equality at all depths.

The principal Lean export is
`OrderedRemoval.Crown.no_polynomial_removal_bound` in
[Complete.lean](formal/OrderedRemoval/Crown/Complete.lean). It proves the
qualitative theorem of Section 1 with the same literal 3×3 crown and n⁶
normalization: every c,C,ε₀>0 admits a fixed 0<ε<ε₀ such that every host-size
threshold N admits an n≥max(1,N) and a square binary host with at least εn²
edits required in every crown-free binary repair and fewer than c \(ε^C\) n⁶
ordered copies. There are no host-existence, localization, sampling or
anchor-preservation hypotheses.

For this certificate each anchor block on each axis is doubled to size 2m,
represented by two consecutive identical subgroups of size m. All body and
dummy blocks, entry rules and relative block orders are retained. The formal
host has n=(14h+2)m. Localization bounds the number of eligible middle-zero
cells by 2m; encoding the other four indices gives at most 2mn⁴ copies.
The protected sampler still gives a repair lower bound m². Consequently
ε=(14h+2)⁻² and the density is at most 2ε2⁻ʰ. Exponential decay and uniform
blowups prove the full quantifier order. This certifies the qualitative
3×3 result, not the exact 7m⁴ count on the more economical written host.

The [source-bound audit](verification/reference/crown-formal-audit.json)
built and checked 92 local modules, 573 named theorems and 2,163 declarations,
including inherited infrastructure. The Crown development adds 19 modules,
88 named theorems and 257 declarations. Only `propext`, `Quot.sound`, and
`Classical.choice` occur as transitive axioms. Each local module was replayed
into its imported Lean environment; the audit does not freshly replay all
Mathlib or use a different proof assistant. Lean is pinned to 4.34.1 and
Mathlib to `d13f23b723b8a846827a245b89c10fc7d3f11612`.

The [executed-model check](verification/reference/crown-formal-model-report.json)
compares the actual Lean host and axis orders with a separate Python model
through h=3, covering 139,332 entries, and physical copy counts through h=2.
The [formal semantic note](verification/reviews/three-by-three-formal-scope.md)
is a same-agent second pass. The separate adversarial reviewer covered the
written proof, not this Lean port. Exact repair equality, global minimality,
and worldwide priority remain outside the certificate.

See [formal/README.md](formal/README.md) and [RUNLOG.md](RUNLOG.md) for
reproducible commands, historical checkpoints and verification boundaries.
