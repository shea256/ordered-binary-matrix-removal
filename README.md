# Ordered binary matrix removal

**Candidate research manuscript · October 11, 2026**

This repository proposes reducing the fixed obstruction to polynomial ordered
induced removal from **66×66 to 4×4**, refining our earlier 15×15 and 5×5
candidates. The complete **4×4 forbidden pattern** contains a **2×2 anchor
component** plus two additional rows and columns. The manuscript contains
the full written argument and exact finite checks. Independent mathematical
review and a conclusive novelty assessment remain pending.

A [separate-agent adversarial review](verification/reviews/four-separate-agent.md)
found no material error in the written argument. Additional exact checkers
and a [Lean development](formal/README.md) are included. Lean now proves the
qualitative 4×4 removal theorem end to end: the concrete copy bound, arbitrary
binary repair bound, and conclusion for every positive c,C. It uses the
sufficient coarse count `N_H≤2mn⁶`; the sharper exact copy formula and canonical
sampler bound remain outside the formal certificate. The result retains
candidate status pending independent mathematical review.

![Forbidden pattern sizes decrease from OpenAI's 66×66 baseline to candidate patterns of 15×15, 5×5, and 4×4. The vertical axis is the pattern side length; stages show refinement order, not elapsed time. Independent mathematical review of the candidates remains pending.](assets/pattern-size-history.png)

| Construction | Forbidden pattern | Anchor component | Status |
| --- | --- | --- | --- |
| [OpenAI baseline](BASELINE.md) | 66×66 | 64×64 | Released manuscript and Lean sources |
| [First candidate](proofs/compressed-pattern.md) | 15×15 | 13×13 | Proof draft; independent review pending |
| [Previous candidate](proofs/five-by-five.md) | 5×5 | 3×3 | Proof draft; independent review pending |
| [Current candidate](proofs/four-by-four.md) | **4×4** | **2×2** | Qualitative theorem checked in Lean; independent review pending |

All four constructions use arbitrarily large host matrices. The anchor is
part of the forbidden pattern. See [IMPROVEMENTS.md](IMPROVEMENTS.md) for
the history of the refinements.

Read the [manuscript PDF](manuscript.pdf), [Markdown manuscript](manuscript.md),
or [LaTeX source](tex/manuscript.tex). Start with [RESULT.md](RESULT.md) for the
precise contribution and [BASELINE.md](BASELINE.md) for the strongest audited
baseline and its assumptions. The host and propagation mechanism adapt
OpenAI's September 25, 2026 construction; [ATTRIBUTION.md](ATTRIBUTION.md)
identifies the inherited and proposed ingredients.

The fixed forbidden pattern is:

```text
0 1 1 0
1 0 0 1
1 0 1 0
0 1 1 1
```

For every integer h ≥ 1, put m=2^h. The candidate host has order
n=(14h+2)m and normalized repair distance at least (14h+2)^−2. Its exact
copy count is 128 at h=1 and (33/4)m^6−(29/2)m^5 for h≥2. Thus its copy
density is at most (33/4)(14h+2)^−8·4^−h, smaller than every fixed power
of the certified distance scale as h grows.

Copies match both binary values and preserve separate row and column
orders. Repairs allow arbitrary binary changes, including anchor cells.
The pattern is fixed independently of h. The new proof permits additional
anchor configurations and localizes every complete 4×4 copy to one of 2m
specific zero cells. Finite tests support the argument; they do not prove
its universal quantifiers. The Lean certificate proves the qualitative
conclusion using copy density at most `2(14h+2)⁻²2⁻ʰ`.

## Reproduce the checks

Python 3.9 or newer; standard library only:

```sh
python3 scripts/run_checks.py
```

This regenerates exact reports, compares them to checked-in references, and
validates repository artifacts. Receipts go to ignored `.context/` files.
The 4×4 census checks all copies through depth 4 without assuming the
localization theorem, and the separate count calculation runs through
depth 8. A fresh literal implementation repeats the full census and negative
controls, and the separate reviewer's checker examines unbalanced copies
through depth 7. The suite retains the earlier candidates' checks.

For optional network source verification:

```sh
python3 verification/fetch_upstream.py
python3 verification/check_sources.py
```

The 78-file source cache is ignored. Offline checks validate manifest metadata,
not downloaded source bytes. The original source audit is preserved separately.
The original upstream Lean formalization has not been rebuilt here.
For the Lean development, install the pinned Lean 4.34.1 toolchain,
fetch the pinned Mathlib cache with `(cd formal && lake exe cache get)`,
and run `python3 scripts/run_formal_checks.py`. This audits the project
axiom dependencies and replays each local module in Lean's kernel.
The actual host, coarse copy bound, arbitrary-repair lower bound, and final
every-c,C theorem are checked. Exact enumeration remains open. See
[formalization coverage](formal/README.md) and the
[final Lean theorem](formal/OrderedRemoval/Main.lean).

Rebuild the PDF with `pdflatex` (TeX Live and the packages named in the build
script): `python3 scripts/build_manuscript.py`. To regenerate the LaTeX source
from Markdown, install Pandoc 3.6.4 and use `--regenerate-tex`.

The comparison graphic is available as [PNG](assets/pattern-size-history.png)
and [SVG](assets/pattern-size-history.svg). To rebuild it, install the optional
plotting dependency `matplotlib==3.9.4` and run
`python3 scripts/build_figure.py`. The exact verification suite uses only
the Python standard library.

## Review

[HANDOFF.md](HANDOFF.md) identifies the full-pattern classification,
zero-cell localization, copy count, and arbitrary-repair argument to audit.
[ATTEMPT.md](ATTEMPT.md), [RUNLOG.md](RUNLOG.md), and
[verification/README.md](verification/README.md) separate proofs, finite
evidence, and remaining obligations. [results/current.json](results/current.json)
is the machine-readable status. No claim that 4×4 is minimal is made.

The earlier [15×15](proofs/compressed-pattern.md) and
[5×5](proofs/five-by-five.md) drafts and exact reports are retained. The
previous 5×5 manuscript is available at its
[release commit](https://github.com/shea256/ordered-binary-matrix-removal/tree/f16d432d9a918c694f0b404a12f744c0c8b0db03).

Prepared by Ryan Shea with Codex assistance. AI assistance, same-agent checks,
and separate-agent review are not independent peer review. Licensed under
[Apache 2.0](LICENSE); see [NOTICE](NOTICE).
