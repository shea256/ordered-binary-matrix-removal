#!/usr/bin/env python3
"""Exact searches for smaller role-encoded patterns, with weighted twins.

An unexpected copy is not automatically a disproof. A shallow all-nonleaf
copy has weight proportional to m^(r+c) and rules out the desired sparse
sequence for this unchanged host.
"""
from itertools import combinations, combinations_with_replacement
from math import comb
import argparse, json, sys
sys.dont_write_bytecode = True
from host import entry
from refine_anchor import axis, crown, bits


def pattern(S, row_sigs=None, col_sigs=None):
    r,c = len(S),len(S[0])
    row_sigs = row_sigs or [[int(i==j) for i in range(c)] for j in range(2)]
    col_sigs = col_sigs or [[int(i==j) for i in range(r)] for j in range(2)]
    return [row+[col_sigs[j][i] for j in range(2)] for i,row in enumerate(S)]+[
        row_sigs[0]+[1,0],row_sigs[1]+[1,1]]


def search(H, rows, cols, value, h, only_shallow=False, stop_on_shallow=False):
    nr,nc = len(H),len(H[0])
    if only_shallow:
        rows = [x for x in rows if x.kind != 'variable' or x.depth < h]
        cols = [x for x in cols if x.kind != 'variable' or x.depth < h]
    full = (1 << len(cols))-1
    masks = [sum(value(r,c) << j for j,c in enumerate(cols)) for r in rows]
    signatures = list(zip(*H))
    unique_rows = len(set(map(tuple,H))) == nr
    row_choices = combinations(range(len(rows)),nr) if unique_rows else combinations_with_replacement(range(len(rows)),nr)
    total, count, sets, witness = 0,0,0,None
    for ix in row_choices:
        # Repeated representatives require identical pattern rows and enough
        # actual positions. Each quotient block is consecutive on the axis.
        row_weight = 1
        for i in set(ix):
            times = ix.count(i)
            if times > rows[i].weight:
                row_weight=0; break
            row_weight *= comb(rows[i].weight,times)
        if not row_weight:
            continue
        sets += 1
        candidate=[]
        for sig in signatures:
            mask=full
            for v,i in zip(sig,ix):
                mask &= masks[i] if v else full^masks[i]
            if not mask: break
            candidate.append(mask)
        if len(candidate)!=nc: continue
        dp=[1]+[0]*nc
        for j,c in enumerate(cols):
            old=dp[:]
            for k in range(nc):
                if not old[k]: continue
                for times in range(1,min(c.weight,nc-k)+1):
                    if any(not ((candidate[t]>>j)&1) for t in range(k,k+times)):
                        break
                    dp[k+times] += old[k]*comb(c.weight,times)
            # A separate existence search is only needed for the witness.
        if not dp[nc]: continue
        total += row_weight*dp[nc]
        count += 1
        if witness is None and all(r.kind!='variable' or r.depth<h for r in (rows[i] for i in ix)):
            def find(k, start, chosen):
                if k==nc: return chosen
                for j in bits(candidate[k] >> start):
                    j+=start
                    if cols[j].kind=='variable' and cols[j].depth==h: continue
                    # For the shallow certificate use distinct quotient blocks.
                    result=find(k+1,j+1,chosen+[j])
                    if result is not None: return result
                return None
            js=find(0,0,[])
            if js is not None:
                witness={'rows':[vars(rows[i]) for i in ix], 'columns':[vars(cols[j]) for j in js],
                         'matrix':H}
                if stop_on_shallow:
                    return {'h':h,'shallow_copy':witness,'row_choices_until_witness':sets}
    return {'h':h,'copies':total,'row_choices':sets,'positive_row_choices':count,'shallow_copy':witness}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--max-depth',type=int,default=3)
    p.add_argument('--shallow',action='store_true')
    args=p.parse_args()
    S=crown(2); H=pattern(S)
    report={'pattern':H,'hosts':[]}
    for h in range(1,args.max_depth+1):
        rows,cols=axis(h,2,'row'),axis(h,2,'column')
        report['hosts'].append(search(H,rows,cols,lambda r,c:entry(r,c,S),h,
                                      only_shallow=args.shallow,stop_on_shallow=args.shallow))
    print(json.dumps(report,indent=2))
