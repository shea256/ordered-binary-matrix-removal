# Handoff — OPENAI-190

**Current checkpoint:** the qualitative obstruction for the fixed **4×4**
ordered binary pattern is formalized end to end. The result remains
`Candidate result` pending independent mathematical review and conclusive
novelty assessment. This checkpoint changes verification coverage, not the
pattern size or the written theorem.

Start with [Main.lean](formal/OrderedRemoval/Main.lean),
[formal coverage](formal/README.md), and the [manuscript](proofs/four-by-four.md).
The capstone `OrderedRemoval.no_polynomial_removal_bound` quantifies over every
positive real c,C. Its explicit arbitrary-repairs variant quantifies over every
H4-free binary B. No anchor-preservation, localization, sampling, or host-existence
hypothesis remains. [DistanceMeaning](formal/OrderedRemoval/DistanceMeaning.lean)
proves that the finite minimum is attained by an actual repair.

The proof combines bounds for the **same actual host**: for h≥1, m=2^h and
n=(14h+2)m, every repair changes at least m² entries and the copy count is at
most 2mn⁶. The normalized density is at most 2(14h+2)⁻²2⁻ʰ, sufficient to defeat
every polynomial in the distance scale (14h+2)⁻². The factor two is essential
to this coarse localization argument and is retained throughout.

## Next decisive work

1. Obtain independent mathematical review, especially of the correspondence
   between the literal H4, independent axis orders, unrestricted repairs,
   manuscript, and formal capstone. The favorable
   [separate-agent review](verification/reviews/four-removal.md) is not peer review.
2. Formalize the sharper exact count: 128 for h=1 and
   (33/4)m⁶−(29/2)m⁵ for h≥2. This refines the certified density rate beyond
   the coarse bound; the h=1 exception must be preserved.
3. Formalize the canonical sampler consequence separately, including its
   quantifiers. It does not establish a bound for every adaptive tester.
4. Finish novelty screening against primary literature. No global minimality
   claim for 4×4 is made. A smaller pattern needs its own copy-density and
   arbitrary-repair arguments.

The exact equality |T_h|=2m for positive h is also outside the certificate;
the checked upper bound suffices for the capstone. Historical 15×15 and 5×5
proofs and reports are retained. The two-by-two anchor itself is not rigid;
the full-pattern classification permits both (2,2) and (2,1) anchor counts.

## Reproduce and interpret verification

```sh
python3 scripts/run_formal_checks.py
python3 scripts/run_checks.py
```

The first command requires pinned Lean 4.34.1 and the Mathlib cache, audits
all project declarations for transitive axioms, and replays each local module
into its imported Lean environment. It is not fresh replay of all Mathlib.
The second runs nine exact Python checkers and validates the source-bound
audit receipt and manuscript artifacts. Finite tests are not universal proofs.
See [RUNLOG.md](RUNLOG.md) for actual outputs and
[verification/README.md](verification/README.md) for evidence scope.

The new reviewer checker independently reconstructs all m³ sampled paths for
h=1..4, checks each protected zero and one, and confirms maximum guard frequency
m. An unprotected common-leaf diagonal has frequency m², a useful negative control.
Neither the script nor a finite original-copy hitting set proves arbitrary-repair
hardness; the guarded-path Lean chain supplies that proof.

Upstream main still matched `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` on
2026-10-11. The original full upstream Lean implementation has not been rebuilt.
Selected sampling, guarded-path, normalization, and analytic modules were adapted
with attribution. Their methods are inherited, not new contributions.

Keep `independent_review` false and `status` candidate. The qualitative
`new_result_formalized` flag is true; exact enumeration and the canonical sampler
flags remain false. The explicit coverage fields in
[results/current.json](results/current.json) distinguish those statements.

The localization checkpoint was merged in
[PR #4](https://github.com/shea256/ordered-binary-matrix-removal/pull/4),
commit `6e7711ffdc51280ff8b9c882a77c3af2982ddaa2`. This checkpoint builds on it.
