# Result — OPENAI-190

**Category: Candidate result.** The current proposed obstruction is **4×4**,
refining the earlier **5×5** and **15×15 candidates** and the pinned primary
manuscript's **66×66** pattern. A complete [proof draft](proofs/four-by-four.md)
and [exact finite checks](verification/reference/four-report.json) are included.
Independent mathematical review, formal verification, and a conclusive
novelty assessment remain pending.

The explicit fixed forbidden pattern and its anchor component are

\[
H=\begin{pmatrix}
0&1&1&0\\
1&0&0&1\\
1&0&1&0\\
0&1&1&1
\end{pmatrix},\qquad
S=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

For every integer h≥1 the candidate host has

\[
 m=2^h,\quad n_h=(14h+2)m,\quad
 \operatorname{dist}_H(A_h)\ge\epsilon_h=(14h+2)^{-2}.
\]

At h=1 there are exactly 128 copies. For h≥2 the exact count is

\[
 N_H(A_h)=\frac{33}{4}m^6-\frac{29}{2}m^5.
\]

For all h the normalized density is at most
\(\frac{33}{4}(14h+2)^{-8}4^{-h}\). Its ratio to \(\epsilon_h^C\) tends
to zero for every fixed C>0. Thus for every c,C>0 the same fixed H has a
binary host at least epsilon-far from H-freeness with fewer than
\(c\epsilon^C n^8\) copies. Copies match zeros and ones and preserve
independent row and column orders. Repairs may change any cells in either
direction. These universal statements rest on the written proof, not on
extrapolation from finite tests.

| Parameter | Pinned primary | Earlier candidate | Earlier candidate | Current candidate |
| --- | --- | --- | --- | --- |
| Forbidden pattern | 66×66 | 15×15 | 5×5 | 4×4 |
| Anchor component | 64×64 | 13×13 | 3×3 | 2×2 |
| Host order | (386h+2)2^h | (80h+2)2^h | (20h+2)2^h | (14h+2)2^h |
| Distance lower bound | (386h+2)^−2 | (80h+2)^−2 | (20h+2)^−2 | (14h+2)^−2 |
| Density bound | 2(386h+2)^−132 4^−h | 2(80h+2)^−30 4^−h | 2(20h+2)^−10 4^−h | (33/4)(14h+2)^−8 4^−h |
| Verification here | Sources audited; no Lean build | Draft; finite checks | Draft; finite checks | Draft; finite checks |

The first three densities are exact, derived from their localization proofs;
the last is a uniform upper bound with the exact count above. Different
pattern sizes have different normalizations, so the table does not give a
ratio of removal bounds for the same pattern.

## What changed mathematically

All 16 binary 2×2 patterns already occur among nonanchors. Consequently
pure two-by-two anchor rigidity remains impossible in this host. The new
argument avoids that requirement: it classifies **full H copies**. Every
copy has two anchor rows and either two or one anchor columns. The extra
one-anchor-column copies are allowed and counted explicitly.

Every full copy sends its fixed zero cell (3,4) to a leaf row and that leaf's
parent-minus column block. There are only 2m such zero cells. The previous
leaf-diagonal set does not meet every copy; an explicit depth-two
counterexample is in the report. The new zero-cell localization yields the
copy bound and the canonical sampling bound. The inherited arbitrary-repair
argument needs only designated mode embeddings, so it still applies without
pure anchor rigidity.

Even the coarse count obtained from those 2m zero cells suffices for the
universal obstruction; the exact formula is a further density refinement.
Flipping all those zeros creates new copies, illustrating why original-copy
hitting and arbitrary repair distance must be kept distinct.

The new proof uses crown exclusion and ordered laminar role supports from
the 5×5 draft. Within each depth, the order is W+0,W+1,W−0,W−1,V+,V−.
Reversing the minus parity modes creates nonleaf copies already at h=3;
the report includes that boundary witness. The tree host and arbitrary-edit
propagation remain adaptations of OpenAI's construction.

## Exact finite evidence and limits

The checker exhaustively examines 3,693,411 quotient row quadruples across
h=1,...,4 and all matching increasing column quadruples, with exact block
multiplicities. It assumes no copy localization. The actual host orders are
32, 120, 352, 928 and the exact copy counts are 128; 18,944; 1,687,552; 123,207,680.
Every copy satisfies the stated zero-cell localization and falls in a listed
family. A separate integer node-pair sum matches the closed formula through
h=8. Crown exclusion, laminar supports, strict tree orders, 34,952 arbitrary
path assignments, and exact protected-cell probabilities also pass.

These are same-agent checks, not independent review or a universal
machine-checked proof. No global minimality claim is made: 3×3 and other
smaller patterns remain unresolved here. The canonical sampler bound has
exponential denominator 28, with prefactor sqrt(rho/2), and remains
exp(Omega(epsilon^−1/2)). No arbitrary adaptive/two-sided tester or
host-generation complexity improvement is claimed.

See [BASELINE.md](BASELINE.md), [ATTEMPT.md](ATTEMPT.md),
[RUNLOG.md](RUNLOG.md), and [HANDOFF.md](HANDOFF.md). The previous 5×5
mathematical release is preserved at commit
`f16d432d9a918c694f0b404a12f744c0c8b0db03`; its proof and finite checks remain
in this repository. The current manuscript and metadata describe the 4×4
candidate. Independent mathematical review remains pending.
