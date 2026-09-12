import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

class TestCRISPDMDMReplication(unittest.TestCase):
    def test_scorecard_schema(self):
        df = pd.read_csv(ART / "scorecard.csv")
        self.assertEqual(list(df.columns), ["metric", "value"])
        self.assertTrue(set(df["metric"]) >= {"silhouette", "regression_r2", "outlier_rate"})

    def test_lsh_output(self):
        df = pd.read_csv(ART / "lsh_neighbors.csv")
        self.assertIn("cosine_similarity", df.columns)
        self.assertGreater(len(df), 0)

if __name__ == "__main__":
    unittest.main()
