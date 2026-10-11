# Reproduction log


## October 11 — date axis and Erebos release timestamp

The user requested real dates and attribution of Erebos Labs' repository
result. Checked GitHub API records for Erebos's repository and releases,
OpenAI's commit adding the paper, ProveIt's intake commit, and our relevant
commits/PRs. Erebos v1.0.0 has `published_at=2026-10-09T12:40:51Z`; repository
creation was 12:39:06Z. The chart uses the result-bearing release timestamp,
without inferring a discovery date or the presence/absence of an X announcement.

Changed the x-axis to proportional UTC time using explicit GitHub event types.
OpenAI's paper date (September 25) is separated from its October 6 commit.
ProveIt's October 7 written 5×5 result and Erebos's October 9 4×4 release
precede our October 10 intermediate stages. Those stages now appear as hollow
markers; the line follows the minimum entry count among the plotted records.
The final point is our October 11 3×4 PR opening. The vertical axis remains
logarithmic with standard decade ticks. The theorem and Lean sources are unchanged.

Archived the seven timestamp records, pinned commits, event types and source
URLs in `assets/pattern-size-events.json`; refreshed the generated figure
receipt. Updated README, chart documentation, baseline date notes, and
package-integrity checks. Regenerated PNG/SVG with Matplotlib 3.9.4 via
`python3 scripts/build_figure.py` using the existing figure-tools interpreter.
Visually inspected the final chart and adjusted crowded labels.

Validation: `python3 scripts/run_checks.py` passed all 14 suites and reference
comparisons. Package integrity passed 177 local links plus all formal,
manuscript and figure hashes. UTC timestamp order, entry counts, Erebos's
release time and SVG parsing were checked. `git diff --check` passed.


## October 11 — standard logarithmic chart ticks

Replaced the irregular data-value ticks with equally spaced base-10 decade
ticks: 10, 100, 1,000 and 10,000. The chart was already logarithmic; its
axis now explicitly says log₁₀, while the exact entry counts stay beside
each point. Regenerated PNG, SVG and the artifact receipt with Matplotlib
3.9.4 using `python3 scripts/build_figure.py`, and visually checked the PNG.
The plotted values and theorem statements are unchanged. The chart readme
now explains the tick spacing. PR #7 was merged before this adjustment.

Validation: all 14 suites in `python3 scripts/run_checks.py` passed,
including reference comparisons and package integrity (180 local links
and source/artifact hashes). Visual inspection and `git diff --check` passed.


## October 11 — restore the README chart through 3×4

The merged 3×4 README omitted its earlier image embedding and the old renderer
still expected square-pattern metadata. Restored the embedding and updated
`scripts/build_figure.py` for rectangular dimensions. It now plots specified
entry counts 4,356 → 225 → 25 → 16 → 12 on a labeled logarithmic scale.
Stage positions order selected constructions by size; the figure and caption
credit Erebos's earlier 4×4 theorem and ProveIt's earlier 5×5 work/H4 candidate.
The final callout compares 16 with 12 entries and records the existing Lean
verification. Candidate status and independent-review requirements are retained.

Rendered PNG and SVG with Matplotlib 3.9.4 using:

```sh
python3 scripts/build_figure.py
```

In this workspace the rendering interpreter was
`/home/vercel-sandbox/open-math-problems/.context/figure-tools/bin/python`.
Visually inspected the generated PNG. Added `assets/README.md` and a generated
receipt binding the plotted data, renderer, and image hashes. The existing
package validator now rejects a removed README embedding, stale dimensions,
or changed graphic artifacts. Updated the README's obsolete draft wording
because PR #6 is merged. This is a presentation update to the existing theorem.

Validation: `python3 scripts/run_checks.py` passed all 14 exact-check suites
and deterministic reference comparisons. Package integrity passed 180 local
links plus graphic, formal-source and manuscript hashes. `git diff --check`
passed. The SVG parsed successfully and the plotted entry counts were
recalculated from the five pattern dimensions. No Lean source changed.


## October 11 — 3×4 draft PR and complete Lean theorem

Final package validation: `python3 scripts/run_checks.py` passed all 14 exact
checks and deterministic reference comparisons under Python 3.9.25;
the individual checks totalled 57.518 seconds on this workspace.
The package validator passed 166 local links, source-bound Lean receipts,
proof/manuscript agreement and PDF hashes. `git diff --check` passed.
The PDF was rebuilt with Pandoc 3.6.4 and three pdflatex passes; its receipt
records no warnings. The first page and formalization page were visually
inspected. All 24 formal-review source hashes match the compiled snapshot.

The root research mirror passed `python3 scripts/validate_repository.py --write`
and `python3 scripts/validate_repository.py`: 34 tracks in 7 groups,
448 local links across 116 Markdown files. The catalog remains Candidate.


Prepared branch `shea256/three-by-four-obstruction` in the existing public
standalone repository, based on the merged previous PR. Preserved the prior
H4 source-bound audit and both older result metadata files. The 3×4 proof,
finite reports, independent implementations, limitation certificate and
required discovery dependencies are included in the review package.

Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`
checked the literal new host, independent orders, complete anchor classification,
fixed-zero localization, 2mn⁵ count, arbitrary m² repair bound, decay, and
uniform blowups. The final theorem chooses ε before an arbitrary host-size
threshold, preserving the strong quantifiers. The formal sampler uses the
inherited three seeds with m-sized row subgroups; its cell bound is 1/m².
The blowup argument proves the sufficient q⁷ count upper bound and handles
arbitrary repairs by partitioning all cells into offset slices.

The new development has 24 modules, 98
named theorems and 462 compiled declarations. Including
inherited historical code, the audit checked 485 named
theorems and 1906 declarations, and replayed all
73 project modules. These counts include inherited
arguments and do not measure novelty. Only `propext`, `Quot.sound`, and
`Classical.choice` occur as transitive axioms. Replay imports each module's
environment; it does not freshly replay all Mathlib or use a second proof checker.

Actual formal command, with the pinned toolchain on PATH:

```sh
python3 scripts/run_rectangular_formal_checks.py
```

The receipt is `verification/reference/rectangular-formal-audit.json` and
complete local output `.context/rectangular-formal-checks.txt`. Early builds
caught porting/syntax errors and an overlarge arithmetic search; the final
proof uses explicit class cases before exact arithmetic. No assumptions were
weakened and no admitted proof was used. The final build has the unchanged
historical `if_false` deprecation warning in DistanceMeaning; new modules
compile without warnings.

The authorized separate agent reviewed all new modules and found no required
mathematical correction. Its review and exact execution limitations are in
`verification/reviews/three-by-four-formal.md`; this is not independent peer
review. Its early targeted repair declaration check succeeded, while a later
attempted import encountered a file temporarily absent during rebuilding.
The coordinating agent's completed audit supplies the full compiler evidence.

The shipped discovery script was also run through h=2, reproducing 1,632 and
101,888 copies; the certificate generator's CLI/imports were checked. OpenAI
and Erebos main commits were reread and matched the pinned baselines. Additional
bounded smaller-pattern searches located no new primary result.

## October 11 — optimized global order, exact repair and prior-work correction

Environment: Python 3.9.25; Linux-6.18.49-x86_64-with-glibc2.34. Work was carried out in the standalone
checkout `.context/ordered-binary-matrix-removal` on branch
`shea256/optimized-mode-order`, based on fetched origin/master after PR #5 merged.
No external publication or author contact was performed.

Read Erebos's current theorem, exact-count manuscript and full terminal-anchor
repair proof at `6d21ce36e83b71d8a44015016cf3ac77e44b55ff`. Rechecked current main
via GitHub API and the source listing for OpenAI #190. Prior baseline/priority
corrections are in BASELINE.md; earlier missed searches are not novelty evidence.

Executed initial literal full-copy censuses for four within-depth orders at
h=2,3, then the global minus-first order at h=1..4. The final repeatable checker
uses a column-quadruple/row-DP census and a separately written reviewer uses
recursive axes and explicit row-quadruple enumeration. Neither final census
assumes localization or the closed formula.

Commands executed from the standalone project root:

```sh
python3 verification/check_optimized_order.py > .context/optimized-order-report.json
PATH=/home/vercel-sandbox/open-math-problems/.context/pandoc-3.6.4/bin:$PATH python3 scripts/build_manuscript.py --regenerate-tex
python3 scripts/run_checks.py > .context/optimized-package-checks.txt 2>&1
python3 scripts/validate_repository.py
```

The separate reviewer first ran its checker from ignored scratch space; the
unchanged implementation is now `verification/check_optimized_order_reviewer.py`
and was rerun by the full suite. Its review covers the actual proof text and
corrected a stale old-host statement about the leaf diagonal. The global order
makes that diagonal an original-copy hitting set; that does not make flipping
it a valid repair. This is separate AI review, not independent peer review.

Actual results, h=1,2,3,4 respectively:

| Host order | Exact copies |
| --- | --- |
| Erebos | 128; 23040; 2080768; 152567808 |
| Previous local order | 128; 18944; 1687552; 123207680 |
| Minus-first within each depth | 128; 9216; 753664; 53477376 |
| Global minus-first | 128; 9216; 622592; 40894464 |

The terminal-anchor repair has zero copies with exactly 4,16,64,256 physical
edits at these depths. The expanded h=1 scans agree. Intrinsic-family sums run
through h=10; the reviewer exhausts support/generic localization cases through
h=7. These are finite implementation checks, not proofs of universal claims.
The all-depth enumeration, unrestricted repair equality, restricted permutation
optimum and blowup quantifiers are written in proofs/optimized-order.md.

All **11** suite commands matched their reference reports; package integrity
passed with 128 local links, manuscript hashes, and candidate status. New-check
runtimes in the suite were optimized_order 20.852 seconds, optimized_order_reviewer 10.916 seconds. The PDF build completed with three pdflatex
passes and no warnings. Initial build failures from plain Unicode mathematics
and TeX's non-UTF-8 diagnostic output were corrected; the successful build uses
explicit math syntax and replacement decoding for diagnostics.

All 53 paths in the historical formal source manifest still match their hashes.
No new Lean build was claimed or needed to verify those unchanged sources. The
old capstone covers the previous host order; new order/count/exact repair and
optimality flags remain false. The announcement draft qualifies 75.6% as an
asymptotic reduction and credits Erebos. Its lead post has 276 characters under
the usual 23-character URL accounting.

Parent catalog regeneration/validation and whitespace checks were also run.
The 3×3 limitations and previous research artifacts were preserved.


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
