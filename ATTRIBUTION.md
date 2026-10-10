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

The proposed contributions are the all-depth three-column nonshattering
argument and a 13×13 anchor with an asymmetric rigidity proof, yielding a
15×15 pattern. The exact 4^−h density decay also follows for the original
construction and is not claimed as a new mechanism.

The manuscript, proof draft, and verification scripts were prepared for this
review package. The companion literature and unresolved novelty check are
recorded in [BASELINE.md](BASELINE.md). No Lean certificate for the new result
or independent acceptance is asserted.
