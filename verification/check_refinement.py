#!/usr/bin/env python3
"""Exact finite checks for the reordered 3-anchor / 5-pattern candidate.

Uses full ordered embedding searches, plus a separate symbolic description
of role supports. Same-agent checks are not independent peer review.
"""
import itertools
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from host import entry, nonanchors, role
from refine_anchor import axis, bits, check_three, crown, refined_modes
from check_compression import check_bodies, check_incidence_and_sampling
from check_adversarial import propagation_cases, threshold_cases

H = [[0,1,1,1,0], [1,0,1,0,1], [1,1,0,0,0],
     [1,0,0,1,0], [0,1,0,1,1]]


def check_crown(h):
    rs, cs = nonanchors(h, 'row'), nonanchors(h, 'column')
    masks = [sum(entry(r,c,crown(3)) << i for i,r in enumerate(rs)) for c in cs]
    full = (1 << len(rs))-1
    checked = 0
    for a,b,c in itertools.combinations(masks,3):
        assert not (a & b & (full^c) and a & (full^b) & c and (full^a) & b & c)
        checked += 1
    return {'h':h, 'column_triples':checked, 'nonanchor_crowns':0}


def support_descriptor(t, j, name, h):
    # Literal mode table, independently encoded using whole/half classes.
    kind, i, sign, parity = t
    if kind == 'V':
        if name == 'column':
            return ('dummy',) if j == 1 else (i-1, sign, None)
        child = (j == 1) if sign == '+' else (j == 2)
        depth = i if child else i-1
        return (depth, 'L' if depth == h else sign, None)
    if name == 'row':
        return (i, 'L' if i == h else sign, parity) if j == 1 else ('dummy',)
    child = (j == 2) if sign == '+' else (j == 1)
    return (i, 'L' if i == h else sign, parity) if child else (i-1, sign, None)


def descriptor_contains(desc, x):
    if desc == ('dummy',):
        return x.kind == 'dummy'
    i, sign, parity = desc
    return (x.kind == 'variable' and x.depth == i and x.sign == sign
            and (parity is None or x.node % 2 == parity))


def check_laminar(h):
    total, strict = 0, 0
    for name in ('row','column'):
        ns = nonanchors(h, name)
        supports = []
        for index,t in enumerate(refined_modes(h)):
            pair = []
            for j in (1,2):
                actual = {q for q,x in enumerate(ns) if role(x,t,name) == j}
                expected = {q for q,x in enumerate(ns) if descriptor_contains(support_descriptor(t,j,name,h),x)}
                assert actual == expected and actual
                supports.append((index,t,j,actual))
                pair.append(actual)
            assert pair[0].isdisjoint(pair[1])
        for (i,t,j,a),(k,u,l,b) in itertools.combinations(supports,2):
            assert a.isdisjoint(b) or a <= b or b <= a
            if a < b:
                assert i < k  # the containing support comes later
                strict += 1
            if b < a:
                assert k < i  # impossible in this ordered enumeration
                strict += 1
            total += 1
    return {'h':h,'support_pairs':total,'strict_containments':strict}


def weighted_embedding_count(h):
    """Enumerate all distinct quotient row choices; count increasing columns.

    Distinct pattern rows/columns prohibit repeated twin representatives.
    This searches the full H, without using the anchor-localization theorem.
    """
    rs, cs = axis(h,3,'row'), axis(h,3,'column')
    masks = [sum(entry(r,c,crown(3)) << j for j,c in enumerate(cs)) for r in rs]
    full = (1 << len(cs))-1
    pattern_cols = list(zip(*H))
    total, quotient, rowsets = 0, 0, 0
    for ix in itertools.combinations(range(len(rs)),5):
        rowsets += 1
        selected = [masks[i] for i in ix]
        candidates = []
        for signature in pattern_cols:
            mask = full
            for bit, values in zip(signature,selected):
                mask &= values if bit else full^values
            if not mask:
                break
            candidates.append(mask)
        if len(candidates) != 5:
            continue
        # Count increasing distinct columns by weighted prefix dynamic programming.
        dp, raw = [1]+[0]*5, [1]+[0]*5
        for j,c in enumerate(cs):
            for k in range(4,-1,-1):
                if (candidates[k] >> j) & 1:
                    dp[k+1] += dp[k]*c.weight
                    raw[k+1] += raw[k]
        mult = 1
        for i in ix:
            mult *= rs[i].weight
        total += mult*dp[5]
        quotient += raw[5]
    assert total == 2*(2**h)**8, (h,total)
    return {'h':h,'row_quintuples_checked':rowsets,'quotient_H_copies':quotient,
            'weighted_H_copies':total,'expected':2*(2**h)**8}


def two_anchor_limitation():
    # Expand actual twin positions; every binary 2x2 anchor appears among
    # nonanchors already at depth 2. This blocks pure anchor rigidity there.
    rs = [r for r in nonanchors(2,'row') for _ in range(r.weight)]
    cs = [c for c in nonanchors(2,'column') for _ in range(c.weight)]
    values = [[entry(r,c,crown(3)) for c in cs] for r in rs]
    witnesses = {}
    for a,b in itertools.combinations(range(len(rs)),2):
        for c,d in itertools.combinations(range(len(cs)),2):
            word = ''.join(str(values[i][j]) for i,j in ((a,c),(a,d),(b,c),(b,d)))
            witnesses.setdefault(word,{'rows':[a,b],'columns':[c,d]})
    assert len(witnesses) == 16, witnesses
    return {'h':2,'all_binary_2x2_patterns':len(witnesses),'witnesses':witnesses,
            'scope':'No 2x2 anchor can have pure anchor rigidity in this unchanged nonanchor host; not a lower bound on all obstruction constructions.'}


if __name__ == '__main__':
    assert len(set(map(tuple,H))) == len(set(zip(*H))) == 5
    expected = [r + [int(i == 0),int(i == 1)] for i,r in enumerate(crown(3))]
    expected += [[1,0,0,1,0],[0,1,0,1,1]]
    assert H == expected
    report = {'pattern':H,
              'nonanchor_crown':[check_crown(h) for h in range(1,6)],
              'laminar_roles':[check_laminar(h) for h in range(1,9)],
              'anchor_embeddings':[check_three(h) for h in range(1,7)],
              'full_pattern_embeddings':[weighted_embedding_count(h) for h in (1,2)],
              'bodies':[check_bodies(h,3) for h in range(1,7)],
              'sampling':[check_incidence_and_sampling(h) for h in range(1,9)],
              'arbitrary_path_edits':propagation_cases(),
              'triangle_thresholds':threshold_cases(),
              'original_order_failure':check_three(2,False),
              'two_anchor_limitation':two_anchor_limitation(),
              'scope':'Exact finite checks; universal theorem depends on proofs/five-by-five.md. No independent review or Lean verification.'}
    print(json.dumps(report,indent=2))
