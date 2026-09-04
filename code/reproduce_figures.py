#!/usr/bin/env python3
"""Regenerate manuscript and supplementary figures from frozen derived CSV inputs."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "reproduced" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
arch = pd.read_csv(DATA / "archetype_physics.csv", encoding="utf-8-sig")
site = pd.read_csv(DATA / "recoded_site_results.csv", encoding="utf-8-sig")
topo = pd.read_csv(DATA / "monitoring_architecture.csv", encoding="utf-8-sig")
models = pd.read_csv(DATA / "small_sample_model_diagnostics.csv", encoding="utf-8-sig")

def save(fig, stem, tight=True):
    if tight:
        fig.tight_layout()
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

fig = plt.figure(figsize=(12, 6.3)); ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
boxes = [
(0.03,0.60,0.17,0.22,"1  Geology and storage","Can the formation accept\nand retain CO$_2$?"),
(0.24,0.60,0.18,0.22,"2  Measurement sensitivity","Would a specified measurement\nrespond to the subsurface change?"),
(0.47,0.60,0.18,0.22,"3  Monitoring design","Is the measurement acquired\nwith sufficient sensitivity?"),
(0.72,0.60,0.18,0.22,"4  Quantitative observation","Was a measurable change\nactually observed?"),
(0.72,0.18,0.18,0.22,"6  Public verification","Is the result documented\nquantitatively and auditable?"),
(0.47,0.18,0.18,0.22,"5  Time in operation","Has the system evolved long\nenough to test expectations?")]
for x,y,w,h,t,s in boxes:
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.012"))
    ax.text(x+w/2,y+h*0.65,t,ha="center",va="center",fontsize=10.6,fontweight="bold")
    ax.text(x+w/2,y+h*0.30,s,ha="center",va="center",fontsize=9.3)
def ar(x1,y1,x2,y2): ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="->",mutation_scale=14,linewidth=1.4))
ar(0.20,0.71,0.24,0.71); ar(0.42,0.71,0.47,0.71); ar(0.65,0.71,0.72,0.71); ar(0.81,0.60,0.81,0.40); ar(0.65,0.29,0.72,0.29); ar(0.56,0.40,0.56,0.60)
ax.text(0.22,0.86,"not the same as",fontsize=8.7,ha="center")
ax.text(0.695,0.49,"not the same as",fontsize=8.7,ha="center",rotation=90)
ax.text(0.50,0.065,"Reactive basalt is evaluated with a separate tracer and geochemical branch because mineralizing CO$_2$ is governed by different measurement physics.",ha="center",va="center",fontsize=9.5)
ax.set_title("Figure 1 | From geological storage to publicly verifiable subsurface behaviour",fontsize=14,pad=10)
save(fig,"Fig1_verification_system_framework",tight=False)

sed = site[site["B1"] == False].copy(); counts = sed["dominant"].value_counts().to_dict()
metrics=["amp","ts_std","union_std","ts_enh","union_enh"]
labels=["Amplitude","Travel-time\nchange\nstandard survey","Either signal\nstandard survey","Travel-time\nchange\nhigh-repeatability","Either signal\nhigh-repeatability"]
M=arch[metrics].to_numpy(float)
short={"A1":"Shallow porous offshore sandstone","A2":"Intermediate-depth offshore sandstone","A3":"Deep consolidated offshore sandstone","A4":"Shallow porous onshore sandstone","A5":"Intermediate-depth onshore sandstone","A6":"Deep stiff onshore sandstone","A7":"Thin or compartmentalized sandstone","A8":"Shaly heterogeneous sandstone","A9":"Porous fractured carbonate","A10":"Deep tight carbonate"}
ylabs=[f"{r.code}  {short[r.code]}  (sites: {counts.get(r.code,0)})" for _,r in arch.iterrows()]
fig,ax=plt.subplots(figsize=(10.8,7.1)); im=ax.imshow(M,aspect="auto",vmin=0,vmax=1)
ax.set_xticks(np.arange(len(labels)),labels); ax.set_yticks(np.arange(len(ylabs)),ylabs)
for i in range(M.shape[0]):
    for j in range(M.shape[1]): ax.text(j,i,f"{M[i,j]*100:.0f}%",ha="center",va="center",fontsize=8)
ax.set_title("Figure 2 | Predicted seismic detectability varies strongly among representative storage settings")
c=fig.colorbar(im,ax=ax,shrink=.78); c.set_label("Probability of exceeding the detection threshold")
save(fig,"Fig2_archetype_observability")

x=sed["union_enh_recode"].to_numpy(float); c3=sed["k3_e2plus"].astype(bool).to_numpy(); c4=sed["k4_e2plus"].astype(bool).to_numpy()
fig,ax=plt.subplots(figsize=(10.6,6.2))
ax.scatter(x,np.where(c3,1.08,0.08),marker="o",s=70,label="Observed behaviour compared quantitatively with expectations")
ax.scatter(x,np.where(c4,0.92,-0.08),marker="^",s=70,label="Quantitative evidence addressing containment")
off={"A14":(5,16),"A15":(5,-18),"A02":(4,14),"A05":(4,-18),"A10":(-18,15),"A08":(7,15),"A04":(4,16),"A12":(4,16)}
for i,aid in enumerate(sed["asset_id"]):
    yy=1.0 if (c3[i] or c4[i]) else 0.08; dx,dy=off.get(aid,(4,12)); ax.annotate(aid,(x[i],yy),xytext=(dx,dy),textcoords="offset points",fontsize=8)
for q,ls in [(0.4,"--"),(0.5,":"),(0.6,"-.")]: ax.axvline(q,linestyle=ls,linewidth=1)
ax.set_yticks([0,1],["Plan/narrative or limited quantitative evidence","Observed quantitative public evidence"])
ax.set_xlim(-.03,1.04); ax.set_ylim(-.25,1.35); ax.set_xlabel("Generic seismic detectability for the mapped geological setting")
ax.set_title("Figure 3 | Public subsurface evidence does not follow a simple seismic ranking"); ax.legend(loc="center right",fontsize=8.4)
save(fig,"Fig3_cross_axis_non_equivalence")

sedt=topo[topo["B1"]==False].copy(); age=sedt["operational_age_y"].to_numpy(float); phys=sedt["union_enh_recode"].to_numpy(float); breadth=sedt["topology_breadth"].to_numpy(float)
k3=sedt["K3_E2plus"].astype(bool).to_numpy(); k4=sedt["K4_E2plus"].astype(bool).to_numpy(); cats=[]
for a,b in zip(k3,k4):
    if a and b: cats.append("Both behaviour and containment evidence")
    elif a: cats.append("Behaviour evidence only")
    elif b: cats.append("Containment evidence only")
    else: cats.append("Neither reaches quantitative-evidence threshold")
marks={"Both behaviour and containment evidence":"D","Behaviour evidence only":"^","Containment evidence only":"s","Neither reaches quantitative-evidence threshold":"o"}
fig,ax=plt.subplots(figsize=(10.6,6.8))
for cat in marks:
    idx=np.array([c==cat for c in cats])
    if idx.any(): ax.scatter(age[idx],phys[idx],s=35+24*breadth[idx],marker=marks[cat],label=cat,alpha=.85)
off4={"A14":(5,18),"A15":(5,-18),"A02":(5,14),"A05":(5,-16),"A10":(-21,-13)}
for i,aid in enumerate(sedt["asset_id"]):
    dx,dy=off4.get(aid,(4,10)); ax.annotate(aid,(age[i],phys[i]),xytext=(dx,dy),textcoords="offset points",fontsize=8)
ax.set_xlabel("Years since injection began at the evidence cutoff"); ax.set_ylabel("Generic seismic detectability")
ax.set_title("Figure 4 | Time in operation and the mix of measurements add distinct information")
ax.legend(loc="lower right",fontsize=8.3); ax.text(0.015,0.985,"Larger symbols = more documented measurement families",transform=ax.transAxes,va="top",fontsize=9)
save(fig,"Fig4_verification_realization")

order=["Physical only","Age only","Topology only","Age + topology","Physical + age","Physical + age + topology"]; xp=np.arange(len(order))
fig,ax=plt.subplots(figsize=(10.4,5.7))
for outcome,marker,lab in [("K3","o","Behaviour-versus-expectation evidence"),("K4","s","Containment evidence")]:
    d=models[models["outcome"]==outcome].set_index("model").loc[order]
    ax.plot(xp,d["LOOCV_AUC"].to_numpy(),marker=marker,label=lab)
ax.axhline(.5,linestyle="--",linewidth=1); ax.set_xticks(xp,["Seismic\ndetectability","Time in\noperation","Monitoring\nbreadth","Time +\nmonitoring","Seismic +\ntime","Seismic + time\n+ monitoring"])
ax.set_ylim(0,1); ax.set_ylabel("Leave-one-site-out AUC"); ax.set_title("Supplementary Fig. 3 | Small-sample diagnostic models"); ax.legend(fontsize=8.5)
save(fig,"FigS3_model_diagnostic")

families=["P","S","M","W","G","D","E"]
T=topo[families].to_numpy(float)
fig,ax=plt.subplots(figsize=(9.6,7.5)); im=ax.imshow(T,aspect="auto",vmin=0,vmax=1)
ax.set_xticks(np.arange(len(families)),["Pressure /\ninjection","Active\nseismic","Microseismic","Well / fibre /\nlogs","Geochemical /\ntracer","Deformation /\ngeodesy","Shallow /\nenvironment"])
ax.set_yticks(np.arange(len(topo)),topo["asset_id"]); ax.set_title("Supplementary Fig. 2 | Documented monitoring architecture")
fig.colorbar(im,ax=ax,shrink=.75,label="Documented measurement family")
save(fig,"FigS2_monitoring_architecture")
print(f"Figures written to {OUT}")
