import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, r2_score
from sklearn.metrics.pairwise import cosine_similarity

OUT = Path(__file__).parent / "artifacts"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
n = 2500

# Synthetic census-style dataset matching the reference project's teaching setup.
age = rng.integers(18, 76, n)
edu = rng.integers(8, 17, n)
hours = np.clip(rng.normal(40, 10, n), 15, 80)
income = (22000 + age * 700 + edu**1.6 * 1200 + hours * 550 + rng.normal(0, 6500, n)).clip(18000, 220000)
occupation = rng.choice(["management", "professional", "sales", "service", "technical"], n)
df = pd.DataFrame({
    "age": age,
    "education_num": edu,
    "hours_per_week": hours.round(1),
    "occupation": occupation,
    "annual_income": income.round(2),
})
df.to_csv(OUT / "census_replica.csv", index=False)

numeric = ["age", "education_num", "hours_per_week", "annual_income"]
df[numeric].corr().to_csv(OUT / "phase1_correlations.csv")

# Clustering and stability analysis.
X = StandardScaler().fit_transform(df[numeric])
stability_rows = []
for k in (3, 4, 5):
    labels_k = KMeans(n_clusters=k, n_init=20, random_state=42).fit_predict(X)
    stability_rows.append({"k": k, "silhouette": silhouette_score(X, labels_k)})
stability = pd.DataFrame(stability_rows)
stability.to_csv(OUT / "cluster_stability.csv", index=False)

best_k = int(stability.loc[stability["silhouette"].idxmax(), "k"])
km = KMeans(n_clusters=best_k, n_init=20, random_state=42)
labels = km.fit_predict(X)
pd.DataFrame({"cluster": labels}).value_counts().rename("size").to_csv(OUT / "cluster_sizes.csv")

# Anomaly detection.
iso = IsolationForest(contamination=0.05, random_state=42)
outlier = iso.fit_predict(X) == -1
pd.DataFrame({"is_outlier": outlier}).to_csv(OUT / "outlier_flags.csv", index=False)

# Income regression.
Xr = df[["age", "education_num", "hours_per_week"]]
y = df.annual_income
xt, xv, yt, yv = train_test_split(Xr, y, test_size=0.2, random_state=42)
model = GradientBoostingRegressor(random_state=42, n_estimators=180, max_depth=3, learning_rate=0.05).fit(xt, yt)
r2 = r2_score(yv, model.predict(xv))

# Transparent pair-rule discovery.
bins = pd.DataFrame({
    "age_group": pd.cut(df.age, [17, 29, 44, 59, 100], labels=["18-29", "30-44", "45-59", "60+"]),
    "high_income": df.annual_income >= df.annual_income.median(),
})
rules = []
for group in bins.age_group.cat.categories:
    sub = bins.age_group == group
    support = float((sub & bins.high_income).mean())
    confidence = float((sub & bins.high_income).sum() / max(sub.sum(), 1))
    base = float(bins.high_income.mean())
    lift = confidence / base if base else 0
    rules.append({"age_group": group, "support": support, "confidence": confidence, "lift": lift})
pd.DataFrame(rules).to_csv(OUT / "association_style_rules.csv", index=False)

# Cosine-similarity locality hashing approximation.
vecs = StandardScaler().fit_transform(df[["age", "education_num", "hours_per_week"]])[:500]
planes = rng.normal(size=(12, vecs.shape[1]))
bits = (vecs @ planes.T >= 0).astype(int)
q = 0
hamming = np.abs(bits - bits[q]).sum(axis=1)
cosine = cosine_similarity(vecs[[q]], vecs)[0]
res = pd.DataFrame({"index": np.arange(len(vecs)), "hamming_distance": hamming, "cosine_similarity": cosine})
res = res[res["index"] != q].sort_values(["hamming_distance", "cosine_similarity"], ascending=[True, False]).head(25)
res.to_csv(OUT / "lsh_neighbors.csv", index=False)

scorecard = pd.DataFrame({
    "metric": ["best_cluster_k", "silhouette", "regression_r2", "outlier_rate", "top_lsh_cosine"],
    "value": [best_k, stability[stability.k == best_k].silhouette.iloc[0], r2, outlier.mean(), res.cosine_similarity.max()],
})
scorecard.to_csv(OUT / "scorecard.csv", index=False)

print({
    "best_cluster_k": best_k,
    "silhouette": round(float(stability[stability.k == best_k].silhouette.iloc[0]), 4),
    "regression_r2": round(float(r2), 4),
    "outlier_rate": round(float(outlier.mean()), 4),
    "top_lsh_cosine": round(float(res.cosine_similarity.max()), 4),
})
