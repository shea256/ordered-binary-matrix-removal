# Current result — candidate 3×4 removal obstruction

A new [written all-depth proof](proofs/three-by-four.md) gives the fixed
rectangular pattern

```text
1 0 0 1
1 0 1 0
0 1 1 1
```

For every h≥1, m=2^h, n=(14h+2)m, its explicit square binary host requires
at least m² arbitrary binary edits to become pattern-free and has at most
2mn⁵ ordered copies. Therefore its density is at most
2(14h+2)⁻²2⁻ʰ, while its certified distance is (14h+2)⁻². The proof preserves
failure of every polynomial removal bound, arbitrarily small ε, and
arbitrarily large hosts via blowups.

This is a **candidate pattern-size advance over the known 4×4 result**:
one fewer row, 12 rather than 16 entries (25% fewer). It is rectangular,
not a 3×3 result. No global minimality, exact repair equality, or exact
all-depth count is claimed for the new host. The broader novelty search
remains bounded; see [BASELINE.md](BASELINE.md).

Verification: two full weighted censuses agree at h=1..6, covering square
hosts of order 32, 120, 352, 928, 2,304, and 5,504; physical h=1 and
adversarial entry-rule variants were checked. A separately written agent
checker agrees through h=4 and checks structural sublemmas through h=7.
See the [exact report](verification/reference/three-by-four-report.json)
and [review](verification/reviews/three-by-four.md).
The main 3×4 theorem is **checked in Lean**, including arbitrarily small ε
and arbitrarily large hosts at that same ε. The source-bound audit and
separate-agent semantic review are linked in [formal/README.md](formal/README.md).
The result has **not received independent mathematical peer review**.
The older H4 formalization and its receipt remain separate.

A complementary [limitation certificate](proofs/asymmetric-limitations.md)
excludes 16,384 uniform templates at the inherited certified distance.
The successful candidate uses nonuniform anchor entries outside that class.
The user-authorized draft PR packages the proof and formal certificate.
No social announcement or author contact has been performed.


## Previous checkpoint record

# Current result — candidate quantitative refinement

The same H4 and its qualitative Lean obstruction were already released by
Erebos on October 9, before our 4×4 PR. Those headline results are not a new
advance here. The corrected comparison is in [BASELINE.md](BASELINE.md).

The [new written proof](proofs/optimized-order.md) globally orders all minus
horizontal modes first, then plus horizontal modes, then vertical modes.
For every h≥1, m=2^h and n=(14h+2)m, it gives:

- Exact copies N=(5/2)m⁶−m⁵, versus Erebos's (41m⁶−74m⁵)/4 for h≥2.
- Exact minimum unrestricted binary repair cost m², adapting Erebos's known repair.
- Limiting count and density ratio 10/41 at identical host size and exact distance:
  asymptotically 75.6098% fewer copies. The finite reductions differ; h=1 is equal.
- Minimum copy count within the class obtained by independently permuting intact
  anchor-mode blocks on the two axes with entries, weights, group orders and
  nonanchor orders fixed. No broader optimality is established.
- The inherited failure of every polynomial removal bound, including arbitrarily
  small ε and arbitrarily large hosts, with the same pattern and density exponent.

The complete finite census reproduces the formula through h=4 and the explicit
repair is H-free with m² edits at each checked depth. Separate physical h=1
checks and a separately written reviewer implementation support the result.
These are evidence for the written theorem, not a replacement for its proof.
The new construction/count/exact equality are not yet checked in Lean; the
existing Lean certificate applies to the previous host order and qualitative
H4 theorem. Independent mathematical peer review remains pending.

The result remains **candidate**. A bounded search found no earlier global-order
count refinement in the inspected sources; this is not proof of novelty.
No pattern-size reduction, new asymptotic exponent, global construction optimum,
or improvement for arbitrary adaptive testers is claimed.
