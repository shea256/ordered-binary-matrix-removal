# Dated pattern-size chart

[PNG](pattern-size-history.png) and [SVG](pattern-size-history.svg) use a
**proportional UTC time axis**. The logarithmic vertical axis counts specified
binary entries: rows times columns. Standard ticks at 10, 100, 1,000 and
10,000 are equally spaced.

The step line follows the minimum entry count among the displayed results.
Hollow markers show this project's intermediate constructions at their own
dates, including those already surpassed by the earlier ProveIt/Erebos work.
This is a selected, sourced history rather than a complete priority ranking.

## Timestamp sources

These are **GitHub record timestamps**, not asserted discovery dates or a
uniform measure of first public availability. A Git commit date is supplied
by the committer and does not prove when that commit became publicly visible.
A release's `published_at` records release publication; a PR's `created_at`
records when the PR was opened. Repository creation and social announcements
are separate events. We do not infer the absence of an announcement from
finding a GitHub record.

| Source | Pattern | Entries | Timestamp (UTC) | Record | Role |
| --- | --- | ---: | --- | --- | --- |
| OpenAI | 66×66 | 4,356 | 2026-10-06 21:58:50 | [Git commit](https://github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a) | Main-line milestone |
| ProveIt | 5×5 | 25 | 2026-10-07 21:24:26 | [Git commit](https://github.com/VladimirReshetnikov/ProveIt/commit/bfbfe915186310fdf745a7a089e7dd88eeb773b1) | Main-line milestone |
| Erebos Labs | 4×4 | 16 | 2026-10-09 12:40:51 | [GitHub release](https://github.com/erebos-labs/ordered-matrix-removal-4x4/releases/tag/v1.0.0) | Main-line milestone |
| This project | 15×15 | 225 | 2026-10-10 06:37:28 | [Git commit](https://github.com/shea256/ordered-binary-matrix-removal/commit/fa2aa33105d7d16ae782f4a0858a417e31de9f05) | Earlier project stage |
| This project | 5×5 | 25 | 2026-10-10 15:10:23 | [Git commit](https://github.com/shea256/ordered-binary-matrix-removal/commit/f16d432d9a918c694f0b404a12f744c0c8b0db03) | Earlier project stage |
| This project | 4×4 | 16 | 2026-10-10 18:48:25 | [PR opened](https://github.com/shea256/ordered-binary-matrix-removal/pull/1) | Earlier project stage |
| This project | 3×4 | 12 | 2026-10-11 18:38:32 | [PR opened](https://github.com/shea256/ordered-binary-matrix-removal/pull/6) | Main-line milestone |

Erebos Labs' **v1.0.0 release was published October 9, 2026 at 12:40:51 UTC**.
That is evidence of its public 4×4 result by that timestamp, regardless of
whether there was a social announcement. Its repository was created at
12:39:06 UTC, but the chart uses the result-bearing release instead.

OpenAI's manuscript is dated **September 25, 2026**. Its point uses the
**October 6, 2026 repository commit** that added the paper, so every x-value
refers to a GitHub record. ProveIt's October 7 commit includes the written
5×5 result and the H4 candidate; Erebos's later release supplies the 4×4
Lean theorem. These source and verification differences are documented in
[BASELINE.md](../BASELINE.md). Our 3×4 point uses the opening of
[PR #6](https://github.com/shea256/ordered-binary-matrix-removal/pull/6), which
contained the main theorem and its Lean certificate.

The fixed-pattern dimensions are separate from host size: hosts can be
arbitrarily large. The 25% reduction compares 16 with 12 specified entries.
Independent mathematical review remains pending.

## Regenerate

The archived [event data](pattern-size-events.json) contains each source URL,
API endpoint, timestamp field and pinned commit. Dates were checked against
GitHub on October 11, 2026. Rendering is offline and requires Matplotlib 3.9.4:

```sh
python3 scripts/build_figure.py
```

The renderer checks the current and baseline dimensions against
[metadata](../results/current.json) and writes a [receipt](pattern-size-history.json)
binding the dated input, renderer and PNG/SVG hashes. Package validation
checks the chronological data, current dimensions and README embedding
using only the Python standard library.
