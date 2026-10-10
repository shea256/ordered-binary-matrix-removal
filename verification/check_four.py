#!/usr/bin/env python3
"""Exact census and boundary checks for the candidate 4x4 obstruction.

The full census assumes neither anchor rigidity nor copy localization.
Twin blocks are weighted exactly; distinct pattern rows/columns prohibit
repeated representatives of a block. Same-agent evidence, not peer review.
"""
import itertools
import json
from collections import defaultdict
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from host import Position, entry, nonanchors
from refine_anchor import axis, crown, bits, refined_modes
from check_refinement import check_crown, check_laminar
from check_adversarial import propagation_cases
from check_compression import check_incidence_and_sampling

S=crown(2)
H=[[0,1,1,0],[1,0,0,1],[1,0,1,0],[0,1,1,1]]


def closed_count(h):
    m=2**h
    return 2*m**6 if h==1 else (33*m**6-58*m**5)//4


def direct_count(h):
    """Independent integer node-pair sum, with actual block multiplicities."""
    m=2**h
    families=defaultdict(int)
    for p in range(m):
        b,d=divmod(p,2)
        for e in (0,1):
            q2=2*b+e
            for q1 in range(e,p,2):
                if q1<q2 and p<=q2:
                    families['leaf_plus']+=1
                    if e<=d:
                        families['leaf_minus']+=1
            for a in range(b):
                # Two parent-plus modes, one for each e; positions weigh 2x2.
                families['parent_full']+=4
                if h>=2 and a%2==e and b%2==e:
                    families['parent_half']+=4
    extra=2*m**4*sum(families.values())
    count=2*m**6+extra
    assert count==closed_count(h)
    assert 4*count<=33*m**6
    return {'h':h,'m':m,'n':(14*h+2)*m,'canonical_copies':2*m**6,
            'additional_copies':extra,'total_copies':count,
            'pair_counts_by_family':dict(families)}


def full_census(h):
    rs,cs=axis(h,2,'row'),axis(h,2,'column')
    assert sum(x.weight for x in rs)==sum(x.weight for x in cs)==(14*h+2)*2**h
    masks=[sum(entry(r,c,S)<<j for j,c in enumerate(cs)) for r in rs]
    full=(1<<len(cs))-1
    groups=defaultdict(lambda:{'quotient_copies':0,'weighted_copies':0})
    old_hitting_set_failure=None
    rowsets=0
    for ix in itertools.combinations(range(len(rs)),4):
        rowsets+=1
        candidates=[]
        for signature in zip(*H):
            mask=full
            for v,i in zip(signature,ix):
                mask &= masks[i] if v else full^masks[i]
            if not mask: break
            candidates.append(mask)
        if len(candidates)!=4: continue
        def columns(k,start,chosen):
            if k==4:
                yield chosen
                return
            for j in bits(candidates[k]>>start):
                j+=start
                yield from columns(k+1,j+1,chosen+[j])
        for js in columns(0,0,[]):
            R,C=[rs[i] for i in ix],[cs[j] for j in js]
            assert [[entry(r,c,S) for c in C] for r in R]==H
            a,b=sum(r.kind=='anchor' for r in R),sum(c.kind=='anchor' for c in C)
            assert (a,b) in ((2,2),(2,1))
            assert R[2].kind==C[3].kind=='variable'
            assert R[2].depth==h and C[3].depth==h-1
            assert C[3].sign=='-' and C[3].node==R[2].node//2
            assert R[3].kind=='dummy'
            label='balanced' if b==2 else 'unbalanced'
            if b==1:
                p=R[2].node
                assert R[1].mode==C[0].mode==('W',h,'-',p%2)
                assert R[1].group==1 and C[0].group==0
                kind,i,sign,e=R[0].mode
                assert kind=='W'
                if C[2].depth==h:
                    assert i==h and R[0].group==(1 if sign=='+' else 0)
                    label='leaf_plus' if sign=='+' else 'leaf_minus'
                else:
                    assert C[2].depth==h-1 and C[2].sign=='+'
                    assert sign=='+'
                    assert (i,R[0].group) in ((h,0),(h-1,1))
                    label='parent_full' if i==h else 'parent_half'
            weight=1
            for x in R+C: weight*=x.weight
            groups[label]['quotient_copies']+=1
            groups[label]['weighted_copies']+=weight
            hits=[(i,j) for i,r in enumerate(R) for j,c in enumerate(C)
                  if r.kind==c.kind=='variable' and r.depth==c.depth==h and r.node==c.node]
            if not hits and old_hitting_set_failure is None:
                old_hitting_set_failure={'rows':[vars(r) for r in R], 'columns':[vars(c) for c in C]}
    total=sum(g['weighted_copies'] for g in groups.values())
    assert total==closed_count(h)
    direct=direct_count(h)
    assert groups['balanced']['weighted_copies']==direct['canonical_copies']
    for family,pairs in direct['pair_counts_by_family'].items():
        assert groups[family]['weighted_copies']==2*(2**h)**4*pairs
    return {'h':h,'quotient_axis_size':len(rs),'row_quadruples_checked':rowsets,
            'total_copies':total,'groups':dict(groups),'parent_zero_localization_failures':0,
            'old_leaf_diagonal_hitting_set_counterexample':old_hitting_set_failure}


def tree_order_check(h):
    cols=nonanchors(h,'column')
    index={(c.depth,c.sign,c.node):j for j,c in enumerate(cols) if c.kind=='variable'}
    checked=0
    for i in range(1,h+1):
        for sign in ('+', '-') if i<h else ('L',):
            for q in range(2**i):
                child=index[i,sign,q]
                for b in range(2**(i-1)):
                    assert (child<index[i-1,'+',b])==(q//2<b)
                    assert (index[i-1,'-',b]<child)==(b<q//2)
                    checked+=2
    for j in range(h):
        for a,b in itertools.product(range(2**j),repeat=2):
            assert (index[j,'+',a]<index[j,'-',b])==(a<=b)
            assert (index[j,'-',a]<index[j,'+',b])==(a<b)
            checked+=2
    return {'h':h,'strict_order_comparisons':checked}


def reversed_minus_parity_witness():
    """Reversing the two minus parity modes permits a nonleaf copy."""
    h=3
    ts=refined_modes(h)
    for i in range(1,h+1):
        a,b=ts.index(('W',i,'-',0)),ts.index(('W',i,'-',1))
        ts[a],ts[b]=ts[b],ts[a]
    def bad_axis(name):
        return [Position('anchor',mode=t,group=g,weight=2**h)
                for t in ts for g in range(2)]+nonanchors(h,name)
    rs,cs=bad_axis('row'),bad_axis('column')
    def anchor(xs,t,g):
        return next(x for x in xs if x.kind=='anchor' and x.mode==t and x.group==g)
    def variable(xs,i,p):
        return next(x for x in xs if x.kind=='variable' and
                    (x.depth,x.sign,x.node)==(i,'-',p))
    R=[anchor(rs,('W',2,'-',1),0),anchor(rs,('W',2,'-',0),1),
       variable(rs,2,2),next(x for x in rs if x.kind=='dummy')]
    C=[anchor(cs,('W',2,'-',0),0),variable(cs,2,1),variable(cs,2,3),variable(cs,1,1)]
    assert [rs.index(x) for x in R]==sorted(rs.index(x) for x in R)
    assert [cs.index(x) for x in C]==sorted(cs.index(x) for x in C)
    assert [[entry(r,c,S) for c in C] for r in R]==H
    assert all(x.kind!='variable' or x.depth<h for x in R+C)
    weight=1
    for x in R+C: weight*=x.weight
    assert weight==(2**h)**8//128
    return {'h':h,'rows':[vars(x) for x in R],'columns':[vars(x) for x in C],
            'weighted_copies_in_this_family':weight,
            'scope':'Counterexample to localization if minus parity modes are reversed; all chosen depths are fixed below the leaves.'}


if __name__=='__main__':
    assert len(set(map(tuple,H)))==len(set(zip(*H)))==4
    report={'pattern':H,'anchor':S,
            'full_census':[full_census(h) for h in range(1,5)],
            'independent_node_pair_counts':[direct_count(h) for h in range(1,9)],
            'tree_orders':[tree_order_check(h) for h in range(1,6)],
            'reversed_minus_parity_counterexample':reversed_minus_parity_witness(),
            'crown_exclusion':[check_crown(h) for h in range(1,6)],
            'laminar_supports':[check_laminar(h) for h in range(1,9)],
            'arbitrary_path_edits':propagation_cases(),
            'sampling':[check_incidence_and_sampling(h) for h in range(1,9)],
            'scope':'Exact finite evidence and a separate combinatorial count; no independent review or Lean proof. Universal argument: proofs/four-by-four.md.'}
    print(json.dumps(report,indent=2))
