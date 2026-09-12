import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

class TestMultimodal(unittest.TestCase):
    def test_ablation_models(self):
        df = pd.read_csv(ART / "modality_ablation.csv")
        expected = {"Text only","Image only","Tabular only","Equal-weight fusion","OOF Ridge stacking"}
        self.assertEqual(set(df["model"]), expected)
        self.assertTrue((df["MAE"] >= 0).all())

    def test_predictions_have_modalities(self):
        df = pd.read_csv(ART / "fusion_predictions.csv")
        self.assertTrue({"actual","text","image","tabular","equal_weight","oof_stack"}.issubset(df.columns))

if __name__ == "__main__":
    unittest.main()
