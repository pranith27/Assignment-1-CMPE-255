# Medical Insurance Cost Prediction — Final Project Report

## Executive Summary

This project demonstrates an end-to-end machine-learning workflow for predicting individual medical insurance charges using the Kaggle Medical Cost Personal Dataset. ChatGPT was used as a coding and reasoning assistant for project planning, implementation guidance, visualization ideas, interpretation, and documentation. Generated suggestions were executed and checked against observed outputs before being used in the final analysis.

## Problem Definition

The target variable, `charges`, is continuous, so the project is formulated as a regression problem. The objective is to estimate insurance charges from age, sex, BMI, number of children, smoking status, and region.

## CRISP-DM Workflow

- **Business Understanding:** Define insurance-cost prediction as the project objective.
- **Data Understanding:** Inspect structure, data types, distributions, missing values, and duplicate records.
- **Data Preparation:** Remove one duplicate and encode categorical predictors.
- **Modeling:** Compare Linear Regression, Decision Tree, and Random Forest.
- **Evaluation:** Use MAE, RMSE, R², a mean baseline, and five-fold cross-validation.
- **Interpretation:** Examine feature importance, prediction behavior, residuals, subgroup error, and feature engineering.

## Dataset and Data Quality

The dataset contains 1,338 original observations and 7 columns. No missing values were found. One duplicate row was detected and removed, leaving 1,337 observations for the modeling workflow.

## Exploratory Findings

The charge distribution is positively skewed. The smoker and non-smoker groups show a substantial difference in observed charges. Age and BMI also show positive relationships with charges. Region and sex show comparatively weaker relationships. These exploratory results informed the subsequent modeling stage.

## Model Comparison

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 4,177.05 | 5,956.34 | 0.8069 |
| Decision Tree Regressor | 2,730.63 | 5,769.01 | 0.8189 |
| **Random Forest Regressor** | **2,611.53** | **4,664.78** | **0.8816** |

Random Forest is the strongest held-out test-set model among the three evaluated algorithms.

## Validation

Five-fold cross-validation on the training split produced mean R² values of 0.8177 for Random Forest, 0.7228 for Linear Regression, and 0.6495 for Decision Tree. The same model ranking was preserved, supporting the main conclusion. A dummy mean baseline produced an R² of -0.0084 on the held-out test set, showing that the trained models provide substantial improvement over a naive constant prediction.

## Feature Engineering Experiment

A BMI-age interaction feature was added as an explicit feature-engineering experiment. On the same train/test split, the original Random Forest achieved R² 0.8816, while the model with the BMI-age interaction achieved R² 0.8803. The engineered feature therefore did not improve the selected model and was not retained as part of the final specification. Documenting this negative result demonstrates evidence-based model selection.

## Interpretation

Random Forest feature importance identifies smoking status as the strongest predictive feature, followed by BMI and age. These values describe predictive contribution within the fitted model and do not establish causation.

## Error Analysis

Actual-versus-predicted and residual plots provide additional information beyond aggregate metrics. Subgroup MAE analysis was also used to check whether prediction difficulty differs across smoking-status groups. The held-out subgroup MAE was approximately 2,634.24 for non-smokers and 2,532.77 for smokers.

## Limitations and Responsible Use

The dataset is relatively small and contains a limited set of explanatory variables. The evaluation is based on one reproducible holdout split supplemented by cross-validation, not external validation. The results are predictive rather than causal, and feature importance should not be interpreted causally. This demonstration should not be used alone for medical, insurance, or financial decision-making.

## AI-Assisted Development

ChatGPT assisted with planning, CRISP-DM organization, coding suggestions, debugging guidance, EDA planning, model implementation, interpretation, and documentation. The final workflow emphasizes human verification: code was executed, outputs were inspected, and the reported findings were based on observed results.
