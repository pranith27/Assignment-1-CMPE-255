import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

class TestNYCMobility(unittest.TestCase):
    def test_model_metrics(self):
        df = pd.read_csv(ART / "model_metrics.csv")
        self.assertIn("model", df.columns)
        self.assertTrue({"Mean baseline", "Histogram Gradient Boosting"}.issubset(set(df["model"])))

    def test_mobility_segments(self):
        df = pd.read_csv(ART / "mobility_segments.csv")
        self.assertTrue({"trips","avg_fare","avg_duration"}.issubset(df.columns))
        self.assertGreater(len(df), 0)

if __name__ == "__main__":
    unittest.main()
