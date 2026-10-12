# Current result — candidate 3×3 crown obstruction

The fixed pattern `011/101/110` admits no polynomial ordered binary matrix
removal bound. It has nine entries, compared with twelve in our previous
3×4 result and sixteen in the located external 4×4 results.

For every c,C,ε₀>0, some fixed 0<ε<ε₀ has the following property: for every
N there are n≥max(1,N) and a binary n×n host requiring at least εn² edits
in every crown-free repair and containing fewer than c ε^C n⁶ ordered copies.
All nine labels and separate increasing axis maps are required; edits in
both directions and anywhere in the host are allowed.

| Claim | Verification |
| --- | --- |
| Full qualitative theorem and quantifier order | Lean build, axiom audit and local-module kernel replay |
| Written host n=(8h+2)m, exact count 7m⁴, repair at least m² | Written all-depth argument, finite checks, separate-agent written review |
| Formal host n=(14h+2)m, copies at most 2mn⁴, repair at least m² | Lean; anchors have size 2m on each axis |
| Actual formal host and axis definitions match intended padded model | Same-agent executed Lean/Python check through h=3 |
| Human mathematical peer review, worldwide priority, minimality | Pending / not claimed |

The paper and [formal scope](formal/README.md) explicitly distinguish these
two host families. The exact 7m⁴ count and more economical host are not
certified by Lean. No all-depth exact repair equality is claimed.

The audit checks 573 named theorems and 2,163 declarations over 92 modules;
19 modules, 88 named theorems and 257 declarations belong to the new Crown
development. The only allowed transitive axioms are `propext`, `Quot.sound`,
and `Classical.choice`. Each project module was replayed into its imported
environment; this is not a fresh replay of Mathlib.

The [separate reviewer](verification/reviews/three-by-three-adversarial.md)
found no gap in the original written proof and did not review the Lean port.
The original proof and finite-discovery receipt remain unchanged snapshots;
their older verification flags are superseded by the current metadata and
[formal audit](verification/reference/crown-formal-audit.json).

Candidate classification is retained pending independent mathematical review.
The baseline credits OpenAI, ProveIt, Erebos Labs and Zinan Wang; see
[BASELINE.md](BASELINE.md). Older 3×4 and 4×4 results remain in `results/`.
