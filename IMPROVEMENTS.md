# Improvement record

## 2026-10-10 — whole-pattern localization, candidate 4×4 obstruction

Fixed pattern: 5×5 → 4×4; anchor component: 3×3 → 2×2. The smaller anchor
has unintended copies. The new proof instead classifies the full 4×4
pattern's embeddings and localizes every copy to a set of 2m zero cells.
It explicitly counts the additional copies, giving 128 at h=1 and
(33/4)m^6−(29/2)m^5 at h≥2. Protected sampling and designated propagation
still give an arbitrary-repair lower bound of m² edits.

The host order becomes (14h+2)2^h. The qualitative failure of polynomial
removal and the exponential-in-depth density mechanism remain inherited.
The manuscript, PDF, metadata, proof, and exact checks now describe this
4×4 candidate. Independent mathematical review remains pending; there is
no claim that a 3×3 obstruction is impossible.

## 2026-10-10 — reordered 3×3 anchor, candidate 5×5 obstruction

Fixed pattern: 15×15 → 5×5; anchor: 13×13 → 3×3. This also refines the
pinned primary manuscript's 66×66 construction. Three-row crown exclusion
and an order in which containing role supports come later replace the
previous density-prefix argument. The changed mode order is necessary
for the stated anchor rigidity: the old order has an unintended copy at h=2.

That release updated the manuscript, proof, metadata, and verification report
to the 5×5 candidate. All-depth proof review, formalization, and novelty assessment
remain pending. Finite checks do not establish a universal theorem.

## 2026-10-10 — earlier candidate anchor compression

Fixed obstruction: 66×66 → 15×15; anchor: 64×64 → 13×13.
The qualitative failure of polynomial removal is inherited. The proposed
three-column lemma permits the smaller anchor. The full theorem remains a
candidate pending independent proof review, formalization, and novelty review.
See RESULT.md and results/current.json.

## Formal verification checkpoint — October 11, 2026

The pattern remains **4×4**. Lean now proves its qualitative failure of every
polynomial removal bound end to end, using the actual host, coarse copy bound
2mn⁶, and m² lower bound for arbitrary binary repairs. The sharper exact count
and canonical sampler consequence remain outside the formal certificate.
See [formal coverage](formal/README.md). Independent mathematical review and
novelty assessment remain pending; this is a verification milestone, not a
further pattern-size reduction.
