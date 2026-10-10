# Partial Lean formalization of the 4×4 argument

**Status: partial.** These files prove 34 helper theorems in Lean 4.34.1
using only Std. They do not define the complete ordered host or prove the
4×4 removal theorem. The result remains a candidate.

From the repository root, with the pinned Lean/Lake toolchain available:

```sh
python3 scripts/run_formal_checks.py
```

The script builds the project, prints and checks the axioms of every exported
theorem, and runs `leanchecker --fresh OrderedRemoval` to replay the imported
and new declarations in a fresh Lean kernel environment. Only `propext`,
`Quot.sound`, and `Classical.choice` are permitted in the dependency audit.
No added axioms or admitted proofs are used. Kernel replay uses Lean itself;
it is not verification by a different proof assistant or human peer review.
The source hashes and actual results go to `.context/formal-checks-receipt.json`.
The archived run is [formal-audit.json](../verification/reference/formal-audit.json).

## What is proved

| Module | Universal statement checked | Main remaining connection |
| --- | --- | --- |
| [AnchorClassification](OrderedRemoval/AnchorClassification.lean) | Explicit order, crown-exclusion, comparability, and containment hypotheses force anchor counts (2,2) or (2,1). H has distinct rows and columns. | Extract the `Certificate` from every actual host copy, including exclusion of duplicate twin blocks. |
| [LocalArithmetic](OrderedRemoval/LocalArithmetic.lean) | All balanced and unbalanced threshold contradictions; equality of the terminal parent indices; the parity-order lemma and last-row exclusions. | Show every actual copy supplies one of the exhaustive case hypotheses, using the concrete tree order and role table. |
| [Propagation](OrderedRemoval/Propagation.lean) | For arbitrary Boolean sequences and arbitrary depth, opposite root bits and a shared terminal bit force one of the four P bodies. | Extract the sequences and show the body extends to an ordered H copy when protected entries are unchanged. |
| [ProtectedSampling](OrderedRemoval/ProtectedSampling.lean) | An integer union bound produces an untouched sample under an incidence-frequency budget; combining this with arbitrary-bit propagation forces a P body. | Construct the concrete sampler, prove its incidence bound, and supply the protected host entries. |

These are unbounded mathematical theorems, rather than depth-limited
computations. Their hypotheses are part of their statements. In particular,
`Certificate` is a structure of assumptions; defining it does not prove
those assumptions for the host.

The files also contain an arithmetic counterexample to dropping the minus
parity-order hypothesis. It explains why that hypothesis is substantive.
The fresh [literal checker](../verification/check_four_literal.py) separately
exhibits full nonlocalized host copies after reversing those modes.

## The alternate three-seed sampler

The paper chooses many representatives independently conditional on a leaf.
Its probability space has more than `m³` outcomes. For the optional smaller
finite parameterization, take independent uniform `z,u,v∈{0,...,m−1}`.
Choose leaf z. In each ancestor block of size w on the row axis select
offset `u mod w`; on the column axis use `v mod w`. Select offset u in every
size-m row anchor/dummy block and offset v in every column anchor/dummy
block. A shared leaf has w=1. This reuses offsets within an axis.

For a variable position in a size-w block, there are w possible leaves z
and m/w offsets giving the specified residue. Opposite anchor/dummy
coordinates fix the other axis's offset. Each protected variable-to-anchor
or variable-to-dummy cell therefore has exactly m preimages out of m³.
For cells with both endpoints anchor/dummy, or both root positions, the
two offsets are fixed and the leaf is free: again m preimages. Thus all
protected cell probabilities are 1/m². A diagonal leaf cell has m²
preimages and probability 1/m, and is deliberately unprotected.

The correlations within an axis do not matter for the union bound or path
propagation. This is an alternate sampler with the same needed marginals,
not a claim that the paper's independent sampler has m³ outcomes.
The literal checker exhausts these frequencies through h=3.
The preceding all-depth counting justification is **written mathematics**;
the construction and incidence extraction are not yet Lean theorems.

## Next formalization steps

1. Define actual positions, block sizes, the two strict axis orders, roles,
   binary entries, and ordered H embeddings. Prove leaf identification and
   twin exclusion using those definitions.
2. Prove the concrete crown, comparability, and ordered-support properties,
   then construct `AnchorClassification.Certificate` from an arbitrary
   embedding.
3. Extract the balanced and unbalanced arithmetic cases and establish the
   full zero-cell localization theorem for every h≥1.
4. Connect protected sampling and designated body extension to arbitrary
   edited matrices, yielding at least m² edits.
5. Prove the copy bound and the final real-valued, every-c,C conclusion.
   The coarse bound `2mn⁶` already suffices; exact enumeration can follow.

The parent audit's [proof map](../verification/reviews/four-assurance.md)
separates these gaps from the completed written review.
