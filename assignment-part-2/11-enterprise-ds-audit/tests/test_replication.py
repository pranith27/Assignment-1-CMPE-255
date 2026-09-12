import unittest, json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

class TestEnterpriseAudit(unittest.TestCase):
    def test_scorecard_dimensions(self):
        df = pd.read_csv(ART / "audit_scorecard.csv")
        self.assertEqual(len(df), 6)
        self.assertTrue({"dimension","score","status","evidence"}.issubset(df.columns))

    def test_summary_is_valid(self):
        obj = json.loads((ART / "audit_summary.json").read_text())
        self.assertEqual(obj["dimensions"], 6)
        self.assertGreaterEqual(obj["overall_score"], 0)
        self.assertLessEqual(obj["overall_score"], 100)

if __name__ == "__main__":
    unittest.main()
