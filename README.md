# Ordered binary matrix removal

**Private review package · candidate result · October 10, 2026**

This repository proposes reducing the fixed obstruction to polynomial ordered
induced removal from **66×66 to 15×15**. The manuscript contains the complete
written argument and exact finite checks. Independent mathematical review,
formalization, and a conclusive novelty assessment remain pending.

Read the [manuscript PDF](manuscript.pdf), [Markdown manuscript](manuscript.md),
or [LaTeX source](tex/manuscript.tex). Start with [RESULT.md](RESULT.md) for the
precise contribution and [BASELINE.md](BASELINE.md) for the strongest audited
baseline and its assumptions. The host and propagation mechanism adapt
OpenAI's September 25, 2026 construction; [ATTRIBUTION.md](ATTRIBUTION.md)
identifies the inherited and proposed ingredients.

For every integer h ≥ 1, the candidate has order n=(80h+2)2^h, normalized
repair distance at least (80h+2)^−2, and exactly 2·2^(28h) ordered copies.
The density is 2(80h+2)^−30·4^−h. Copies match both binary values and preserve
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
No Lean build or proof of the new theorem is included.

Rebuild the PDF with `pdflatex` (TeX Live and the packages named in the build
script): `python3 scripts/build_manuscript.py`. To regenerate the LaTeX source
from Markdown, install Pandoc 3.6.4 and use `--regenerate-tex`.

## Review

[HANDOFF.md](HANDOFF.md) identifies the decisive all-depth lemma and rigidity
arguments to audit. [ATTEMPT.md](ATTEMPT.md), [RUNLOG.md](RUNLOG.md), and
[verification/README.md](verification/README.md) separate proofs, finite evidence,
and remaining obligations. [results/current.json](results/current.json) is the
machine-readable status. Two-column nonshattering fails; this is a limitation
of the proposed method, not a minimality theorem for the pattern.

Prepared by Ryan Shea with Codex assistance. AI assistance and same-agent
second-pass checking are not independent peer review. Licensed under
[Apache 2.0](LICENSE); see [NOTICE](NOTICE).
