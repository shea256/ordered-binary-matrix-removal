#!/usr/bin/env python3
"""Screen structured asymmetric completions on a persistent nonleaf trunk."""
import argparse
from itertools import product
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode = True
from host import Position, nonanchors, role, modes
from search_three import find_copy
from search_asymmetric import body_entry, patterns, word


def axes(levels, axis, order='global', full=False):
    h = levels if full else levels+2
    ts = modes(levels)
    if order == 'global':
        ts.sort(key=lambda t: (0 if t[0]=='W' and t[2]=='-' else 1 if t[0]=='W' else 2,
                               t[1],t[3],t[2]))
    elif order == 'within':
        ts.sort(key=lambda t: (t[1],t[0]=='V',t[2]=='-',t[3]))
    elif order != 'erebos':
        raise ValueError(order)
    anchors = [Position('anchor',mode=t,group=j,weight=2**h*(2 if axis=='row' else 1))
               for t in ts for j in range(1 if axis=='row' else 2)]
    return anchors + [x for x in nonanchors(h,axis) if full or x.kind!='variable' or x.depth<levels]


def value(r,c,H,fill,background=0):
    # fill=(nonrole row code bit0, bit1, nonrole column bit,
    #       off-mode anchor corner bit0, bit1)
    if r.kind==c.kind=='anchor':
        return H[0][c.group] if r.mode==c.mode else fill[3+c.group]
    if r.kind=='anchor':
        j=role(c,r.mode,'column')
        return H[0][j+1] if j else fill[2]
    if c.kind=='anchor':
        i=role(r,c.mode,'row')
        return H[i][c.group] if i else fill[c.group]
    return body_entry(r,c,background)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--background',type=int,choices=(0,1),default=0)
    ap.add_argument('--order',choices=('global','within','erebos'),default='global')
    ap.add_argument('--candidates',help='JSON list of twelve-bit patterns')
    ap.add_argument('--levels',type=int,default=3)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    allowed=set(json.loads(Path(args.candidates).read_text())) if args.candidates else None
    rs,cs=axes(args.levels,'row',args.order),axes(args.levels,'column',args.order)
    results=[]
    start=time.monotonic()
    for H in patterns():
        if allowed is not None and word(H) not in allowed:
            continue
        for fill in product((0,1),repeat=5):
            matrix=[[value(r,c,H,fill,args.background) for c in cs] for r in rs]
            witness,checked=find_copy(H,rs,cs,matrix)
            results.append({'pattern':word(H),'fill':fill,'witness':witness,'row_choices':checked})
        print(json.dumps({'pattern':word(H),'surviving_fills':[x['fill'] for x in results[-32:] if x['witness'] is None]}),flush=True)
    Path(args.output).write_text(json.dumps({'scope':'Finite structured-template search, no all-depth theorem.',
        'order':args.order,'background':args.background,'mode_levels':args.levels,'variable_depth_max':args.levels-1,
        'rows':[vars(r) for r in rs],'columns':[vars(c) for c in cs],
        'results':results},indent=2)+'\n')
    print(json.dumps({'tested':len(results),'survivors':sum(x['witness'] is None for x in results),
                      'elapsed':time.monotonic()-start}),flush=True)


if __name__=='__main__':
    main()
