# Verification scope

`check_refinement.py` checks the current 5×5 candidate: all 5,813,724
quotient row triples in full anchor searches through depth 6; all 1,567,588
quotient row quintuples in full pattern searches through depth 2; 156,576
nonanchor column triples; and 28,944 role-support pairs through depth 8.
It also reruns exact mode counts, sampling marginals, path assignments, and
terminal threshold checks. It includes the old-order failure and witnesses
for all 16 nonanchor 2×2 patterns. The exhaustive full-pattern searches do
not assume the anchor rigidity theorem.

The retained `check_compression.py` checks anchor properties, 156,576 quotient triples,
weighted mode counts through depth 6, sampling marginals, and source manifest
metadata. `check_adversarial.py` uses a separate threshold/path calculation
without importing the host: 74,898 threshold cases and 34,952 path assignments.
Both were written by the same agent. Neither is independent peer review.

`reference/` contains deterministic outputs regenerated for this package.
`upstream-audit.json` is the historical same-agent audit from the originating
workspace: 78 source hashes and 61 implementation modules scanned. It is not
a Lean build. `fetch_upstream.py` plus `check_sources.py` reproduce the pinned
byte checks online. The cache is ignored, and default offline checks do not
pretend to rehash absent source files.

Finite tests cannot prove the all-depth lemma, rigidity theorem, or arbitrary
repair bound. Those obligations are the manuscript's mathematical argument.
