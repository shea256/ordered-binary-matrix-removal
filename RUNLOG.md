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
pending. This repository is a private review package, not a public release.
