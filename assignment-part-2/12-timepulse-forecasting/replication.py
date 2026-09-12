import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

OUT = Path(__file__).parent / "artifacts"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)

n = 730
t = np.arange(n)
trend = 1200 + 1.8 * t + 0.0012 * t * t
weekly = 140 * np.sin(2 * np.pi * t / 7) + 60 * np.cos(4 * np.pi * t / 7)
annual = 320 * np.sin(2 * np.pi * t / 365.25 - np.pi / 2)
noise = rng.normal(0, 45, n)
for i in [85, 142, 210, 312, 420, 515, 602, 690]:
    noise[i] += rng.choice([350, -320, 410, 480])
y = trend + weekly + annual + noise

df = pd.DataFrame({"demand_mw": y})
for lag in [1, 2, 3, 7, 14, 21, 30]:
    df[f"lag_{lag}"] = df.demand_mw.shift(lag)
df["rolling_mean_7"] = df.demand_mw.shift(1).rolling(7).mean()
df["rolling_std_7"] = df.demand_mw.shift(1).rolling(7).std()

# 40-lag autocorrelation profile and anomaly flags.
acf_rows = []
for lag in range(1, 41):
    acf_rows.append({"lag": lag, "autocorrelation": df.demand_mw.autocorr(lag=lag)})
pd.DataFrame(acf_rows).to_csv(OUT / "acf_40_lags.csv", index=False)

rolling_mean = df.demand_mw.rolling(21, center=True).mean()
rolling_std = df.demand_mw.rolling(21, center=True).std()
df["anomaly_flag"] = ((df.demand_mw - rolling_mean).abs() > 3 * rolling_std).fillna(False)
df.to_csv(OUT / "forecast_diagnostics.csv", index=False)

df = df.dropna().reset_index(drop=True)
features = [c for c in df.columns if c.startswith("lag_") or c.startswith("rolling_")]
cut = int(len(df) * 0.8)
model = GradientBoostingRegressor(random_state=42, n_estimators=180, learning_rate=0.06, max_depth=3).fit(df.iloc[:cut][features], df.iloc[:cut].demand_mw)
pred = model.predict(df.iloc[cut:][features])
actual = df.iloc[cut:].demand_mw.to_numpy()
seasonal_naive = df.demand_mw.shift(7).iloc[cut:].to_numpy()

metrics = pd.DataFrame([
    {"model": "GradientBoosting multi-lag", "MAE": mean_absolute_error(actual, pred), "RMSE": mean_squared_error(actual, pred) ** 0.5, "MAPE": np.mean(np.abs((actual - pred) / actual)) * 100},
    {"model": "Seasonal Naive s=7", "MAE": mean_absolute_error(actual, seasonal_naive), "RMSE": mean_squared_error(actual, seasonal_naive) ** 0.5, "MAPE": np.mean(np.abs((actual - seasonal_naive) / actual)) * 100},
])
metrics.to_csv(OUT / "metrics.csv", index=False)
pd.DataFrame({"actual": actual, "gbr_forecast": pred, "seasonal_naive": seasonal_naive}).to_csv(OUT / "forecast.csv", index=False)

plt.figure(figsize=(10, 4))
plt.plot(actual, label="Actual")
plt.plot(pred, label="Gradient Boosting")
plt.plot(seasonal_naive, label="Seasonal Naive", alpha=0.7)
plt.legend(); plt.tight_layout(); plt.savefig(OUT / "forecast_comparison.png", dpi=160); plt.close()
print(metrics.round(3).to_string(index=False))
