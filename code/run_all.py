#!/usr/bin/env python3
"""One-command reproduction and verification entry point."""
from pathlib import Path
import subprocess,sys
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def run(script):
    print(f'\n==> {script}'); subprocess.run([sys.executable,str(ROOT/'code'/script)],cwd=ROOT,check=True)
run('reproduce_ambiguity.py'); run('reproduce_models.py'); run('reproduce_figures.py')
a=pd.read_csv(ROOT/'data'/'ambiguity_sensitivity_results.csv'); b=pd.read_csv(ROOT/'reproduced'/'ambiguity_sensitivity_results.csv')
assert list(a.columns)==list(b.columns)
for c in a.columns:
    if pd.api.types.is_numeric_dtype(a[c]): assert np.allclose(a[c].to_numpy(float),b[c].to_numpy(float),rtol=0,atol=1e-10,equal_nan=True),c
    else: assert a[c].astype(str).tolist()==b[c].astype(str).tolist(),c
print('\nAmbiguity sensitivity: VERIFIED')
frozen=pd.read_csv(ROOT/'data'/'small_sample_model_diagnostics.csv'); repro=pd.read_csv(ROOT/'reproduced'/'small_sample_model_diagnostics.csv'); fk=frozen.set_index(['outcome','model']); rk=repro.set_index(['outcome','model'])
for key in fk.index:
    if key in rk.index:
        for c in ['LOOCV_AUC','LOOCV_Brier']: assert abs(float(fk.loc[key,c])-float(rk.loc[key,c]))<1e-10,(key,c)
print('Small-sample diagnostic models: VERIFIED'); print('\nREPRODUCTION PASS')
