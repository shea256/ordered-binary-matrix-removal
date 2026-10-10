# Handoff — OPENAI-190

**Current checkpoint:** a complete candidate proof for a fixed **5×5**
ordered binary obstruction, using a 3×3 anchor. Retain `Candidate result`:
no independent reviewer or Lean kernel has verified the new theorem.

Start with [five-by-five.md](proofs/five-by-five.md). The earlier
[15×15 draft](proofs/compressed-pattern.md) is retained as history, not a
proven premise. The new draft restates the host and arbitrary-edit argument.

The next decisive step is independent adversarial review of:

1. **Nonanchor crown exclusion.** Only the three weight-two words are
   needed. Verify same-class comparability, the unique terminal class
   triangle, nested leaf traces, and the h=1 shared-leaf boundary.
2. **Ordered laminar supports.** Every role is a whole class or parity
   half. All strict containers must occur later on both axes. The mode
   order is W+0,W+1,W−0,W−1,V+,V− within each increasing depth. Reverting
   to V-before-W produces an unintended anchor copy at h=2.
3. **3×3 rigidity.** Audit all cases for the counts a,b of selected
   anchor positions. For a,b≥2, aligned mode order forces the crossed
   anchor incidences into one mode. For one count≥2 and the other≤1,
   proper containment would run backward. For a,b≤1, same-class
   comparability or crown exclusion gives the contradiction.
4. **Final theorem.** Unit signatures must exclude all other anchors;
   original body localization and arbitrary-repair sampling must still
   apply after reordering. Verify n=(20h+2)2^h, count 2·2^(8h), and the
   all-c,C asymptotic implication with n^10 normalization. Preserve the
   distinction between protected probabilities 1/m² and leaf probability
   1/m. Do not replace arbitrary repair distance by original-copy hitting.

Reproduce all new finite checks offline:

```sh
python3 scripts/run_checks.py
```

Compare parsed JSON with `verification/reference/refinement-report.json`. The checker
searches every ordered S_3 copy through depth 6 and every ordered H_5 copy
through depth 2, with exact twin-block weights. It checks role supports
against a separate descriptor table, and reruns the existing exact path
and sampling checks. These are same-agent checks, not independent review.

For further compression, the direct 2×2 anchor route is blocked in this
host: all 16 patterns already occur among nonanchors at depth 2. A 4×4
obstruction might require a different host, a different enforcement
mechanism, or a proof that does not require pure-anchor rigidity. No
universal lower bound of 5 is claimed.

Upstream main still matched the audited commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` when rechecked on 2026-10-10.
The original Lean implementation has not been rebuilt. Formalization of
the new construction must include the changed mode order and new rigidity
lemma; changing constants in the old formalization is insufficient.

The earlier 15×15 package is preserved at commit
`fa2aa33105d7d16ae782f4a0858a417e31de9f05` and in the retained earlier proof.
The current manuscript and `results/current.json` describe the 5×5 candidate.
Run `python3 scripts/run_checks.py` for the complete offline verification
and package-integrity checks.
