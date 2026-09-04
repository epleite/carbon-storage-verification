#!/usr/bin/env python3
"""Recompute the four independent ambiguity-bound combinations."""
from pathlib import Path
import pandas as pd
import numpy as np
import itertools

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=ROOT/'reproduced'
OUT.mkdir(exist_ok=True)

scores=pd.read_csv(DATA/'final_evidence_scores.csv',encoding='utf-8-sig')
site=pd.read_csv(DATA/'recoded_site_results.csv',encoding='utf-8-sig')
amb=pd.read_csv(DATA/'evidence_ambiguity_bounds.csv',encoding='utf-8-sig')

axes=['K2','K3','K4']
assets=site.asset_id.tolist()
final={(r.asset_id,'K2'):int(r.k2) for _,r in scores.iterrows()}
final.update({(r.asset_id,'K3'):int(r.k3) for _,r in scores.iterrows()})
final.update({(r.asset_id,'K4'):int(r.k4) for _,r in scores.iterrows()})

# Current threshold-crossing ambiguity is only A15 K2 and A12 K4.
combos=[('K2-low__K4-low',1,1),('adjudicated',2,1),('worst-gap',1,2),('K2-high__K4-high',2,2)]

maturity=dict(zip(site.asset_id,site.maturity))
operation=dict(zip(site.asset_id,site.operation))
physical=dict(zip(site.asset_id,site.union_enh_recode))
is_b1=dict(zip(site.asset_id,site.B1))
age={a:(2026+8/12)-operation[a] for a in assets}
sed=[a for a in assets if not bool(is_b1[a])]
mature_sed=[a for a in sed if maturity[a]=='mature_primary']
mature_all=[a for a in assets if maturity[a]=='mature_primary']

def exact_binary_difference(values,labels):
    values=np.asarray(values,float); labels=np.asarray(labels,bool)
    obs=float(values[labels].mean()-values[~labels].mean())
    vals=[]
    for comb in itertools.combinations(range(len(labels)),int(labels.sum())):
        g=np.zeros(len(labels),bool); g[list(comb)]=True
        vals.append(float(values[g].mean()-values[~g].mean()))
    vals=np.asarray(vals)
    p=float(np.mean(np.abs(vals)>=abs(obs)-1e-12))
    return obs,p

rows=[]
for label,a15,a12 in combos:
    d=final.copy(); d[('A15','K2')]=a15; d[('A12','K4')]=a12
    r={'scenario':label,'A15_K2':a15,'A12_K4':a12}
    for ax in axes:
        n=sum(d[(a,ax)]>=2 for a in assets)
        r[f'{ax}_E2plus_n']=n; r[f'{ax}_E2plus_pct']=100*n/15
    r['K2_minus_K3_pp']=r['K2_E2plus_pct']-r['K3_E2plus_pct']
    r['K2_minus_K4_pp']=r['K2_E2plus_pct']-r['K4_E2plus_pct']
    r['mature_complete_n']=sum(all(d[(a,ax)]>=2 for ax in axes) for a in mature_all)
    r['mature_complete_pct']=100*r['mature_complete_n']/len(mature_all)
    for ax in ('K3','K4'):
        y=np.array([d[(a,ax)]>=2 for a in sed]); x=np.array([physical[a] for a in sed],float)
        for q in (0.4,0.5,0.6): r[f'{ax}_mismatch_q{q:.1f}_n']=int(np.sum((x>=q)!=y))
        ym=np.array([d[(a,ax)]>=2 for a in mature_sed]); xm=np.array([physical[a] for a in mature_sed],float)
        dp,pp=exact_binary_difference(xm,ym)
        r[f'{ax}_mature_physical_delta']=dp; r[f'{ax}_mature_physical_exact_p']=pp
        av=np.array([age[a] for a in sed],float); da,pa=exact_binary_difference(av,y)
        r[f'{ax}_time_in_operation_delta_y']=da; r[f'{ax}_time_in_operation_exact_p']=pa
    rows.append(r)

pd.DataFrame(rows).to_csv(OUT/'ambiguity_sensitivity_results.csv',index=False)
print('Wrote',OUT/'ambiguity_sensitivity_results.csv')
