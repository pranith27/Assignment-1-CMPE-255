# Assignment Part 2: Six Creative Data Science Experiment Replications

## Overview

This part contains six independently implemented replications selected from the instructor's `dlmastery/data_science_examples` repository. The assignment permits creative adaptation rather than exact duplication. Each project therefore preserves the central data-science idea of the reference while using a smaller, reproducible implementation and adding documented improvements.

## Selected Replications

| # | Reference experiment | Core idea reproduced | What I changed / improved | Local evidence |
|---|---|---|---|---|
| 10 | CRISP-DM Master's Platform | CRISP-DM analytics, clustering, anomaly detection, regression, association-style analysis, cosine similarity/LSH | Added cluster stability across k=3,4,5, consolidated scorecard, detailed cosine-neighbor output, and explicit phase evidence | [Project 10](10-crispdm-masters-platform/) |
| 11 | Enterprise DS Audit | Data quality, leakage, validation, reproducibility, and governance review | Audited the Assignment 1 project directly, added weighted scoring, review-item handling, and machine-readable evidence | [Project 11](11-enterprise-ds-audit/) |
| 12 | TimePulse Forecasting | Trend/seasonality, lag features, chronological forecasting | Added seasonal-naive benchmark, 40-lag autocorrelation diagnostics, rolling diagnostics, and anomaly flags | [Project 12](12-timepulse-forecasting/) |
| 13 | NYC TLC Mobility Platform | Mobility analytics, trip features, fare modeling, and segmentation | Added rush-hour, fare-per-mile, and speed features plus a baseline comparison; uses transparent synthetic data | [Project 13](13-nyc-tlc-mobility-platform/) |
| 14 | AutoGluon Multimodal Suite | Text, image, and tabular multimodal fusion | Added leakage-safe 5-fold out-of-fold Ridge stacking and modality ablation; replaced heavyweight models with deterministic local features | [Project 14](14-autogluon-multimodal-suite/) |
| 15 | SPY SOTA TimeSeries Alpha | Financial forecasting, walk-forward evaluation, and risk metrics | Added momentum, volatility, zero-return baseline, transaction-cost deduction, and drawdown analysis; uses synthetic SPY-like data | [Project 15](15-spy-sota-timeseries-alpha/) |

## Review Pattern Used in Every Replication

Each project follows the same grading-friendly path:

**Reference -> Objective -> Replication approach -> What changed -> Results -> Evidence -> Reproducibility -> Limitations**

This allows each experiment to be reviewed independently without requiring the grader to understand the entire repository first.

## Results at a Glance

| Project | Key result |
|---|---|
| 10 | Best clustering k = 3; silhouette **0.2677**; regression R² **0.9288**; outlier rate **5.0%** |
| 11 | Audit score: **96.0/100 weighted**; unweighted mean 96.2; two dimensions flagged for review |
| 12 | Seasonal Naive outperformed Gradient Boosting; MAPE **2.125% vs 2.516%** |
| 13 | Histogram Gradient Boosting achieved R² **0.998** on the synthetic mobility experiment |
| 14 | Out-of-fold Ridge stacking achieved MAE **10.020** and R² **0.934** |
| 15 | Ridge walk-forward directional accuracy **60.27%**; synthetic-test Sharpe **5.05** after transaction-cost deduction |

## Evidence and Reproducibility

Every replication contains:

- `README.md` with methodology, results, limitations, and a change log
- `PROMPT.md` documenting the coding-assistant request
- `replication.py` as the reproducible entry point
- `tests/` containing basic artifact and result validation
- `artifacts/` containing machine-readable CSV/JSON outputs and visual evidence
- `reference/` containing the source-project description and a reference screenshot

Shared dependencies for the six replications are listed in [`requirements.txt`](requirements.txt).

Run every replication from this folder with:

```bash
python run_all.py
```

Run all replication test suites with:

```bash
python run_tests.py
```

Run the tests from the repository's Assignment Part 2 folder with:

```bash
for d in 10-crispdm-masters-platform 11-enterprise-ds-audit 12-timepulse-forecasting 13-nyc-tlc-mobility-platform 14-autogluon-multimodal-suite 15-spy-sota-timeseries-alpha; do (cd "$d" && python -m unittest discover -s tests -v); done
```

## Reference Repository

Instructor source repository: https://github.com/dlmastery/data_science_examples

## YouTube Walkthrough

**Published YouTube URL:** https://youtu.be/5fAuANO59UM
