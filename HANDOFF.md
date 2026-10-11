# Handoff — 3×4 theorem checked in Lean

The pattern is `1001/1010/0111`. For h≥1, its explicit square host has
n=(14h+2)2^h, repair cost at least m², and at most 2mn⁵ copies.
The full quantified no-polynomial-bound theorem is checked in Lean.
See [formal/README.md](formal/README.md) and the
[audit](verification/reference/rectangular-formal-audit.json).

The user-authorized draft PR contains the written proof, Lean sources,
exact checks, manuscript and source-bound audit. The separate agent's
[semantic review](verification/reviews/three-by-four-formal.md) is distinct
from independent mathematical peer review, which remains pending.
The announcement has not been posted and the PR has not been merged.

Next: review the draft PR and seek independent mathematical review before
release. Keep the result classified as candidate under this repository's
review policy. This is 3×4, with no 3×3, minimality, exact repair equality,
or exact all-depth enumeration claim. Preserve Erebos's H4 priority credit.

Reproduce with `python3 scripts/run_checks.py` and, with the pinned toolchain,
`python3 scripts/run_rectangular_formal_checks.py`. The audit checks all
project declarations and replays each module into its imported environment;
it does not freshly replay all Mathlib. Both the historic H4 audit and its
source files remain intact.

## Previous checkpoint record

# Handoff — optimized order and corrected prior work

Current result: a written quantitative refinement of the known H4 obstruction,
with candidate status pending independent mathematical review. See
[proofs/optimized-order.md](proofs/optimized-order.md), [RESULT.md](RESULT.md),
and [BASELINE.md](BASELINE.md). The pattern-size priority claim is withdrawn.

The new exact count is (5/2)m⁶−m⁵ for all h≥1; Erebos gives
(41m⁶−74m⁵)/4 for h≥2. Both have n=(14h+2)m and exact repair cost m².
The ratio tends to 10/41; 75.6% is an asymptotic reduction. The new count is
optimal only over the specified intact-mode-block permutation class.

Next decisive work:

1. Independent mathematical review of the new all-depth count, the repair transfer,
   and the precise restricted optimality class. A separate AI review is not peer review.
2. Adapt Lean's `Concrete.modeRank` and its order-dependent lemmas to the new global
   order, then formally connect exact enumeration and repair equality to that host.
   Current Lean sources still represent the previous order. Do not describe the new
   comparison as machine checked merely because the same H already has a Lean proof.
3. Continue primary-source novelty screening beyond the located Erebos and ProveIt
   sources. Any further pattern reduction needs a new all-copy and arbitrary-repair proof.

Reproduce the exact checks with `python3 scripts/run_checks.py`. The manuscript
PDF is built from the new proof; metadata explicitly separates its scope from
`results/previous-four.json` and the preserved source-bound formal audit.
`ANNOUNCEMENT.md` is a draft, not a published announcement. No contact with authors
or external publication was performed during this refinement.
