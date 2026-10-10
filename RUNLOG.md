# Reproduction log

## Originating research workspace — 2026-10-10

Python 3.9.25, standard library, exact integer/Fraction/bitset calculations.
The complete proof draft and host implementation were developed in the
open-math-problems #190 track. The source snapshot is pinned by
verification/source_manifest.json; its actual source audit is preserved in
verification/upstream-audit.json. No Lean build was performed.

## Standalone review package

From the repository root:

```sh
python3 scripts/run_checks.py
python3 verification/fetch_upstream.py
python3 verification/check_sources.py
python3 scripts/build_manuscript.py
```

The first command is offline and writes actual run receipts under `.context/`.
The source commands require network access and rehash 78 pinned source files.
PDF builds use three pdflatex passes with shell escape disabled. The checked-in
build receipt binds the Markdown, LaTeX, and PDF by SHA-256. It records actual
tool versions and warnings. Finite reference outputs are committed under
verification/reference/. No numerical check is substituted for the proof.

The exact checks cover 156,576 nonanchor triples through depth 5; mode bodies
through depth 6 for both 13 and 64 anchors; 74,898 threshold cases through
depth 6; 34,952 arbitrary path assignments through depth 4; anchor and sampling
certificates. Two-column nonshattering fails at depth 2.

Independent review, end-to-end formalization, and novelty assessment remain
pending. The initial package was prepared for private review; the repository was
public when the 5×5 update was requested. Candidate status is unchanged.


## 5×5 refinement package — 2026-10-10

That release's proof is `proofs/five-by-five.md`. The 5×5 pattern contains a
3×3 anchor; both manuscript formats, the PDF, and results/current.json
are updated together. The earlier 15×15 proof and exact reports remain.
The initial package is preserved at commit
`fa2aa33105d7d16ae782f4a0858a417e31de9f05`.

`python3 scripts/run_checks.py` now also executes check_refinement.py and
compares its JSON to verification/reference/refinement-report.json.
The expected exact totals are 5,813,724 anchor row triples; 1,567,588 full
pattern row quintuples; 156,576 nonanchor column triples; 28,944 role-support
pairs; 34,952 path assignments; and 74,898 threshold cases. The full H counts
at depths 1,2 are 512 and 131,072. Receipts record the actual successful
executions; no execution is treated as independent mathematical review.

The PDF build receipt also binds the current proof source, and the package
validator checks that the manuscript contains that proof's full statement
and body. The inherited 78-source audit and unchanged upstream pin remain
separate from the offline finite checks.

Actual standalone update validation: all three exact report comparisons
passed; package integrity passed with 38 local links and matching manuscript
artifacts. The PDF built with three pdflatex passes and no warnings.

## 4×4 review PR — 2026-10-10

The user authorized a PR for the 4×4 refinement. No existing PR was found
in this standalone repository. Preparation started from master at
`5aae39b6015677a4fba98e402fa576b22d3b10f9` on branch
`shea256/four-by-four-obstruction`. A fresh GitHub API query confirmed that
openai/math main still matches the pinned upstream commit. The baseline's
previous companion and follow-up audit is retained; novelty remains unresolved.

Copied the 4×4 proof, discovery search, two verification scripts, and exact
reference reports from the originating research track. Typeset the proof's
plain-text mathematical expressions without changing its argument. The
manuscript contains the same statement and proof body, with repository-local
verification links. Updated the README table, result metadata, contribution
history, attribution, and review handoff. Earlier candidates and reports
remain available. Subsequent exploratory 3×3 work is outside this PR.

Actual commands and results, using Python 3.9.25 and the standard library:

```sh
python3 scripts/run_checks.py
python3 scripts/build_manuscript.py --regenerate-tex
python3 scripts/validate_repository.py
git diff --check
```

All five exact reference comparisons passed: compression, adversarial,
refinement, four, and four_repair. The 4×4 census checked 3,693,411 quotient
row quadruples at depths 1–4, with counts 128; 18,944; 1,687,552; and
123,207,680. The closed formula agreed with the separate node-pair sums
through depth 8. All 510 repair-boundary cases passed. Run receipts are
under ignored `.context/checks-receipt.json`.

The first PDF build exposed unsupported Unicode mathematical symbols;
visual inspection also caught malformed math delimiters in the new abstract.
These export issues were corrected before publication. Final conversion
used Pandoc 3.6.4 and three pdflatex passes with shell escape disabled;
the nine-page PDF built with no warnings. Mathematical tables and first-page
formulas were visually checked. The build receipt records all artifact hashes.
After the final typesetting changes, package integrity passed again with
49 local links, matching manuscript hashes, and candidate status. Whitespace
checks passed. No independent mathematical review or Lean build was performed.

## README comparison graphic — 2026-10-10

The user requested a graphic in the style of a supplied scientific step
chart. The 4×4 PR had already been merged, so this change starts from
master commit `a5920eb` on `shea256/pattern-size-graphic`.

Added a reproducible Matplotlib figure showing pattern side lengths
66, 15, 5, and 4, with a zero-based linear vertical axis. The baseline date
is the source manuscript's September 25, 2026 date; all three candidate
drafts are dated October 10, 2026. The horizontal axis explicitly shows
refinement order with equal spacing, not elapsed time. The graphic identifies
the candidate review status and states that hosts can be arbitrarily large.

Rendered `assets/pattern-size-history.png` (2400×1440) and the companion SVG
using `scripts/build_figure.py` with Matplotlib 3.9.4, installed only in an
ignored virtual environment. Matplotlib is optional and does not affect the
standard-library verification suite. The README embeds the PNG, provides
descriptive alternative text, and links both exports and rebuild instructions.

Actual validation: visually inspected the PNG for labels, values, clipping,
and comparison with the reference; parsed the SVG successfully. All five
checks in `python3 scripts/run_checks.py` passed, including deterministic
reference comparisons and package integrity (52 local links and matching
manuscript hashes). `git diff --check` passed. The mathematical result and
its candidate classification are unchanged.
