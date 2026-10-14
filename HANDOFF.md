# Handoff — 3×3 theorem checked in Lean

The October 14 manuscript formatting update adds a title/abstract layout,
consistent mathematical typography, table spacing, bookmarks, and online PDF
links. It also adds a cited background section and seven numbered references
covering the foundational literature and prior repository constructions.
The reviewed mathematical argument and all verification scopes remain
unchanged. Edit `manuscript.md` for text, `references.bib` for bibliographic
metadata, and `tex/preamble.tex` for typography;
regenerate with `python3 scripts/build_manuscript.py --regenerate-tex` and
check synchronization with `--check-tex`. See [RUNLOG.md](RUNLOG.md) for the
executed checks.

The release package contains the current manuscript, exact checks, separate
written-proof review, all Crown Lean sources, source-bound audit and updated
dated chart. The user authorized a PR; no merge or social announcement is
part of this action. See [ANNOUNCEMENT.md](ANNOUNCEMENT.md) for the draft.

The full qualitative theorem is `OrderedRemoval.Crown.no_polynomial_removal_bound`.
It quantifies over arbitrary binary repairs and arbitrarily large hosts at
the same arbitrarily small ε. The written n=(8h+2)m host has exactly 7m⁴
copies; Lean instead uses a padded n=(14h+2)m host and bound 2mn⁴.
That quantitative distinction must remain in future summaries.

Run `python3 scripts/run_checks.py` for finite checks and package integrity.
With the pinned toolchain, run `python3 scripts/run_crown_formal_checks.py`
and `python3 verification/check_crown_formal_model.py --output .context/crown-model-check.json`.
The old 3×4 audit remains independently reproducible with its own script.

Next steps after review and merge: independent mathematical peer review;
optionally formalize the smaller written host and its exact count. Further
pattern-size reductions need a new mathematical argument; no minimality
claim follows from the present work. Worldwide novelty remains a bounded
source search. No author contact or announcement has been performed.
