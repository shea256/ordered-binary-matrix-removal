# Ordered binary matrix removal

**Candidate research manuscript · October 10, 2026**

This repository proposes reducing the fixed obstruction to polynomial ordered
induced removal from **66×66 to 5×5**. The complete **5×5 forbidden pattern**
contains a **3×3 anchor** plus two additional rows and columns. The manuscript contains the full written
argument and exact finite checks. Independent mathematical review,
formalization, and a conclusive novelty assessment remain pending.

| Construction | Forbidden pattern | Anchor | Status |
| --- | --- | --- | --- |
| [OpenAI baseline](BASELINE.md) | 66×66 | 64×64 | Released manuscript and Lean sources |
| [Our earlier candidate](proofs/compressed-pattern.md) | 15×15 | 13×13 | Proof draft; independent review pending |
| [Our current candidate](proofs/five-by-five.md) | **5×5** | **3×3** | Proof draft; independent review pending |

All three constructions use arbitrarily large host matrices. The anchor is
part of the forbidden pattern. See [IMPROVEMENTS.md](IMPROVEMENTS.md) for
the history of the refinements.

Read the [manuscript PDF](manuscript.pdf), [Markdown manuscript](manuscript.md),
or [LaTeX source](tex/manuscript.tex). Start with [RESULT.md](RESULT.md) for the
precise contribution and [BASELINE.md](BASELINE.md) for the strongest audited
baseline and its assumptions. The host and propagation mechanism adapt
OpenAI's September 25, 2026 construction; [ATTRIBUTION.md](ATTRIBUTION.md)
identifies the inherited and proposed ingredients.

For every integer h ≥ 1, the candidate has order n=(20h+2)2^h, normalized
repair distance at least (20h+2)^−2, and exactly 2·2^(8h) ordered copies.
The density is 2(20h+2)^−10·4^−h. Copies match both binary values and preserve
separate row and column orders. Repairs allow arbitrary binary changes.
The pattern is fixed independently of h. Finite tests support the argument;
they do not prove its universal quantifiers.

## Reproduce the checks

Python 3.9 or newer; standard library only:

```sh
python3 scripts/run_checks.py
```

This regenerates exact reports, compares them to checked-in references, and
validates repository artifacts. Receipts go to ignored `.context/` files.
For optional network source verification:

```sh
python3 verification/fetch_upstream.py
python3 verification/check_sources.py
```

The 78-file source cache is ignored. Offline checks validate manifest metadata,
not downloaded source bytes. The original source audit is preserved separately.
No Lean build or formal proof of the new theorem is included.

Rebuild the PDF with `pdflatex` (TeX Live and the packages named in the build
script): `python3 scripts/build_manuscript.py`. To regenerate the LaTeX source
from Markdown, install Pandoc 3.6.4 and use `--regenerate-tex`.

## Review

[HANDOFF.md](HANDOFF.md) identifies the decisive all-depth lemma and rigidity
arguments to audit. [ATTEMPT.md](ATTEMPT.md), [RUNLOG.md](RUNLOG.md), and
[verification/README.md](verification/README.md) separate proofs, finite evidence,
and remaining obligations. [results/current.json](results/current.json) is the
machine-readable status. All binary 2×2 patterns occur in the nonanchor host,
blocking a further reduction by the same pure-anchor rigidity method. This does not prove
that a 5×5 obstruction is minimal.

The earlier 15×15 candidate used a 13×13 anchor. Its
[proof draft](proofs/compressed-pattern.md) and exact reports are retained;
the original manuscript is available at the
[initial commit](https://github.com/shea256/ordered-binary-matrix-removal/tree/fa2aa33105d7d16ae782f4a0858a417e31de9f05).
The new [proof](proofs/five-by-five.md) uses a different order of the anchor
blocks to make the smaller anchor rigid. See [IMPROVEMENTS.md](IMPROVEMENTS.md).

Prepared by Ryan Shea with Codex assistance. AI assistance and same-agent
second-pass checking are not independent peer review. Licensed under
[Apache 2.0](LICENSE); see [NOTICE](NOTICE).
