import unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ev=pd.read_csv(DATA/'final_evidence_scores.csv',encoding='utf-8-sig'); cls.site=pd.read_csv(DATA/'recoded_site_results.csv',encoding='utf-8-sig'); cls.src=pd.read_csv(DATA/'evidence_source_registry.csv',encoding='utf-8-sig'); cls.amb=pd.read_csv(DATA/'ambiguity_sensitivity_results.csv',encoding='utf-8-sig')
    def test_dimensions(self): self.assertEqual(len(self.ev),15); self.assertEqual(len(self.src),45); self.assertEqual(len(self.site),15)
    def test_scores(self): self.assertEqual(int((self.ev.k2>=2).sum()),13); self.assertEqual(int((self.ev.k3>=2).sum()),6); self.assertEqual(int((self.ev.k4>=2).sum()),6)
    def test_reactive_basalt_boundary(self):
        b1=self.site[self.site.B1.astype(bool)]; self.assertEqual(len(b1),1); self.assertEqual(b1.iloc[0].asset_id,'A13')
    def test_ambiguity_bounds(self):
        self.assertEqual(len(self.amb),4); self.assertGreaterEqual(float(self.amb.K2_minus_K3_pp.min()),40.0-1e-12); self.assertGreaterEqual(float(self.amb.K2_minus_K4_pp.min()),33.333333333-1e-9); mm=[c for c in self.amb.columns if 'mismatch_q' in c and c.endswith('_n')]; self.assertGreaterEqual(int(self.amb[mm].min().min()),5)
if __name__=='__main__': unittest.main()
