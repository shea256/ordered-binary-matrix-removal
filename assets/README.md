# Pattern-size chart

[PNG](pattern-size-history.png) and [SVG](pattern-size-history.svg) show
selected constructions in decreasing order of pattern size. The logarithmic
vertical axis counts specified binary entries: rows times columns.

| Pattern | Entries | Source and role |
| --- | ---: | --- |
| 66×66 | 4,356 | OpenAI baseline; [source audit](../BASELINE.md). |
| 15×15 | 225 | Earlier project construction; [proof](../proofs/compressed-pattern.md). |
| 5×5 | 25 | Earlier project construction; [proof](../proofs/five-by-five.md). ProveIt published earlier 5×5 work. |
| 4×4 | 16 | Erebos's earlier theorem; [priority correction](../BASELINE.md). |
| 3×4 | 12 | Current [proof](../proofs/three-by-four.md) and [Lean certificate](../formal/README.md). |

The chart is a selection by size, not a timeline or a sequence of world records.
The dimensions describe the fixed forbidden patterns. Host matrices remain
arbitrarily large. The 25% reduction compares entry counts, not removal-bound
constants, host sizes or runtimes. Independent mathematical review remains pending.

With Matplotlib 3.9.4 installed, regenerate from the repository root:

```sh
python3 scripts/build_figure.py
```

The renderer reads the current and baseline dimensions and formalization status
from [current metadata](../results/current.json); the historical stages come
from the proofs and [improvement record](../IMPROVEMENTS.md). It writes a
[data and artifact receipt](pattern-size-history.json). Package validation
checks the current dimensions, PNG/SVG hashes and README embedding using only
the Python standard library.
