# Attribution and scope

Author: Ryan Shea. Developed with Codex assistance; no independent reviewer
or specific model configuration is claimed by this package.

The construction adapts OpenAI, *Polynomial removal fails for ordered binary
matrices*, September 25, 2026, pinned at
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` in
[openai/math](https://github.com/openai/math). Its tree host, sign chains,
four-step propagation, sampling argument for arbitrary repairs, and diagonal
leaf localization are inherited. The original source repository is licensed
under Apache 2.0. The pinned [source manifest](verification/source_manifest.json)
records provenance; upstream files are fetched into an ignored cache.

The earlier proposed contribution was a three-column nonshattering
argument and a 13×13 anchor yielding a 15×15 pattern. The current candidate
sharpens this to three-row crown exclusion, orders the laminar role supports
by containment, and proves rigidity of a 3×3 anchor, yielding a 5×5 pattern. The exact 4^−h density decay also follows for the original
construction and is not claimed as a new mechanism.

The proof draft and verification scripts were prepared for this research
track; the current manuscript describes the 5×5 candidate, with the earlier 15×15 draft retained for provenance. The companion literature and unresolved novelty check are
recorded in [BASELINE.md](BASELINE.md). No Lean certificate for the new result
or independent acceptance is asserted.
