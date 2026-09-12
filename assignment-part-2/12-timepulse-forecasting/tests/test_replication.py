import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

class TestTimePulse(unittest.TestCase):
    def test_metrics_models(self):
        df = pd.read_csv(ART / "metrics.csv")
        self.assertEqual(set(df["model"]), {"GradientBoosting multi-lag", "Seasonal Naive s=7"})
        self.assertTrue((df[["MAE","RMSE","MAPE"]] >= 0).all().all())

    def test_forecast_columns(self):
        df = pd.read_csv(ART / "forecast.csv")
        self.assertEqual(set(df.columns), {"actual","gbr_forecast","seasonal_naive"})
        self.assertGreater(len(df), 0)

if __name__ == "__main__":
    unittest.main()
