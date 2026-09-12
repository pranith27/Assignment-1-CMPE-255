import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

OUT = Path(__file__).parent / "artifacts"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
n = 8000

pickup_lat = 40.70 + rng.normal(0, 0.06, n)
pickup_lon = -73.99 + rng.normal(0, 0.07, n)
drop_lat = 40.70 + rng.normal(0, 0.06, n)
drop_lon = -73.99 + rng.normal(0, 0.07, n)
dx = (drop_lon - pickup_lon) * 53
dy = (drop_lat - pickup_lat) * 69
distance = np.sqrt(dx * dx + dy * dy)
duration = np.maximum(3, distance * 9 + rng.normal(12, 6, n))
speed = np.divide(distance, duration / 60, out=np.zeros(n), where=duration > 0)
hour = rng.integers(0, 24, n)
rush_hour = np.isin(hour, [7, 8, 9, 16, 17, 18, 19])
fare = 3.5 + 2.2 * distance + 0.35 * duration + 5 * (rng.random(n) > 0.8) + 2.5 * rush_hour + rng.normal(0, 2, n)
fare_per_mile = fare / np.maximum(distance, 0.25)

df = pd.DataFrame({
    "distance_miles": distance,
    "duration_min": duration,
    "speed_mph": speed,
    "fare_usd": fare,
    "hour": hour,
    "rush_hour": rush_hour.astype(int),
    "fare_per_mile": fare_per_mile,
})
df.to_csv(OUT / "synthetic_taxi_trips.csv", index=False)
df[df.rush_hour == 1].groupby("hour").agg(trips=("fare_usd", "size"), avg_fare=("fare_usd", "mean"), avg_fare_per_mile=("fare_per_mile", "mean")).to_csv(OUT / "rush_hour_fare_efficiency.csv")

cut = int(0.8 * n)
train, test = df.iloc[:cut], df.iloc[cut:]
features = ["distance_miles", "duration_min", "speed_mph", "hour", "rush_hour"]
model = HistGradientBoostingRegressor(max_depth=7, learning_rate=0.06, max_iter=220, random_state=42).fit(train[features], train.fare_usd)
pred = model.predict(test[features])
base = np.full(len(test), train.fare_usd.mean())
rows = [
    {"model": "Mean baseline", "RMSE": mean_squared_error(test.fare_usd, base) ** 0.5, "MAE": mean_absolute_error(test.fare_usd, base), "R2": r2_score(test.fare_usd, base)},
    {"model": "Histogram Gradient Boosting", "RMSE": mean_squared_error(test.fare_usd, pred) ** 0.5, "MAE": mean_absolute_error(test.fare_usd, pred), "R2": r2_score(test.fare_usd, pred)},
]
pd.DataFrame(rows).to_csv(OUT / "model_metrics.csv", index=False)

df["segment"] = pd.cut(df.distance_miles, [0, 1, 3, 6, 20], labels=["Short", "Medium", "Long", "Very Long"], include_lowest=True)
df.groupby("segment", observed=False).agg(trips=("fare_usd", "size"), avg_fare=("fare_usd", "mean"), avg_duration=("duration_min", "mean")).to_csv(OUT / "mobility_segments.csv")

plt.figure(figsize=(6, 4))
plt.scatter(test.fare_usd, pred, s=5, alpha=.25)
plt.xlabel("Actual fare"); plt.ylabel("Predicted fare"); plt.title("NYC TLC-inspired Fare Prediction")
plt.tight_layout(); plt.savefig(OUT / "actual_vs_predicted.png", dpi=160); plt.close()
print(pd.DataFrame(rows).round(3).to_string(index=False))
