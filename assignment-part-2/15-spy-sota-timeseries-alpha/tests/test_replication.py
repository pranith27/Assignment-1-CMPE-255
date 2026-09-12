import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

class TestSPYReplication(unittest.TestCase):
    def test_metrics_models(self):
        df = pd.read_csv(ART / "metrics.csv")
        self.assertTrue({"Zero-return baseline","Ridge walk-forward"}.issubset(set(df["model"])))

    def test_walk_forward_has_no_missing_values(self):
        df = pd.read_csv(ART / "walk_forward_predictions.csv")
        self.assertTrue({"actual_return","predicted_return","signal","gross_strategy_return","transaction_cost","net_strategy_return","equity"}.issubset(df.columns))
        self.assertFalse(df.isnull().any().any())

if __name__ == "__main__":
    unittest.main()
