# ChatGPT Prompt History

This document records the main prompt types used to guide the chatbot-assisted data science workflow.

## Initial Project Prompt

> Build an end-to-end data science project using the Medical Cost Personal Dataset from Kaggle. Organize the work as a complete machine learning workflow and explain each stage clearly.

## Workflow and Methodology Prompts

- Structure the project using the CRISP-DM methodology.
- Help define the business problem, target variable, and modeling objective.
- Identify what data-quality checks should be performed before modeling.
- Recommend appropriate exploratory visualizations for the dataset.

## Modeling Prompts

- Compare multiple regression algorithms rather than using only one model.
- Explain why Linear Regression, Decision Tree, and Random Forest are appropriate comparison models.
- Recommend suitable regression evaluation metrics and explain what each metric means.
- Help interpret model-comparison results and feature importance.

## Improvement Prompts

- Add a simple baseline so model performance can be compared against a non-learning reference.
- Add cross-validation to check whether performance is reasonably consistent.
- Add residual and actual-vs-predicted analysis.
- Review the project for limitations, overclaims, and reproducibility issues.

## Documentation Prompts

- Improve notebook documentation and markdown explanations.
- Create a professional GitHub README.
- Organize the project artifacts clearly.
- Prepare a YouTube walkthrough script explaining the end-to-end journey.
