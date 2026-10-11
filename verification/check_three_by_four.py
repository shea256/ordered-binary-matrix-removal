#!/usr/bin/env python3
"""Independent literal host and weighted subsequence census for the 3x4 draft.

No discovery imports or SAT dependency. Finite checks support, but do not
replace, the all-depth proof in proofs/three-by-four.md.
"""
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from check_three import anchor, body, dummy, key, role, var

H = [[1,0,0,1], [1,0,1,0], [0,1,1,1]]
SIGS = list(zip(*H))


def axis(h, name):
    modes = ([('W', i, '-', p) for i in range(1,h+1) for p in (0,1)]
             + [('W', i, '+', p) for i in range(1,h+1) for p in (0,1)]
             + [('V', i, s, -1) for i in range(1,h+1) for s in ('+','-')])
    anchors = [anchor(t,j) for t in modes for j in range(1 if name == 'row' else 2)]
    tail = [var(i,s,p) for i in range(h) for s in ('+','-') for p in range(2**i)]
    tail += [var(h,'L',p) for p in range(2**h)] + [dummy()]
    return anchors + sorted(tail,key=lambda x:key(x,name))


def weight(x,h,name):
    if x['kind'] == 'variable':
        return 2**(h-x['depth'])
    return 2**h*(2 if x['kind']=='anchor' and name=='row' else 1)


def entry(r,c,omit_dummy=False,omit_odd=False):
    if r['kind'] == c['kind'] == 'anchor':
        return int(r['mode']==c['mode'] and c['group']==0)
    if c['kind']=='anchor':
        return int(role(r,c['mode'],'row')==c['group']+1)
    if r['kind']!='anchor':
        return body(r,c)
    kind,i,sign,parity = r['mode']
    if c['kind']=='dummy':
        return int(kind=='W' and not omit_dummy)
    depth,csign,node = c['depth'],c['sign'],c['node']
    if kind=='V':
        return int(depth==i-1 and csign==sign)
    if sign=='+':
        return int(depth==i and csign in ('+','L') and node%2==parity)
    return int((depth==i-1 and csign=='-') or
               (not omit_odd and parity==0 and depth==i and csign=='-' and node%2==1))


def bits(mask):
    while mask:
        bit=mask & -mask
        yield bit.bit_length()-1
        mask-=bit


def census(h,physical=False,omit_dummy=False,omit_odd=False):
    rows,cols=axis(h,'row'),axis(h,'column')
    if physical:
        rows=[x for x in rows for _ in range(weight(x,h,'row'))]
        cols=[x for x in cols for _ in range(weight(x,h,'column'))]
    rw=[1 if physical else weight(x,h,'row') for x in rows]
    cw=[1 if physical else weight(x,h,'column') for x in cols]
    A=[[entry(r,c,omit_dummy,omit_odd) for c in cols] for r in rows]
    full=(1<<len(cols))-1
    masks=[sum(v<<j for j,v in enumerate(row)) for row in A]
    count=bad=0; by_config=defaultdict(int)
    for ix in combinations(range(len(rows)),3):
        possible=[]
        for signature in SIGS:
            mask=full
            for i,v in zip(ix,signature):
                mask &= masks[i] if v else full ^ masks[i]
            if not mask:break
            possible.append(mask)
        if len(possible)!=4:continue
        # Dynamic programming counts weighted increasing column subsequences.
        # State key is (last column block, number of anchor columns).
        dp={(j,int(cols[j]['kind']=='anchor')):cw[j] for j in bits(possible[0])}
        for stage in range(1,4):
            nxt={}; previous=sorted(dp.items()); p=0; prefix=defaultdict(int)
            for j in bits(possible[stage]):
                while p<len(previous) and previous[p][0][0]<j:
                    (_,b),ways=previous[p];prefix[b]+=ways;p+=1
                for b,ways in prefix.items():
                    if ways:nxt[j,b+int(cols[j]['kind']=='anchor')]=ways*cw[j]
            dp=nxt
            if not dp:break
        a=sum(rows[i]['kind']=='anchor' for i in ix)
        multiplicity=rw[ix[0]]*rw[ix[1]]*rw[ix[2]]
        for (j,b),ways in dp.items():
            ways*=multiplicity;count+=ways;by_config[str((a,b))]+=ways
            r,c=rows[ix[1]],cols[j]
            localized=(r['kind']==c['kind']=='variable' and r['sign']=='L'
                       and c['sign']=='-' and c['depth']==h-1 and r['node']//2==c['node'])
            if not localized:bad+=ways
            if not (omit_dummy or omit_odd):
                assert a==1 and b in (1,2)
                assert rows[ix[0]]['mode'][:3]==('W',h,'-')
                assert rows[ix[2]]['kind']=='dummy'
    n=sum(rw)
    assert n==sum(cw)==(14*h+2)*2**h
    return {'h':h,'n':n,'copies':count,'bad_localization_copies':bad,
            'by_anchor_counts':dict(by_config)}


def check_designated_extensions(h):
    rows,cols=axis(h,'row'),axis(h,'column')
    tested=0
    for ar in rows:
        if ar['kind']!='anchor':continue
        t=ar['mode'];ac=[anchor(t,0),anchor(t,1)]
        assert [entry(ar,c) for c in ac]==H[0][:2]
        for r in rows:
            if r['kind']=='anchor':continue
            j=role(r,t,'row')
            if j:
                assert [entry(r,c) for c in ac]==H[j][:2];tested+=1
        for c in cols:
            if c['kind']=='anchor':continue
            j=role(c,t,'column')
            if j:assert entry(ar,c)==H[0][j+1];tested+=bool(j)
    return tested


def main():
    results=[]
    for h in range(1,7):
        result=census(h)
        assert result['bad_localization_copies']==0
        assert result['copies']<=2*(2**h)*result['n']**5
        result['designated_role_checks']=check_designated_extensions(h)
        results.append(result)
    physical=census(1,physical=True)
    assert physical=={k:v for k,v in results[0].items() if k!='designated_role_checks'}
    controls={'without_W_dummy_ones':census(2,omit_dummy=True),
              'without_odd_minus_ones':census(2,omit_odd=True)}
    assert all(x['bad_localization_copies']>0 for x in controls.values())
    print(json.dumps({'status':'passed','pattern':H,'results':results,
                      'physical_depth_one':physical,'negative_controls':controls,
                      'scope':'Exact finite checks from an independent implementation; not Lean or peer review.'},indent=2))


if __name__=='__main__':main()
