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

## Separate-agent audit and partial Lean formalization — 2026-10-10

The user confirmed the 4×4 and graphic merges. PR #2 was verified merged
as `0b8b039`. This work starts from that commit on local branch
`shea256/four-proof-audit`. The user explicitly authorized a separate
reviewer; it received a fresh task context and wrote a detailed report
and separate support/unbalanced-copy checker. No model override was set.
The report found no material error, missing case, or incorrect count.
This is a separate-agent audit, not independent mathematical peer review.

Rechecked upstream main and title/correction/smaller-pattern searches.
The source pin remained `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
No stronger direct primary follow-up was found; novelty remains unresolved.

The coordinating agent wrote `verification/check_four_literal.py` without
research-code imports, using sorted tree-interval endpoints and a column
dynamic program. It reproduced all copy totals through h=4 and the
expanded 32×32 h=1 host. Its exact alternate three-seed sampler check
covered h=1,2,3. Reversing minus modes gave 131,072 nonlocalized copies
at h=3; flipping the original zero set produced 256 new copies at h=1.
The reviewer separately checked supports and unbalanced copies through h=7.
Its script's runtime-version output field was removed for portable JSON
comparison; the mathematics and checked cases were unchanged.

Installed the official Lean 4.34.1 release binary in the ignored workspace
cache, commit `5045d0056413266e57c625dcd7c365b10e377c52`. The initial extraction
needed the system zstd package. That initial formal checkpoint used Std and had no
third-party packages. The original 61-module upstream development was
not rebuilt. Initial compilation caught unfolding/decidability and tactic
syntax issues; these were corrected before the successful build.

Actual commands, with the pinned Lean/Lake and Pandoc binaries on PATH:

```sh
python3 scripts/run_formal_checks.py
python3 scripts/run_checks.py
python3 scripts/build_manuscript.py --regenerate-tex
python3 scripts/validate_repository.py
git diff --check
```

The formal build succeeded. All 34 exported helper theorems passed the
dependency audit, using only `propext`, `Quot.sound`, and `Classical.choice`.
`leanchecker --fresh OrderedRemoval` replayed imported and new declarations
successfully in a fresh Lean kernel environment. Its exact source hashes
were archived in the initial `verification/reference/formal-audit.json`
(now superseded by the concrete-host audit; the old receipt remains in git
commit `6fa94c55c3763cef8a719846d7c37591eb093d9a`). No claim of a
formalized concrete host or final removal theorem follows from these
conditional statements. The three-seed sampler differs from the paper's
independent representative sampler; its incidence extraction is unformalized.

All seven exact checks and deterministic reference comparisons passed on
Python 3.9.25: compression, adversarial, refinement, four, four_repair,
four_literal, and four_reviewer. The recorded elapsed times were 1.585,
3.186, 9.181, 3.818, 0.684, 4.544, and 0.622 seconds respectively, under
this run's shared machine load; these are execution records, not benchmarks.
Package integrity passed with 93 local links and matching manuscript hashes.
After the reviewer's three wording clarifications and verification update,
Pandoc 3.6.4 and three pdflatex passes produced a nine-page PDF with no
warnings. The theorem statement is unchanged.

The audit report, new exact scripts/references, and partial formal project
were mirrored into the originating open-math-problems track. The catalog
keeps Candidate result and records the next concrete host formalization
checkpoint. No commit, push, PR, author contact, or paid action had been made
at that initial local checkpoint. The subsequent PR is recorded below.

## Concrete host and anchor classification — 2026-10-10

After the user's instruction to proceed, committed the initial audit as
`6fa94c55c3763cef8a719846d7c37591eb093d9a`, pushed branch
`shea256/four-proof-audit`, and opened
[PR #3](https://github.com/shea256/ordered-binary-matrix-removal/pull/3)
against master. The upstream main commit was rechecked and still matched
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

Added Mathlib at exact commit `d13f23b723b8a846827a245b89c10fc7d3f11612`
and its locked dependencies with `lake update mathlib`. The cache downloaded
8,908 module artifacts. No generated cache is tracked. Generic host/order
and three-seed sampling modules were adapted selectively from pinned
upstream sources; the original full 61-module project was not rebuilt.

Implemented the concrete crown and role-support arguments, extracted all
anchor-certificate fields from an arbitrary copy, and proved
`Concrete.Copy.anchor_counts`. `Concrete.matrix_anchor_counts` transports
the theorem to arbitrary increasing maps into the actual indexed matrix.
Explicit boundary theorems exclude height zero and exhibit a height-one
balanced copy. A separate semantic review found no missing hypothesis or
mismatch with the manuscript. It did not claim compiler verification or
independent peer review. The three-seed sampler's existing upstream
provenance is now explicit.

Actual formal command (with the pinned toolchain on PATH):

```sh
python3 scripts/run_formal_checks.py
```

The full local build succeeded. The audit checked 173 named theorems and
695 compiled project declarations, including private/generated declarations,
with only `propext`, `Quot.sound`, and `Classical.choice` as dependencies.
All sixteen project modules passed sequential `leanchecker` replay into
their respective imported environments. Unlike the original Std-only audit,
this does not freshly replay all Mathlib dependencies. Exact outputs and
source hashes are in `verification/reference/formal-audit.json`.
The count includes inherited theorems and is not a novelty count.

The manuscript's verification-status paragraph was updated, and
`python3 scripts/build_manuscript.py --regenerate-tex` rebuilt the PDF with
Pandoc 3.6.4 and three pdflatex passes, without warnings. The mathematical
statement did not change. Localization, concrete arbitrary-repair connections,
and the final real-valued removal theorem remain unformalized.

Final checks: all seven exact scripts reproduced their reference reports;
package integrity passed with 104 local links, matching source/PDF hashes,
and candidate status. An owning-module scan without namespace filtering
reproduced exactly the same 695 declarations and dependencies. The main
research track's validator passed with 362 local links across 107 Markdown
files, and its generated status view was refreshed. `git diff --check`
passed in both repositories.

## Zero-cell localization formalization — 2026-10-11

Confirmed PR #3 merged as `4e707a25ccf86c0e165e476de01dd1d8c627ce4d`,
then created standalone branch `shea256/four-zero-localization` from that
merge without renaming the previous branch. Rechecked upstream main; it
remained `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

Implemented seven Lean modules: concrete order comparisons, a common mode
frame for both anchor configurations, mode arithmetic, third-column
classification, concrete zero-cell localization, the dummy last row, and
the zero-set cardinality upper bound. The initial combined arithmetic tactic
was too expensive; the final proof instantiates applicable order bounds
from the class cases before invoking exact Presburger arithmetic. No theorem
hypothesis or mathematical claim was weakened.

With the pinned Lean 4.34.1 toolchain and Mathlib on PATH, ran:

```sh
python3 scripts/run_formal_checks.py
```

Actual output: `214 named Lean theorems; 957 declarations audited; module
kernel replay passed.` All 23 local modules replayed into their imported
environments, with only `propext`, `Quot.sound`, and `Classical.choice` in
the transitive dependencies. No added axioms or admitted proofs. This is
not fresh replay of all Mathlib and not independent peer review. The receipt
in `verification/reference/formal-audit.json` binds all compiled sources.
The headline exports are `Copy.zero_localization`, `matrix_zero_localization`,
`Copy.last_row_dummy`, and `card_zeroCells_le` in `OrderedRemoval.Concrete`.

The user-authorized separate reviewer found no semantic error and supplied
a standalone finite transcription, archived as
`verification/check_four_localization.py` with report and source snapshots.
It checks generic localization through h=7, all six column bounds on
419,513 ordered position pairs, zero-code injection through h=10, and 200
last-row class intersections through h=100. Omitting mode order has an
explicit nonleaf counterexample. The review did not claim compiler verification.

Updated the manuscript's verification paragraph, preserving the mathematical
statement. `python3 scripts/build_manuscript.py --regenerate-tex` used
Pandoc 3.6.4 and three pdflatex passes, with no warnings. Copy counting,
arbitrary-repair connections, exact zero-set equality and exact enumeration,
and the final every-c,C theorem remain formal obligations.

Final validation: `python3 scripts/run_checks.py` passed all eight exact
checkers and reference comparisons, including the newly archived reviewer
localization checker. Package integrity passed with 119 local links, source
and PDF hashes, and candidate status. The runtime-version field in the new
reviewer output is excluded from mathematical reference comparison for
portability. Actual timings/environment are in `verification/execution-receipt.json`.
The main research validator passed with 376 local links across 108 Markdown
files and no generated-view discrepancy. `git diff --check` passed in both
repositories. Compared with the merged audit, this adds 41 named theorems
and 262 compiled declarations and removes none; these are verification
counts, not claims of new mathematical results.

## End-to-end qualitative removal theorem — 2026-10-11

Started from merged localization PR #4, commit
`6e7711ffdc51280ff8b9c882a77c3af2982ddaa2`, on new standalone branch
`shea256/four-removal-theorem`. Upstream main remained
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

Adapted selected upstream guarded-path/sampling, coordinate-deletion counting,
normalization, and analytic modules with attribution. Added the concrete
coarse-count bridge, attained-distance semantics, and both unconditional final
capstones. The factor two in N_H≤2mn⁶ is retained through the c/2 decay step.
A separate reviewer found and reported three intermediate index-65 leftovers
in BodyExtension; they were corrected to 3 before successful compilation.
This was a porting error, not an accepted invalid theorem.

Commands used the pinned Lean 4.34.1 toolchain and Mathlib revision
`d13f23b723b8a846827a245b89c10fc7d3f11612`:

```sh
python3 scripts/run_formal_checks.py
python3 verification/check_sources.py
python3 scripts/build_manuscript.py --regenerate-tex
```

Actual formal audit output:

```text
387 named Lean theorems; 1444 declarations audited; module kernel replay passed.
The qualitative 4×4 removal theorem is formalized end to end. The sharper exact copy formula and canonical sampler bound are not formalized.
```

All 49 project modules were individually replayed into their imported Lean
environments. All compiled project declarations use only `propext`, `Quot.sound`,
and `Classical.choice`; no added axioms or admitted proofs were found. This is
not fresh replay of all Mathlib. The build emitted one harmless deprecation
warning for `if_false` in DistanceMeaning. The audit source receipt is
`verification/reference/formal-audit.json`; the local complete output is
`.context/removal-formal-checks.txt`. Named theorem totals include inherited
arguments and do not measure new mathematical contributions.

The source checker verified all 78 cached upstream file hashes. This did not
rebuild the original full upstream Lean development. Pandoc 3.6.4 regenerated
LaTeX; three pdfLaTeX passes completed with no reported warnings or overfull
boxes, updating the source/PDF hash receipt.

The separate agent's semantic review covers all 26 added modules and the
actual-pattern, independent-order, unrestricted-repair, normalization, and
final quantifier bridges. Its checker reconstructs all m³ selections through
h=4 and confirms maximum guard frequencies 2,4,8,16, with the unprotected
leaf-diagonal negative control at m². The original reviewed module snapshots
match the completed sources. Its earlier default-suite attempt passed eight
finite checks and then failed on the temporarily stale root-import hash; the
final audit receipt replaces that stale metadata.

The result remains candidate and independent peer review remains false. The
qualitative formalized-result flag is now true. Exact enumeration, canonical
sampler consequences, and novelty assessment remain outside this certificate.

Final `python3 scripts/run_checks.py` completed successfully under Python 3.9.25:
all nine exact checks matched their references (`compression`, `adversarial`,
`refinement`, `four`, `four_repair`, `four_literal`, `four_reviewer`,
`four_localization`, `four_removal`). Package validation passed 136 local links,
source-bound formal metadata, paper artifact hashes, and candidate status. The
complete local output is `.context/removal-package-checks.txt`.

The mirrored open-math-problems track preserves its separate 3×3 limitation
work. Its catalog and generated STATUS record the completed qualitative proof.
Root validation passed: 34 tracks in 7 groups, 389 local links across 109
Markdown files. `git diff --check` passed in both repositories.
