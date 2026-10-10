# Attribution and scope

Author: Ryan Shea. Developed with Codex assistance. A separate Codex reviewer
audited the 4×4 argument; this is not independent mathematical peer review.
No specific model configuration is claimed by this package.

The construction adapts OpenAI, *Polynomial removal fails for ordered binary
matrices*, September 25, 2026, pinned at
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` in
[openai/math](https://github.com/openai/math). Its tree host, sign chains,
four-step propagation, sampling argument for arbitrary repairs, and diagonal
leaf localization are inherited. The original source repository is licensed
under Apache 2.0. The pinned [source manifest](verification/source_manifest.json)
records provenance; upstream files are fetched into an ignored cache.

The first proposed contribution was a three-column nonshattering argument
and a 13×13 anchor yielding a 15×15 pattern. The next candidate used
three-row crown exclusion and ordered laminar supports to make a 3×3
anchor rigid, yielding a 5×5 pattern. The current 4×4 candidate uses a
2×2 anchor without pure anchor rigidity. Its proposed new contributions
are the full-pattern anchor classification, leaf-to-parent zero-cell
localization, and exact enumeration of the additional copy families.
The arbitrary-repair argument remains inherited. The exact 4^−h decay
also follows for the original construction and is not a new mechanism.

These proof drafts and verification scripts were prepared for this research
track. The current manuscript describes the 4×4 candidate; the 5×5 and
15×15 drafts and exact reports are retained for provenance. Companion
literature and the unresolved novelty check are recorded in
[BASELINE.md](BASELINE.md). No Lean certificate for the new result or
independent acceptance is asserted.

The [separate-agent report](verification/reviews/four-separate-agent.md)
and its checker retain reviewer provenance. The coordinating agent wrote
the additional literal checker and the partial Lean modules. The latter
formalize conditional parts of the current argument; propagation and
sampling are inherited methods, not new mathematical contributions.
Their actual coverage is described in [formal/README.md](formal/README.md).
