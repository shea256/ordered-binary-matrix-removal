# Handoff — OPENAI-190

**Current checkpoint:** complete candidate proof and exact checks for a
15-by-15 fixed ordered binary obstruction. Keep the catalog at
`Candidate result` until the mathematical claims receive independent
verification; do not interpret the finite checks as universal proof.

The next decisive step is an independent adversarial review of
[compressed-pattern.md](proofs/compressed-pattern.md), especially:

1. The three-column lemma: after same-class monotonicity, every pair
   of a shattered three-class set must be supported by a variable row.
   Check the unique terminal triangle and the nested leaf thresholds,
   including h=1 and repeated column nodes.
2. The anchor rigidity argument: the word rectangle starts at row 6,
   overlapping the dense six-row prefix at its all-zero word. Check
   both axes separately. The initial alternative is at least six
   anchor rows **or** at least eleven anchor columns, not a symmetric
   half-size split. Prefix density five must strictly exceed four.
3. Repair distance: root/anchor/dummy selection probabilities are
   exactly 1/m^2; intermediate variable entries are unprotected and
   arbitrary; shared leaves are correlated. All edit directions and
   changes to anchor blocks must be included.
4. Exact count: only W_{h,d}^- leaf bodies survive, with b=floor(p/2),
   exactly two parent column positions, m dummy row choices and no
   duplicated embeddings across modes.

The published 66-by-66 implementation is at
`verification/upstream/lean/OAI/Combinatorics/MatrixRemoval/`; Main
imports the copy-count and arbitrary-repair bounds. Its comparator is
a statement template with `sorry`, not the solution. A future formal
review should first rebuild the baseline on pinned Lean 4.34.1/Mathlib,
then parameterize the host and prove the three-column lemma and
13-by-13 prefix conditions. Do not replace every occurrence of 64
with 13: the old dense-prefix identities and word rectangle change.

The new theorem needs separate formal definitions of S_13, H_15,
ordered copies, arbitrary binary edit distance and the constructed
sequence. The final statement must quantify all c,C>0 and permit
n,epsilon,A to depend on them while fixing H_15. No silent reliance
on unlimited host labels or a ternary symbol is allowed.

The two-column attack is decisively blocked for this host by an actual
shattered pair. A smaller pattern may still be possible through a
different anchor. There is no minimal-pattern theorem here.

Novelty screening found no direct stronger primary result or correction,
but does not establish novelty. Check any further manuscript versions,
reviews or unpublished refinements before claiming acceptance. The
exact 4^-h density decay is already derivable for the baseline and
must not be presented as a wholly new lower-bound mechanism.

Reproduce the checks with the commands in [RUNLOG.md](RUNLOG.md). All
experiments use standard-library exact arithmetic; no paid tooling is
required. Do not publish or contact authors without authorization.
