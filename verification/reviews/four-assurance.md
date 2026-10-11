# 4×4 assurance checkpoint — 2026-10-10

**Outcome:** the separate reviewer found no material error, omitted case,
or incorrect count in the complete written argument. Two separately written
checkers reproduce its finite predictions. The Lean development now constructs the actual host and proves its
all-depth anchor classification and zero-cell localization, as well as the
dummy last row and zero-set size bound. Copy counting and repair connections
remain open.
The pattern remains **4×4** and the result remains **candidate**.
This checkpoint adds verification evidence, not a smaller obstruction or a
new mathematical theorem. Separate-agent review is not independent peer review.

The baseline remains OpenAI's September 25, 2026 manuscript at commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Both agents rechecked that upstream
main still matched it. Searches did not identify a newer direct primary
follow-up; novelty is unresolved. The strongest derived baseline density,
the binary model, arbitrary repairs, and all quantifiers are unchanged.
See [BASELINE.md](../../BASELINE.md).

## Executed attacks and evidence

| Attack | Result | Evidence |
| --- | --- | --- |
| Find a missing anchor-count case, nonleaf unbalanced copy, or wrong multiplicity. | Separate reviewer reconstructed all 25 anchor-count cases, both localization branches, all four unbalanced families, and the h=1 exception. No material gap found. | [Separate-agent report](four-separate-agent.md); [checker](../check_four_reviewer.py); [output through h=7](../reference/four-reviewer-report.json). |
| Expose a shared bug in the existing host code or a false localization assumption. | A fresh interval-endpoint construction and ordered-column dynamic program reproduce the full counts at h=1,...,4. The actual 32×32 matrix at h=1 was also expanded and checked. Neither implementation imports the existing host. | [Literal checker](../check_four_literal.py); [output](../reference/four-literal-report.json). |
| Break arbitrary repair by editing anchors, exploiting correlated leaves, or destroying only old copies. | Reviewer reconstructed the protected-cell union bound and arbitrary-bit propagation. A compact alternate sampler passed exact marginal checks; the zero-set flip creates 256 new copies at h=1. | Reviewer repair section; literal negative controls; [partial Lean coverage](../../formal/README.md). |

The literal census reproduces copy totals 128; 18,944; 1,687,552; and
123,207,680, with no violations of the zero-cell or dummy-last-row claims.
It visits 3,693,411 quotient row quadruples, plus 35,960 actual row quadruples
in the expanded h=1 check. Distinct rows and columns of H justify using
at most one representative of each twin block in the quotient check.

At h=3, reversing the two minus parity modes produces 131,072 copies
outside the prescribed zero set. Flipping that set at h=1 produces 256
copies outside it, all with a nondummy last row. These negative controls
show that the checker can detect failures of the properties being audited.

The reviewer suggested only clarifications: same-mode anchor group order;
the parent-half family's zero contribution at h=2; and uniform q-subsets
for the canonical sampler. The proof and manuscript incorporate those
clarifications without changing a mathematical claim.

## Proof map and exact formal boundary

`crown exclusion + comparability + ordered supports`
→ `anchor counts (2,2) or (2,1)`
→ `fixed zero lies in T_h, |T_h|=2m`
→ `N_H≤2mn⁶`.

Separately:
`protected incidence probability 1/m²`
→ `clean sample for fewer than m² edits`
→ `four arbitrary-bit implications`
→ `contradictory shared leaf`
→ `dist_H≥(14h+2)⁻²`.

The coarse density bound is `2(14h+2)⁻²2⁻ʰ`. Dividing it by
`epsilon_h^C` gives `2(14h+2)^(2C−2)2⁻ʰ→0` for every fixed C>0,
already proving the qualitative implication in the written argument.
The exact enumeration strengthens the bound to
`(33/4)(14h+2)⁻⁸4⁻ʰ`. Neither count is a replacement for the edit lower bound.

Lean now defines the concrete host and its independent axis orders, proves
crown exclusion and ordered support containment, extracts the certificate
from every actual copy, and proves anchor counts (2,2) or (2,1). The indexed
matrix theorem assumes only increasing row/column maps and the sixteen H4
entries. Height-zero exclusion and a height-one witness are also checked.
The [concrete-host review](four-concrete-host.md) found no semantic error.

The [localization review](four-localization.md) checks the common-frame
argument for both anchor configurations. Lean now extracts its role, entry,
and order hypotheses from every actual copy, proves localization and the
dummy last row, and injects the zero set into leaves × parity bits to prove
`|T_h|≤2m`. Exact equality and the final copy-count inequality are not yet
formalized.

The inherited three-seed mixer and fiber counts are now formalized, but concrete
protected-cell incidence extraction and designated-body extension to arbitrary
edited matrices are not. The finite union bound and all-depth Boolean
propagation remain checked components. The full removal theorem is therefore
not yet formalized. The original full upstream development has not been rebuilt.

The [formal README](../../formal/README.md) gives the build command,
all remaining interfaces, and the inherited three-seed sampler's exact
provenance and coverage. The [archived formal audit](../reference/formal-audit.json)
records the actual theorem dependencies and source hashes.

## Next decisive step

Derive the coarse copy count from the checked localization and zero-set
size bound. Then connect designated body extension, protected incidence
counts, arbitrary repairs, and final quantifiers. Keep `new_result_formalized=false`. Human independent
review and novelty assessment are separate outstanding tasks. The earlier
3×3 construction limitations remain in the originating research track.
