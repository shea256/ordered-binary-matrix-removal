# Uniform asymmetric-anchor templates: a limitation

October 11, 2026. **Verified construction-specific limitation.**
The successful [3×4 candidate](three-by-four.md) uses nonuniform anchor
entries and is outside this class. No global impossibility is asserted.

Start with one prefix anchor row block (size 2m) and two prefix anchor
column blocks (size m each) per inherited propagation mode. Keep the
global W−,W+,V order and the original tree orders. A candidate is any
of the 256 borders

\[
 H=\begin{pmatrix}a&b&c&d\\x&y&1&0\\z&w&1&1\end{pmatrix}.
\]

In each mode prescribe the corner (a,b), row-role codes (x,y),(z,w),
and column-role values c,d. Five additional fixed bits specify the
two nonrole row-code bits, the nonrole column value, and the two
off-mode corner values. There are 32 such fills for each H.

Nonanchor dummy incidences stay one. Same-sign same-level and
child-to-parent threshold matrices stay as in the original host.
All other nonanchor variable entries have a fixed background β∈{0,1}.
This gives exactly 256×32×2=16,384 templates.

The [certificate](../verification/reference/asymmetric-template-certificates.json)
contains 3,579 explicit ordered quotient-copy witnesses. Each records
all fills it covers. Together they cover every template. The witnesses
use only modes with indices at most four and nonleaf variable blocks
at depths at most three. The
[independent checker](../verification/check_asymmetric.py) reconstructs
both axes and every entry without importing discovery code or a solver.
It verifies the entire parameter space, all selected entries, order,
and twin multiplicities. Its [report](../verification/reference/asymmetric-template-report.json)
records complete coverage.

These finite certificates imply an all-depth lower bound. At every h≥5,
the selected named blocks retain their relative orders and entries;
additional modes and deeper nodes do not alter them. Each selected block
has at least m/8 positions. If k≤4 distinct physical positions are chosen
from one repeated block of weight w≥4, then

\[
 \binom wk\ge(w/k)^k\ge(m/32)^k.
\]

Multiplying over all selected blocks yields at least (m/32)^7 ordered H
copies. Hence, with n=(14h+2)m and the inherited certified distance
ε_h=(14h+2)^−2, every template has

\[
 N_H(A_h)/n^7\ge32^{-7}(14h+2)^{-7}
 =32^{-7}\epsilon_h^{7/2}.
\]

Thus none gives a superpolynomially sparse copy estimate at this
certified distance. This does not give an upper bound on its actual
distance, and does not exclude other choices of anchors, entries,
orders, propagation bodies, or distance arguments. In particular the
new candidate's W-dummy entries and parity-dependent odd-minus entries
are deliberately outside the five-bit fill model.

Reproduce with Python's standard library:

```sh
python3 experiments/certify_asymmetric_templates.py --output .context/asymmetric-certificates.json
python3 verification/check_asymmetric.py
```

Separate exploratory SAT runs allowed arbitrary unused anchor entries.
Their SAT/UNSAT outcomes were discovery aids, not premises of this
certificate theorem or the new removal theorem. In particular solver
round limits are not impossibility results.
