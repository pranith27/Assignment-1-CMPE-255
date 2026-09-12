# Assignment Part 2 Results Summary

This document provides a concise review of the six selected creative replications. Each project preserves the central idea of the instructor's reference experiment while using a smaller, auditable implementation and at least one documented enhancement.

| Project | Core replication | Added improvement | Key result |
|---|---|---|---|
| 10 | CRISP-DM analytics, clustering, outliers, regression, association-style analysis, cosine similarity | Consolidated scorecard, stability-oriented evidence, detailed neighbor output | Silhouette 0.2669; regression R² 0.9288; outlier rate 5.0% |
| 11 | Enterprise quality and leakage audit | Project-specific evidence, weighted interpretation, machine-readable summary | Overall audit score 96.2/100; two review dimensions |
| 12 | Trend/seasonality forecasting and chronological evaluation | Seasonal-naive benchmark, lag diagnostics, anomaly-aware analysis | Seasonal Naive MAPE 2.125% vs Gradient Boosting 2.516% |
| 13 | Mobility analytics, trip features, fare modeling, segmentation | Rush-hour and fare-efficiency features; explicit synthetic-data disclosure | Histogram Gradient Boosting R² 0.9791 |
| 14 | Text, image, and tabular multimodal fusion | Modality ablation and leakage-safe OOF Ridge stacking | OOF Ridge stacking MAE 10.020; R² 0.9342 |
| 15 | Financial forecasting with walk-forward evaluation and risk metrics | Momentum/volatility features, zero-return baseline, drawdown and transaction-cost analysis | Directional accuracy 60.27%; synthetic-test Sharpe 6.05 |

## Interpretation

The results are intentionally not presented as claims that the lightweight implementations are identical to the instructor's larger reference systems. The adaptations focus on preserving the analytical concept, making the code reproducible in a course environment, and adding at least one meaningful extension per experiment.

Projects using synthetic or proxy data are explicitly labeled as such in their individual READMEs. Their results should be understood as educational replication results, not production benchmarks.
