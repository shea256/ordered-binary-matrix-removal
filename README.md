# Ordered binary matrix removal

**Candidate 3×4 obstruction · Main theorem checked in Lean · October 11, 2026**

![Ordered matrix-removal results on a proportional UTC date axis and logarithmic entry-count axis. OpenAI's October 6 commit is followed by ProveIt's October 7 commit, Erebos Labs' October 9 release, and our October 11 3×4 PR. Hollow markers show our later intermediate constructions.](assets/pattern-size-history.png)

The x-axis uses dated **GitHub records**, with proportional time spacing.
Erebos Labs' 4×4 [v1.0.0 release](https://github.com/erebos-labs/ordered-matrix-removal-4x4/releases/tag/v1.0.0)
was published **October 9, 2026 at 12:40:51 UTC**. The line tracks the smallest
entry count among the displayed results; hollow markers show our later
intermediate stages. OpenAI's paper is dated September 25; the chart uses
its October 6 repository commit. See [timestamp sources and scope](assets/README.md)
and [baseline attribution](BASELINE.md).

We give a construction with a Lean-checked main theorem for the fixed ordered binary pattern

```text
1 0 0 1
1 0 1 0
0 1 1 1
```

This reduces the forbidden pattern from the known **4×4 to 3×4**: twelve
entries instead of sixteen. For every h≥1, m=2^h and n=(14h+2)m, the square
binary host requires at least m² arbitrary binary edits to become H-free
and has at most 2mn⁵ copies. Its density is at most 2(14h+2)⁻²2⁻ʰ.
The written proof retains failure of every polynomial removal bound,
arbitrarily small distance parameters, and arbitrarily large hosts.

Read the [paper](manuscript.pdf), [Markdown manuscript](manuscript.md), and
[proof](proofs/three-by-four.md). Exact checks agree through six depths and
a [separate AI reviewer](verification/reviews/three-by-four.md) found no
remaining proof gap after a boundary qualification was corrected.

**The main theorem for the new 3×4 pattern is checked in Lean.** It includes
arbitrarily small distance parameters and arbitrarily large hosts at the same
chosen parameter. See the [formal proof](formal/README.md),
[source-bound audit](verification/reference/rectangular-formal-audit.json), and
[semantic review](verification/reviews/three-by-four-formal.md).
The proof and certificate were merged in [PR #6](https://github.com/shea256/ordered-binary-matrix-removal/pull/6).
Independent mathematical peer review and a broader novelty assessment remain
pending. This is a rectangular result, not 3×3 or a minimality theorem.
Neither exact repair equality nor an exact all-depth count is claimed.

## Baseline and attribution

Erebos published the same earlier 4×4 obstruction and its qualitative Lean
proof before our 4×4 PR. That priority correction remains in
[BASELINE.md](BASELINE.md) and [ATTRIBUTION.md](ATTRIBUTION.md). The tree,
threshold entries, protected sampling and propagation originate in OpenAI's
construction. The new ingredients are the asymmetric anchor encoding,
nonuniform extra ones and its full-copy localization argument.

The [optimized H4 order](proofs/optimized-order.md) is retained as a separate
quantitative refinement, with limiting copy ratio 10/41 to Erebos at identical
n and exact repair cost. Its metadata is in
[previous-optimized-four.json](results/previous-optimized-four.json).
The retained [4×4 Lean certificate](formal/README.md) concerns the previous
within-depth host and does not certify this 3×4 construction.

## Reproduce

```sh
python3 scripts/run_checks.py
# With the pinned Lean/Lake toolchain installed:
python3 scripts/run_rectangular_formal_checks.py
```

The checks use Python 3.9+ and the standard library. They include complete
weighted censuses through h=6, expanded physical h=1, a separately written
reviewer checker, and adverse variants omitting the essential extra entries.
Finite checks support the written proof; they do not prove its universal
quantifiers. See [verification scope](verification/README.md),
[RESULT.md](RESULT.md), [RUNLOG.md](RUNLOG.md), and [HANDOFF.md](HANDOFF.md).

Build the paper with `python3 scripts/build_manuscript.py`; add
`--regenerate-tex` with Pandoc 3.6.4 installed to regenerate LaTeX first.
The historical [improvement record](IMPROVEMENTS.md) records development,
not priority. Prepared by Ryan Shea with Codex assistance. Licensed under
[Apache 2.0](LICENSE); see [NOTICE](NOTICE).
