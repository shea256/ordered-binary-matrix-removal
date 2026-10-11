# Ordered binary matrix removal

**Candidate 3×4 obstruction · Main theorem checked in Lean · October 11, 2026**

![Selected forbidden patterns shrink from 66×66 through 15×15, 5×5 and 4×4 to 3×4. The logarithmic vertical axis counts entries: 4,356, 225, 25, 16 and 12. Erebos has the earlier 4×4 result; the current 3×4 theorem is checked in Lean.](assets/pattern-size-history.png)

The chart shows selected constructions ordered by size. The 15×15 and 5×5
points record this project's development, not worldwide priority.
Erebos published the earlier 4×4 theorem; ProveIt supplied earlier 5×5 work
and the H4 candidate. See [baseline and attribution](BASELINE.md) and
[chart sources and regeneration](assets/README.md).

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
