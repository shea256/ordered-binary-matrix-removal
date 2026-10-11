# Semantic review of the zero-cell localization modules

Date: 2026-10-11. Separate-agent reviewer: `/root/four_proof_reviewer`.

**Verdict: no mathematical error or extra full-copy assumption found in the four reviewed modules.** The strategy is a valid reorganization of the manuscript's balanced/unbalanced proof: extract one common mode frame, exclude a dummy third selected column, then apply a generic localization theorem whose hypotheses follow from either anchor-count case.

This is a separate-agent semantic review, **not independent peer review or a Lean build/axiom audit**. I did not edit the implementation or publish anything. `LocalizationArithmetic.lean` and `ThirdColumn.lean` were being built/debugged during this review; I make no claim about their compiler status.

Reviewed snapshots under `formal/OrderedRemoval/`:

| File | SHA-256 |
| --- | --- |
| `TreeComparisons.lean` | `a402122506dbc0dd8e3ade3451682f30411d90dce9b92f79115a75afa77aa23a` |
| `LocalizationFrame.lean` | `f997fbf287137b2c40c3156c2b03439278ee629442dacadab6d5211a75ff3dfb` |
| `LocalizationArithmetic.lean` | `1114a3d3f727d339c40a4fffc2e1abd642f49b0c27fc0f1966a0f85b0247d5a9` |
| `ThirdColumn.lean` | `8fb0aa89b81ddf89ec418af57e5b37b785c48f9fa99fc5f76691b6b26c8d1f72` |

Line references below refer to these snapshots. I also read `IndexedHost.lean` and the manuscript's localization section to check the interfaces.

## 1. Common mode frame has no localization assumption

`LocalizationFrame.Copy.mode_frame` (lines 65–90) uses the previously established anchor-count theorem to obtain exactly two anchor rows, at least one anchor column, and nonanchor columns at indices 2 and 3. It then uses the actual zero at zero-based `(2,3)` to force both its endpoints to be variable positions. This excludes a dummy endpoint without assuming a leaf or parent depth.

The actual one at `(1,0)` forces the second anchor row and first anchor column into the same mode `B`, with different groups. The ones at `(2,0)` and `(1,3)` give the row and column roles of the fixed-zero endpoints. The opposite orientation would require a variable position in row role 2 of a W mode or a variable position in column role 1 of a V mode. Those roles are dummy-only. Therefore the second anchor row is in zero-based group 1 and the first column in group 0.

This orientation proof is sound in **both** anchor-count configurations. It does not need to assert anchor rigidity or assume the balanced alignment first.

The first anchor row supplies mode `A` and its actual group. Its order before the second anchor row gives `modeRank A ≤ modeRank B`. The one at `(0,2)` supplies `c_role` for the third selected column. The frame records no depth, parent equality, B-mode kind, parity equality, or localization conclusion. The later generic theorem therefore receives derived data, not a disguised assumption of its conclusion.

`IndexedHost.copyOfIndices` also preserves the earlier model boundary: arbitrary independently increasing row and column index maps in the actual matrix give a `Copy` without an input structural certificate. No new restriction on copies enters through this import.

## 2. Column comparisons and shared-leaf endpoints

The new comparisons agree with the manuscript's recursive column order. The apparent difference between weak and strict inequalities is intentional:

| Ordered positions | Required node relation |
| --- | --- |
| Parent-plus before either-sign child | parent node `≤` child parent node |
| Either-sign child before parent-minus | child parent node `≤` parent node |
| Either-sign child before parent-plus | child parent node `<` parent node |
| Parent-minus before either-sign child | parent node `<` child parent node |
| Same-level plus before minus | plus node `≤` minus node |
| Same-level minus before plus | minus node `<` plus node |

`TreeComparisons` handles the shared leaf in the first two equivalences by the existing leaf-key comparisons. The two reversed-order implications then yield strict inequalities without pretending that leaf plus/minus are distinct classes. The same-level opposite-sign lemmas explicitly require `i<h`; that restriction is necessary and present.

The `ColumnBounds.same` field is about **equal depths**, not merely equal classes. Its proof correctly covers equal classes, plus-before-minus, and minus-before-plus. At leaf depth there is only one class, so its unequal-class branch cannot accidentally invoke a nonexistent leaf-minus class. Weak node order is the right conclusion for different actual coordinates in the same node block. The separate minus/plus field supplies strictness when the signs demand it.

The other four `ColumnBounds` implications separate adjacent-depth order from the parent's sign. Their signs and strictness match the table. `row_leaf_node_lt` correctly produces a strict node inequality, since leaf blocks have one position.

No boundary error was found at `h=1`, where the parents are the root classes, or at shared leaves. Statements quantified over modes require no additional `h≥1`: a `Mode h` already entails a positive level at most `h`.

## 3. A dummy third column is genuinely impossible

The proof in `ThirdColumn.ModeFrame.third_column_variable` (lines 56–88) is valid and does not borrow the desired localization.

Assume the third selected column is dummy. If the second selected column were nonanchor, its zero against the third selected row would force it to be variable. But it precedes the dummy column in the copy, while every dummy column precedes every variable column in the host. This is impossible. Thus the second selected column is anchor, giving the balanced configuration.

`balanced_alignment` uses the crossed one, actual column order, and the frame's row-mode inequality to get both `rank B≤rank A` and `rank A≤rank B`; injectivity of `modeRank` gives `A=B`. Strict anchor block ranks force the first row's group to be 0. The second anchor column's group is then 1. These are conclusions, not extra premises.

The dummy third column belongs to column role 0 in this aligned mode, forcing a V mode. The last selected row belongs to row role 1. It cannot be dummy in a V mode and cannot be anchor by the anchor count, so it is variable. The fixed zero, the bottom-right one, and actual row order now give the ordinary vertical-mode contradiction.

`vertical_zero_impossible` reproduces the manuscript's two vertical exclusions. For V-plus, child-parent row order and the parent diagonal one force the allegedly zero transition to one. For V-minus, parent-child row order and the parent diagonal zero force the allegedly one transition to zero. The proof permits the child to be a shared leaf and does not assume it retains an internal minus entry rule.

This replaces the manuscript's separate non-dummy arguments by a sound common reduction. It does not strengthen the copy hypotheses.

## 4. Generic zero localization and the essential parity condition

`LocalizationArithmetic.mode_zero_localization` (lines 79–100) assumes exactly:

- the derived rank order `A≤B`;
- variable positions `r,c,d` with the three actual role memberships;
- entry values `A(r,c)=1`, `A(r,d)=0`;
- actual column order `c<d`.

It does **not** require that A and B coincide, that the first anchor group have a fixed value, that `c` and `d` avoid one another's supports, or that the copy have one versus two anchor columns. This is a stronger local lemma than merely checking designated balanced bodies, but its conclusion is valid.

The class-entry formula and column bounds give the same four mode cases as the manuscript:

| B mode | Reason no nonlocalized case survives |
| --- | --- |
| V-plus | A one in any permissible own/parent class before the zero's parent-plus column contradicts the transition zero. The extra parent-minus class at a leaf uses the strict minus-before-plus bound. |
| V-minus | The own-minus or preceding-minus one contradicts the zero and column order. The nonexistent preceding root class cannot satisfy the class equation. |
| W-plus | Equal child parity comes from the roles of `r` and `d`; own/parent one inequalities force `r≤d`, contradicting their zero. |
| W-minus | A parent-minus `c` is impossible. A nonleaf own-minus `c` is excluded using earlier-mode parity. At a leaf, own-leaf or parent-plus `c` forces `node d=node r/2`. |

The critical theorem `earlier_minus_child_parity` (lines 62–75) has the correct hypotheses: `B` is a W-minus mode, its level is strictly below the leaf, `c` is in that own-minus class, and `A≤B`. Whole supports of this class occur only at the next level; plus supports cannot name a nonleaf minus class. Thus `A` must supply a W-minus child half of parity no later than B's. The conclusion is the **inequality** `node c % 2 ≤ kind B % 2`, not a spurious parity equality.

Combining this with `node r % 2 = kind B % 2` and `node r/2 ≥ node d ≥ node c/2` forces `node r ≥ node c`, contradicting the internal strict one. At the leaf the theorem intentionally does not apply this earlier-minus classification, because plus and minus child supports coincide there. The weak leaf one instead suffices to force equality of parent indices.

The generic conclusion says the fixed zero lies between leaf class `2h` and parent-minus class `2h−1` at the matching parent node; it also restricts `c` to the leaf or parent-plus class. This is precisely the required local statement. It does not yet claim the last row is dummy or an exact count, and should not be reported as proving those additional conclusions.

### Concrete negative control

Dropping only the mode-order condition makes generic localization false. At `h=3`, take

`B=W_(2,0)−`, `A=W_(2,1)−`, `r=R_2−(2)`, `c=C_2−(3)`, `d=C_1−(1)`, and A's zero-based column group 0.

All three role memberships hold; `A(r,c)=1`, `A(r,d)=0`, and `c<d`. The row is not a leaf. The failed hypothesis is exactly `A≤B`: parity-1 W-minus follows parity-0 W-minus. This also explains why reversing those parity modes would invalidate the argument. The revised order is materially used, not a cosmetic artifact.

## 5. Executed finite checks and limits

I ran the separate reviewer host/support implementation from `.context/reviewer-four-localization.py`, without importing candidate-package code. Unlike the previous complete-copy tests, this run enumerated **exactly the generic theorem's weaker hypotheses**: all `A≤B`, both first-anchor groups including same-mode group 1, all variable role members, one/zero entries and column order. It did not impose extra cross-role exclusions from a full `H4` copy.

Actual output `(h, one-zero triples before column-order filtering, ordered survivors)`:

```text
[(1, 9, 9), (2, 76, 22), (3, 626, 44), (4, 5110, 88),
 (5, 41246, 176), (6, 331246, 352), (7, 2654606, 704)]
```

Every ordered survivor satisfied all four generic localization conclusions. The nonleaf negative control above was also executed and passed as a counterexample when mode order was omitted.

A second independent transcription checked all six `ColumnBounds` implications against the actual dyadic-key ordering on every ordered pair of actual variable positions through depth six, including `h=0` and different positions in one block:

```text
ColumnBounds finite audit: all six implications passed on 419513 ordered actual-position pairs through h=6, including h=0.
```

Root repository validation also passed:

```text
PASS: 34 tracks in 7 groups; catalog, prompts, artifacts, and views agree
PASS: 362 local links across 107 Markdown files
```

These checks support the semantic assessment but do not prove the all-depth theorem or report a kernel result. The next concrete bridge should extract the variable third column from every copy, obtain the two entry equalities and column order, and invoke `mode_zero_localization`. Formal membership in the zero-cell set, the size of that set, last-row localization, counting, and repair results remain distinct claims unless subsequent modules prove them.

## 6. Follow-up review: concrete zero set, last row, and cardinality

I subsequently reviewed `ZeroLocalization.lean`, `LastRow.lean`, and `ZeroSetSize.lean`. **No semantic error found.** These modules supply the intended source-level bridge, last-row conclusion, and cardinality upper bound discussed as remaining work above. They were still compiling during this review; this report does not assert successful Lean verification.

| File | SHA-256 |
| --- | --- |
| `ZeroLocalization.lean` | `8f24112953fcaf426bebae957989e3d9d2fee0227dc5f8f2133951121ac2e414` |
| `LastRow.lean` | `8a93f0d4f11c601d74e3da6452f0e8b154ddb00762687a13702db4b71238ebe5` |
| `ZeroSetSize.lean` | `bcbef9fc64b1c0a2d53b37cab712a4e7d7e2ea8e1fc43e391d7629d4f3263559` |

### Localization interfaces

`InZeroSet` requires both endpoints to be variable positions, row class `2h`, column class `2h−1`, and the column node equal to half the row node. These are exactly a leaf and a position in its immediate parent-minus block. At `h=0`, the column-class equation is impossible, so the set is correctly empty. The natural-number subtraction convention introduces no unintended root case.

`zeroSet_entry` correctly excludes every one-entry disjunct: own-class and matching-sign transition classes do not match these two classes, while the exceptional leaf-to-parent-minus one would require a strict inequality contrary to the specified node equality. Thus every designated cell is actually zero.

`Copy.zero_localization` obtains a frame and the variable third column, then derives both entry values and the column order directly from `Copy`. It passes exactly these facts to the generic theorem. There is no additional caller-supplied role assumption. Zero-based `(2,3)` is consistently the third selected row and fourth selected column. `matrix_zero_localization` uses the inverse **row** enumeration for the row and inverse **column** enumeration for the column, preserving independent axes and the same fixed pattern entry.

### Last-row proof

`ModeFrame.minus_mode` uses the localized row/column classes and their frame roles to exclude V-plus, V-minus, and W-plus. For example, V-minus would make the leaf row a parent of an available mode, requiring a level above `h`; W-plus would put the last column in the child's plus/leaf class, rather than the parent-minus class. The conclusion `4≤kind B` is sufficient because concrete mode kinds are always below six.

The final selected row is already nonanchor. If the second selected column is anchor, balanced alignment identifies it with B's group 1. Hence the last row has B's row role 1, which is dummy-only for a W mode; a variable last row is impossible.

In the unbalanced case, the zero at `(2,1)` forces the second selected column `q` to be variable. It shares A's role with the third selected column `c`, so their classes agree. Localization says this class is either leaf or parent-plus. If a proposed variable last row `s` has ones at both `q` and the localized parent-minus column `d`, the concrete class-shape lemma forces `s` to be a leaf:

- For leaf `q`, a variable row one there is immediately a leaf.
- For parent-plus `q`, the possible row classes are parent-plus or leaf; for parent-minus `d`, they are parent-minus or leaf. Their intersection is the leaf class.

This compressed class argument is equivalent to the manuscript's two cases. Because `s` occurs after the leaf `r`, `node r<node s`. Row antimonotonicity within the leaf class then transfers the one at `(s,q)` to `(r,q)`, contradicting its actual zero. No assertion about edited matrices or a hypothetical repair enters this argument.

### Injective zero code and cardinality

For a zero-set pair `(r,d)`, the leaf node is its coordinate `r.2`, and the parent-minus node is `d.2/2`: the parent block size is exactly two. The lemma `zero_coordinate_quotients` therefore correctly concludes `d.2/2=r.2/2`. Its exponent identity follows from `d.class+1=2h`, which also forces `h≥1`; it does not silently assume positivity at `h=0`.

The code stores the full leaf coordinate and the parent-column coordinate modulo two. Equality of codes gives equal leaf coordinates, hence equal parent-column quotients. Equal quotient and remainder modulo two determine the entire parent-column coordinate. Both classes are already fixed by zero-set membership, so the two raw positions and then the pair are equal. Default codes assigned to nonvariable positions are irrelevant because injectivity is claimed only on the zero set.

The final `Finset` image argument is valid: an injective-on-set map preserves that set's cardinality, and its codomain has `2^h·2` elements. Hence `card_zeroCells_le` proves the stated **upper bound** `≤2·2^h`. It does not claim an exact-cardinality theorem; equality for positive h remains a stronger statement than this declaration. The upper bound suffices for the coarse copy-count argument. Transferring a raw-cell count to a separately defined indexed-cell set would require the product of the row and column index bijections, although a copy count conducted entirely on raw positions can use this result directly.

No missing hypothesis, circular dependency, or incorrect zero-coordinate identification was found in these three modules.

## 7. Reproducible reviewer artifacts

At the parent's request, the earlier generic-localization and `ColumnBounds` inline checks have now been preserved in the standalone script:

```text
/home/vercel-sandbox/open-math-problems/.context/reviewer-localization-checks.py
```

It uses only the Python standard library and includes its own manuscript-derived host, supports, and tree traversal. It has no dependency on the implementation or on the older reviewer script. `run_generic` preserves the earlier weaker-hypothesis enumeration and negative control; `run_bounds` preserves the earlier actual-position comparison checks. New `run_zeros` checks the zero code, zero values, and last-row class intersection.

The exact combined command I executed, from `/home/vercel-sandbox/open-math-problems`, was:

```sh
python3 .context/reviewer-localization-checks.py --check all > .context/reviewer-localization-checks-output.json
```

It exited with code 0 under Python 3.9.25. The saved actual output is:

```text
/home/vercel-sandbox/open-math-problems/.context/reviewer-localization-checks-output.json
```

The individual commands to reproduce just the two earlier checks are:

```sh
python3 .context/reviewer-localization-checks.py --check generic
python3 .context/reviewer-localization-checks.py --check bounds
```

The preserved run reproduced the earlier generic counts exactly and again checked 419,513 ordered actual-position pairs for all six column implications. The new zero-code check found 0 zero-set pairs at `h=0` and respectively `4,8,16,32,64,128,256,512,1024,2048` at depths 1–10, with exactly as many distinct codes and all entries zero. All 200 possible last-row class intersections at depths 1–100 were leaf-only. The latter is a finite check of the class argument, not an enumeration of all copies or a proof of the universal theorem.

These two artifact files can be archived alongside the review; no older `.context` helper is needed. If moved, the script can be run from any directory because it has no relative file imports or input files.

## 8. Final proof-body snapshot check for two revised files

I reread the current `LocalizationArithmetic.lean` and `ThirdColumn.lean` after the parent reported proof-body compilation fixes. Their theorem statements, hypotheses, and conclusions are unchanged from the versions reviewed in Sections 1–5. I found no semantic change or additional assumption.

| File | Revised SHA-256 |
| --- | --- |
| `LocalizationArithmetic.lean` | `76fc67f64f5eb468346595c81fe8492f84717392b7b28f1397fa99e3b78e865b` |
| `ThirdColumn.lean` | `e1844cb48e2943ab03636809b36a2ac4e8f0d5c93ed9439a05198f65f7c48258` |

The revised arithmetic proof first converts the existing row/column roles to their proved support descriptors. It splits the same leaf/nonleaf and mode-kind cases, then the same three concrete one-entry disjuncts. Conditional `ColumnBounds` facts and the earlier-minus parity bound are now explicitly instantiated only when their premises follow in that case. These are derived facts, not new hypotheses. Clearing the original role data and conditional facts after retaining their consequences does not change the theorem's assumptions or meaning. In particular, the crucial nonleaf parity inequality is still derived from the revised mode order, and no parity condition has been imposed at shared leaves.

In `ThirdColumn`, the new rewrite of `hes` in the variable branch merely changes the already-proved role of `E.rows 3` into the role of that branch's actual variable `s`. The dummy branch likewise uses `hes` when simplifying its impossible role. Both are explicit substitutions of the case equality; the balanced alignment and vertical exclusion are unchanged.

This final snapshot note is a semantic source comparison only. I did not independently rerun Lean, assess the remaining modules' build status, or upgrade the review to an end-to-end formalization or independent peer review. Since the declarations and mathematical data were unchanged, the finite checks above were not rerun solely for these proof-body edits.

## Archive paths

The snapshots and original execution paths above record the review as performed.
The standalone package archives the [checker](../check_four_localization.py)
and [actual output](../reference/four-localization-report.json). Reproduce with
`python3 verification/check_four_localization.py --check all` from the package root.
The source hashes in this review identify reviewed snapshots; the current
compiler-checked sources are identified separately by the
[formal audit](../reference/formal-audit.json).
