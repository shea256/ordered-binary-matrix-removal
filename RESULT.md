# Result — OPENAI-190

**Category: Candidate result.** The current proposed obstruction is **5×5**,
refining the earlier **15×15 candidate** and the pinned primary manuscript's
**66×66** pattern. A complete [proof draft](proofs/five-by-five.md) and exact
finite checks are included. Independent mathematical review, formalization,
and a conclusive novelty assessment remain pending.

The explicit fixed pattern is

\[
H=\begin{pmatrix}
0&1&1&1&0\\
1&0&1&0&1\\
1&1&0&0&0\\
1&0&0&1&0\\
0&1&0&1&1
\end{pmatrix}.
\]

For every integer h≥1 the candidate construction has

\[
 n_h=(20h+2)2^h,\quad \epsilon_h=(20h+2)^{-2},\quad
 \operatorname{dist}_H(A_h)\ge\epsilon_h,\quad N_H(A_h)=2\,2^{8h}.
\]

The exact normalized copy density is
\(2(20h+2)^{-10}4^{-h}\). Dividing by \(\epsilon_h^C\) tends to zero
for every fixed C>0. H is independent of h,c,C. Hosts are binary; copies
match zeros and ones and preserve separate row and column orders; repairs
permit arbitrary entry changes in both directions, including anchor cells.
This is an all-depth claim, not a finite-example theorem.

| Parameter | Pinned primary construction | Earlier candidate | Current candidate |
| --- | --- | --- | --- |
| Fixed forbidden pattern | 66×66 | 15×15 | 5×5 |
| Anchor | 64×64 | 13×13 | 3×3 |
| Host order | (386h+2)2^h | (80h+2)2^h | (20h+2)2^h |
| Distance lower bound | (386h+2)^−2 | (80h+2)^−2 | (20h+2)^−2 |
| Exact density from localization | 2(386h+2)^−132 4^−h | 2(80h+2)^−30 4^−h | 2(20h+2)^−10 4^−h |
| Verification stage here | Sources audited; no Lean build | Written draft; finite checks | Written draft; finite checks |

The baseline's exact density is derived from its existing localization
argument, stronger than its headline bound. Different pattern sizes have
different density normalizations; this table is not a numerical ratio
between densities for the same forbidden pattern.

The new proof uses three ingredients: the nonanchor host excludes the
3×3 off-diagonal-one matrix; role supports are whole classes or parity
halves; and ordering W modes before V modes makes containing supports
come later. Together these force every copy of that 3×3 anchor into a
single intended block. The original V-before-W order fails this rigidity
property already at h=2; the report includes the explicit unintended copy.
The tree host, arbitrary-repair propagation and sampling mechanism, and
leaf localization remain adaptations of OpenAI's construction.

**Exact finite evidence:** 5,813,724 quotient row triples in exhaustive
ordered anchor searches through h=6, with no unintended copies; all
1,567,588 quotient row quintuples in full H searches at h=1,2; 156,576
nonanchor column triples; role-support checks through h=8; weighted mode
counts through h=6; 34,952 arbitrary path assignments; and 74,898 terminal
threshold cases. The first two hosts have exactly 512 and 131,072 H copies.
These checks support the proof but do not establish universal quantifiers.

**Method limitation:** all 16 binary 2×2 patterns occur among nonanchors
at h=2. No 2×2 anchor can satisfy this same pure-anchor rigidity property
in the unchanged nonanchor host. This does not prove that 5×5 is minimal
among all possible obstruction constructions.

The canonical sampler bound has exponential denominator 40, versus 160
for the earlier candidate and 772 for the primary baseline; the dependence
remains exp(Omega(epsilon^−1/2)). No arbitrary adaptive/two-sided tester or
host-generation complexity improvement is claimed.

See [BASELINE.md](BASELINE.md), [ATTEMPT.md](ATTEMPT.md),
[RUNLOG.md](RUNLOG.md), and [HANDOFF.md](HANDOFF.md). The earlier 15×15 review package is preserved in the
[initial commit](https://github.com/shea256/ordered-binary-matrix-removal/tree/fa2aa33105d7d16ae782f4a0858a417e31de9f05).
This repository's current manuscript and verification reports describe the
5×5 candidate. Independent review remains pending.
