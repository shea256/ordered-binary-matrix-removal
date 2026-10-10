# Handoff — OPENAI-190

**Current checkpoint:** a complete candidate proof for a fixed **4×4**
ordered binary obstruction, with a 2×2 anchor component. Retain
`Candidate result`: a separate-agent adversarial audit found no material
error, and Lean checks conditional components, but independent peer review
and an end-to-end Lean theorem remain outstanding. The smaller anchor
is not itself rigid.

Start with [four-by-four.md](proofs/four-by-four.md). The earlier
[5×5](proofs/five-by-five.md) and [15×15](proofs/compressed-pattern.md)
drafts remain as research history. The current draft restates its required
host properties and the arbitrary-edit argument.

The [separate-agent review](verification/reviews/four-separate-agent.md)
covers the four issues below. Its verdict is favorable, not independent
peer review. The next implementation step is formalizing the actual host
and deriving the structural and arithmetic hypotheses for arbitrary copies;
see [formal/README.md](formal/README.md). Human reviewers should still inspect:

1. **Full-pattern anchor classification.** Check the complete split by
   counts a,b of selected anchors; crown exclusion, same-class comparability,
   and ordered support containment leave only (2,2) and (2,1). Unit signatures
   alone cannot exclude unintended anchors when the anchor size is two.
2. **Unbalanced copies.** In the (2,1) case check the orientation of the
   second anchor row and first anchor column, all four possible mode types,
   and every column class having a one against row 3. The W− case below the
   leaves crucially uses the parity-mode order. Verify that row 4 must be
   dummy, and the fixed zero (3,4) lies in the leaf-to-parent-minus set T_h.
3. **Exact count.** Audit all four unbalanced families and the factors from
   actual block sizes. The balanced count is 2m^6. The total is 128 at h=1,
   and (33/4)m^6−(29/2)m^5 for h≥2. The h=1 exception is essential; the
   summation uses that m/2 is even only when h≥2. The old leaf-diagonal
   hitting set fails on valid unbalanced copies with no leaf columns.
   The weaker bound N_H≤2mn^6 follows immediately from localization and
   already suffices for failure of polynomial removal; the exact count is
   a separate refinement.
4. **Final theorem and arbitrary repairs.** Designated mode anchors suffice
   for propagation even though other S copies occur. Preserve the protected
   probability 1/m², as opposed to 1/m on shared leaf diagonals. Verify the
   m² edit lower bound, n=(14h+2)m, n^8 density normalization, fixed H and all
   c,C quantifiers. Hitting original copies is not an arbitrary repair bound.

Reproduce the current finite checks offline:

```sh
python3 scripts/run_checks.py
```

Compare parsed JSON with `verification/reference/four-report.json`. The full census
checks every ordered H_4 copy through depth 4 without assuming localization;
a separate node-pair sum checks the closed count through depth 8. The checker
includes a witness for failure of the old hitting set and a nonleaf H copy
when the minus parity modes are reversed. It also reruns the inherited
crown, role-support, path-assignment, and sampling checks. Finite tests and
same-agent proof review do not constitute independent mathematical review.
The suite additionally runs a fresh full-census checker using interval
coordinates, and the separate reviewer's support/unbalanced-copy checker.
The same command also reproduces `verification/reference/four-repair-report.json` and
checks that flipping the zero-cell hitting set creates new designated copies.

No global minimality claim is made. A smaller obstruction would require
its own copy-density and arbitrary-repair arguments; finite pattern searches
alone would not establish it.

Upstream main still matched the audited commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` when rechecked on 2026-10-10.
The original Lean implementation has not been rebuilt. The new Std-only
partial development builds with Lean 4.34.1. Run
`python3 scripts/run_formal_checks.py` from the repository root to build,
audit all 34 theorem dependencies, and replay the imported and local
declarations in a fresh Lean kernel environment. The checked components
do not yet yield a theorem about the concrete host. Keep both
`independent_review` and `new_result_formalized` false.

The previous 5×5 release is preserved at commit
`f16d432d9a918c694f0b404a12f744c0c8b0db03`. The current manuscript, PDF,
and results/current.json describe the 4×4 candidate. All previous proof
drafts and deterministic reference reports remain available.

The 4×4 release and comparison-graphic PRs were merged as `a5920eb` and
`0b8b039` respectively. This audit was prepared locally from `0b8b039` on
`shea256/four-proof-audit`. Its report, additional exact checks, partial
formalization, and manuscript clarifications have not been published.
