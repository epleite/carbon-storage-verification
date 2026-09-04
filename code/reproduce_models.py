#!/usr/bin/env python3
"""Recompute supplementary leave-one-site-out diagnostic models."""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score,brier_score_loss

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; OUT=ROOT/'reproduced'; OUT.mkdir(exist_ok=True)
a=pd.read_csv(DATA/'monitoring_architecture.csv',encoding='utf-8-sig')
a=a[~a.B1.astype(bool)].reset_index(drop=True)
physical=a.union_enh_recode.to_numpy(float); age=np.log1p(a.operational_age_y.to_numpy(float)); top=a.topology_breadth.to_numpy(float); mandatory=a.mandatory_public_route.to_numpy(float)

def loocv(X,y):
    X=np.asarray(X,float); y=np.asarray(y,int); pred=np.zeros(len(y))
    for i in range(len(y)):
        tr=np.ones(len(y),bool); tr[i]=False; Xtr=X[tr].copy(); Xte=X[[i]].copy(); cont=[]
        for j in range(X.shape[1]):
            vals=set(np.unique(X[:,j]).tolist())
            if not (vals.issubset({0.0,1.0}) and len(vals)<=2): cont.append(j)
        if cont:
            sc=StandardScaler().fit(Xtr[:,cont]); Xtr[:,cont]=sc.transform(Xtr[:,cont]); Xte[:,cont]=sc.transform(Xte[:,cont])
        m=LogisticRegression(C=1.0,solver='lbfgs',max_iter=10000).fit(Xtr,y[tr]); pred[i]=m.predict_proba(Xte)[0,1]
    return float(roc_auc_score(y,pred)),float(brier_score_loss(y,pred))

specs={'Physical only':physical[:,None],'Age only':age[:,None],'Topology only':top[:,None],'Age + topology':np.c_[age,top],'Physical + age':np.c_[physical,age],'Physical + age + topology':np.c_[physical,age,top],'Age + topology + mandatory route':np.c_[age,top,mandatory]}
rows=[]
for col,label in [('K3_E2plus','K3'),('K4_E2plus','K4')]:
    y=a[col].astype(int).to_numpy()
    for n,X in specs.items():
        auc,brier=loocv(X,y); rows.append({'outcome':label,'model':n,'LOOCV_AUC':auc,'LOOCV_Brier':brier})
pd.DataFrame(rows).to_csv(OUT/'small_sample_model_diagnostics.csv',index=False)
print('Wrote',OUT/'small_sample_model_diagnostics.csv')
