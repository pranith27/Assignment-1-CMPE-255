import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error

OUT = Path(__file__).parent / "artifacts"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
n = 252
t = np.arange(n)
ret = 0.0002 + 0.0008 * np.sin(t / 15) + rng.normal(0, 0.008, n)
close = 510 * np.exp(np.cumsum(ret))
volume = rng.integers(50_000_000, 90_000_000, n)
vix = 16 - 25 * ret + rng.normal(0, 0.5, n)
tnx = 4.2 + rng.normal(0, 0.05, n).cumsum() / 20

df = pd.DataFrame({"close": close, "volume": volume, "vix": vix, "tnx": t})
df["tnx"] = tnx
df["log_return"] = np.log(df.close / df.close.shift(1))
for lag in [1, 2, 3, 5, 10]:
    df[f"ret_lag_{lag}"] = df.log_return.shift(lag)
df["momentum_5"] = df.log_return.rolling(5).mean()
df["volatility_10"] = df.log_return.rolling(10).std()
df["vol_change"] = df.volume.pct_change()
df = df.dropna().reset_index(drop=True)
features = [c for c in df.columns if "ret_lag_" in c] + ["momentum_5", "volatility_10", "vol_change", "vix", "tnx"]

# Expanding-window walk-forward evaluation.
start = int(0.7 * len(df))
preds, actual, signals = [], [], []
for i in range(start, len(df)):
    tr, te = df.iloc[:i], df.iloc[[i]]
    model = Ridge(alpha=10).fit(tr[features], tr.log_return)
    p = float(model.predict(te[features])[0])
    a = float(te.log_return.iloc[0])
    preds.append(p); actual.append(a); signals.append(1 if p > 0 else -1)

preds = np.array(preds); actual = np.array(actual); signals = np.array(signals)
baseline = np.zeros_like(actual)
transaction_cost = 0.0005
turnover = np.r_[0, np.abs(np.diff(signals))]
gross = signals * actual
net = gross - transaction_cost * turnover
equity = np.cumprod(1 + net)
peak = np.maximum.accumulate(equity)
dd = equity / peak - 1

res = pd.DataFrame({"actual_return": actual, "predicted_return": preds, "signal": signals, "gross_strategy_return": gross, "transaction_cost": transaction_cost * turnover, "net_strategy_return": net, "equity": equity})
res.to_csv(OUT / "walk_forward_predictions.csv", index=False)

sharpe = float(np.sqrt(252) * net.mean() / net.std()) if net.std() else 0.0
metrics = [
    {"model": "Zero-return baseline", "RMSE": mean_squared_error(actual, baseline) ** .5, "MAE": mean_absolute_error(actual, baseline), "directional_accuracy": 0.5, "sharpe": 0.0, "max_drawdown": 0.0},
    {"model": "Ridge walk-forward", "RMSE": mean_squared_error(actual, preds) ** .5, "MAE": mean_absolute_error(actual, preds), "directional_accuracy": float((np.sign(preds) == np.sign(actual)).mean()), "sharpe": sharpe, "max_drawdown": float(dd.min())},
]
pd.DataFrame(metrics).to_csv(OUT / "metrics.csv", index=False)
pd.DataFrame({"metric": ["mean_volatility_10", "mean_momentum_5", "transaction_cost_per_trade"], "value": [df.volatility_10.mean(), df.momentum_5.mean(), transaction_cost]}).to_csv(OUT / "risk_diagnostics.csv", index=False)

plt.figure(figsize=(8, 4))
plt.plot(equity)
plt.title("Synthetic SPY-like Walk-Forward Equity Curve")
plt.xlabel("Test trading day"); plt.ylabel("Growth of $1")
plt.tight_layout(); plt.savefig(OUT / "equity_curve.png", dpi=160); plt.close()
print(pd.DataFrame(metrics).round(4).to_string(index=False))
