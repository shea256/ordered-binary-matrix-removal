#!/usr/bin/env python3
"""Counterexample-guided finite completions of asymmetric protected frames.

This is discovery only. A SAT model is not an all-depth removal construction.
Each no-copy clause retains a literal ordered occurrence for independent audit.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
from host import role
from search_asymmetric import body_entry, distinct_copy, patterns, word
from search_asymmetric_templates import axes


def copy_batch(H, matrix, limit=64, allowed=None):
    full=(1<<len(matrix[0]))-1
    masks=[sum(bit<<j for j,bit in enumerate(row)) for row in matrix]
    result=[]
    for ix in combinations(range(len(matrix)),3):
        candidates=[]
        for signature in zip(*H):
            mask=full
            for i,bit in zip(ix,signature):
                mask &= masks[i] if bit else full ^ masks[i]
            if not mask:break
            candidates.append(mask)
        if len(candidates)!=4:continue
        def visit(prefix):
            if len(prefix)==4:
                if allowed is not None and allowed(ix, prefix):
                    return False
                result.append({'rows':list(ix),'columns':prefix})
                return len(result)>=limit
            mask=candidates[len(prefix)]
            if prefix:mask=(mask>>(prefix[-1]+1))<<(prefix[-1]+1)
            while mask:
                bit=mask & -mask;j=bit.bit_length()-1;mask-=bit
                if visit(prefix+[j]):return True
            return False
        if visit([]):return result
    return result


def frame(H, levels=3, order='global', background=0, free_body=False, off_corner=None, full=False):
    rows,cols=axes(levels,'row',order,full),axes(levels,'column',order,full)
    matrix,free=[],[]
    for i,r in enumerate(rows):
        line=[]
        for j,c in enumerate(cols):
            bit=None
            if r.kind==c.kind=='anchor':
                if r.mode==c.mode:bit=H[0][c.group]
                elif off_corner is not None:bit=int(off_corner[c.group])
            elif r.kind=='anchor':
                k=role(c,r.mode,'column')
                if k:bit=H[0][k+1]
            elif c.kind=='anchor':
                k=role(r,c.mode,'row')
                if k:bit=H[k][c.group]
            else:
                fixed=(not free_body or r.kind=='dummy' or c.kind=='dummy'
                       or (r.sign==c.sign and
                           ((r.depth==c.depth and r.node==c.node)
                            or (r.depth==c.depth+1 and r.node//2==c.node))))
                if fixed:bit=body_entry(r,c,background)
            if bit is None:free.append((i,j))
            line.append(bit)
        matrix.append(line)
    return rows,cols,matrix,free


def solve(H,levels=3,order='global',background=0,free_body=False,max_rounds=1000,off_corner=None,full=False,localize_zero=False):
    import z3
    rows,cols,fixed,free=frame(H,levels,order,background,free_body,off_corner,full)
    assert not localize_zero or full
    def allowed(ix,jx):
        r,c=rows[ix[1]],cols[jx[3]]
        return r.kind==c.kind=='variable' and r.sign=='L' and c.sign=='-' and c.depth==levels-1 and r.node//2==c.node
    vs=[z3.Bool('x'+str(k)) for k in range(len(free))]
    ids={ij:k for k,ij in enumerate(free)}
    solver=z3.Solver();solver.set(timeout=10000)
    cuts=[];start=time.monotonic()
    for step in range(max_rounds):
        result=solver.check()
        if result!=z3.sat:
            return {'pattern':H,'status':str(result),'cuts':cuts,'free_cells':free,'seconds':time.monotonic()-start}
        model=solver.model()
        assignment=[int(z3.is_true(model.eval(x,model_completion=True))) for x in vs]
        A=[[v if v is not None else assignment[ids[i,j]] for j,v in enumerate(row)] for i,row in enumerate(fixed)]
        witnesses=copy_batch(H,A,allowed=allowed if localize_zero else None)
        if not witnesses:
            return {'pattern':H,'status':'sat','cuts':cuts,'free_cells':free,'assignment':assignment,'seconds':time.monotonic()-start}
        for witness in witnesses:
            literals={ids[ri,cj]:1-H[i][j]
                      for i,ri in enumerate(witness['rows']) for j,cj in enumerate(witness['columns']) if (ri,cj) in ids}
            clause=sorted(k+1 if v else -k-1 for k,v in literals.items())
            cuts.append({'witness':witness,'clause':clause})
            solver.add(z3.Or(*[vs[k] if v else z3.Not(vs[k]) for k,v in literals.items()]))
    return {'pattern':H,'status':'round_limit','cuts':cuts,'free_cells':free,'seconds':time.monotonic()-start}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--candidates',required=True)
    ap.add_argument('--levels',type=int,default=3)
    ap.add_argument('--order',choices=('global','within','erebos'),default='global')
    ap.add_argument('--background',type=int,choices=(0,1),default=0)
    ap.add_argument('--free-body',action='store_true')
    ap.add_argument('--off-corner',choices=('00','01','10','11'))
    ap.add_argument('--full-host',action='store_true')
    ap.add_argument('--localize-zero',action='store_true')
    ap.add_argument('--max-rounds',type=int,default=1000)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    allowed=set(json.loads(Path(args.candidates).read_text()))
    checks=[]
    for H in patterns():
        if word(H) not in allowed:continue
        item=solve(H,args.levels,args.order,args.background,args.free_body,args.max_rounds,args.off_corner,args.full_host,args.localize_zero)
        checks.append(item)
        print(json.dumps({'pattern':word(H),'status':item['status'],'cuts':len(item['cuts']),
                          'seconds':round(item['seconds'],3)}),flush=True)
        # Keep a checkpoint if a later candidate needs a long search.
        Path(args.output).write_text(json.dumps({'scope':'Finite CSP discovery; incomplete until completed=true.',
            'levels':args.levels,'order':args.order,'background':args.background,'free_body':args.free_body,
            'off_corner':args.off_corner,'full_host':args.full_host,'localize_zero':args.localize_zero,'completed':False,'checks':checks},indent=2)+'\n')
    report={'scope':'Finite CSP discovery, not a universal theorem or certified SAT verdict.',
            'levels':args.levels,'order':args.order,'background':args.background,'free_body':args.free_body,
            'off_corner':args.off_corner,'full_host':args.full_host,'localize_zero':args.localize_zero,'completed':True,'checks':checks}
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'statuses':dict(Counter(x['status'] for x in checks))}),flush=True)


if __name__=='__main__':main()
