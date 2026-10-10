# Result — OPENAI-190

**Category: Candidate result.** A complete proof draft constructs a fixed
**15-by-15** binary pattern with no polynomial ordered induced removal
bound, improving the **66-by-66** pattern in the pinned primary manuscript.
Exact finite checks pass. Independent proof review, Lean verification,
and a conclusive novelty assessment remain outstanding.

For every integer h>=1, the explicit construction has

\[
 n_h=(80h+2)2^h,\quad \epsilon_h=(80h+2)^{-2},\quad
 \operatorname{dist}_H(A_h)\ge\epsilon_h,\quad
 N_H(A_h)=2\,2^{28h}.
\]

Thus N_H(A_h)/n_h^30 = 2(80h+2)^-30 4^-h, and the ratio to
epsilon_h^C tends to zero for **every** fixed C>0. The pattern is
independent of h,c,C. Hosts are binary; copies match both zeros and
ones and preserve independent axis orders; distance permits every
binary change in either direction. The statement concerns arbitrarily
large depths, not just the tested finite matrices.

| Parameter | Primary baseline | Candidate |
| --- | --- | --- |
| Fixed forbidden pattern | 66-by-66 | 15-by-15 |
| Anchor | 64-by-64 | 13-by-13 |
| Trace obstruction used | Five columns | Three columns |
| Host order | (386h+2)2^h | (80h+2)2^h |
| Proven-in-draft distance lower bound | (386h+2)^-2, reproduced | (80h+2)^-2 |
| Exact copy density derived from localization | 2(386h+2)^-132 4^-h | 2(80h+2)^-30 4^-h |
| Machine-check stage in this workspace | Sources audited; no Lean build | Exact finite checks; no Lean proof |

The baseline's exact count in the table is a stronger consequence of
its existing construction than the headline density bound. It was
recalculated, so the candidate is not being compared only against a
weaker abstract. The new contribution proposed here is the smaller
anchor and the all-depth lemma permitting it. The tree propagation,
arbitrary-edit sampling argument and diagonal localization method are
adaptations of the existing work.

The canonical sampler consequence remains exp(Omega(epsilon^-1/2))
sampled positions per axis along the sequence. In the explicit bound,
the exponential denominator changes from 772 to 160. This is not a
new exponent in epsilon and does not apply automatically to other
tester models. An explicit dense host still has n^2 output entries;
the experiment's weighted representation is not an algorithmic
improvement to that output cost.

**Verified finite facts:** all 13-by-13 anchor certificates; 156,576
non-anchor triples; exact mode counts at h=1,...,6 for both anchors;
74,898 threshold cases; 34,952 arbitrary path assignments; exact
sampling marginals; integrity of 78 pinned text sources. These finite
facts support the derivation but do not prove its universal quantifiers.

**Rigorous method limitation:** two-column nonshattering fails already
at depth two. This does not prove minimality of the 15-by-15 pattern.

**Unresolved:** independent scrutiny of the all-depth three-column
lemma and asymmetric rigidity argument; formalization of the new
statement; broader novelty review. No proof gap is presently identified
in the draft, but same-agent inspection is not independent acceptance.
This review package is intended for a private repository. Public release
requires a separate decision; independent review remains pending.

The mathematical artifact is [compressed-pattern.md](proofs/compressed-pattern.md).
Source/model comparisons are in [BASELINE.md](BASELINE.md), executions
in [RUNLOG.md](RUNLOG.md), and the next decisive audit in [HANDOFF.md](HANDOFF.md).
