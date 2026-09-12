# Assignment Part 1 YouTube Walkthrough Script

## 1. Introduction
Hello, and this is my CMPE 255 Assignment 1 on data science.

For this project, I used the Medical Cost Personal Dataset from Kaggle. The goal was to predict medical insurance charges using machine learning while demonstrating a complete, end-to-end data science workflow. I also explored how an AI assistant can support different stages of the process, while verifying the generated code and results independently.

## 2. Dataset and Problem Definition
The dataset originally contained 1,338 observations and seven columns: age, gender, BMI, children, smoker, region, and charges. Since charges is a continuous numerical variable, this is a regression problem. The objective was to use patient information to estimate medical insurance costs.

I selected this dataset because it is relatively small, easy to interpret, and includes both numerical and categorical features, making it suitable for demonstrating data cleaning, visualization, preprocessing, and regression techniques.

## 3. Workflow
I structured the project using the CRISP-DM methodology, which organized the work into data understanding, preparation, modeling, evaluation, and interpretation.

I used an iterative approach throughout the project. I explored different methods, implemented them, checked the outputs, and made decisions based on the observed results.

## 4. Data Understanding and Preparation
I inspected the dataset's structure, data types, summary statistics, missing values, and duplicate records. There were no missing values, but one duplicate record was identified and removed. This left 1,337 observations for analysis.

I encoded the categorical variables and incorporated numerical and categorical preprocessing into the machine learning workflow. I then divided the data into training and test sets. The training data was used to fit the models, while the test data was reserved for evaluating performance on unseen observations.

## 5. Modeling and Validation
I trained three regression models: Linear Regression, Decision Tree Regressor, and Random Forest Regressor.

Linear Regression provided an interpretable baseline. Decision Trees helped capture nonlinear relationships, while Random Forest combined multiple trees to model more complex patterns.

I also included a dummy mean baseline and performed five-fold cross-validation on the training data. Random Forest remained the strongest model during the comparison, providing additional confidence in its performance.

## 6. Conclusion
Overall, this project demonstrated an end-to-end data science workflow, including cleaning, analysis, preprocessing, modeling, evaluation, and interpretation.

Random Forest achieved the strongest predictive performance, and feature importance indicated that smoking status, BMI, and age were the most influential predictors in the fitted model.

Most importantly, the project showed how AI-assisted tools can support data science through planning, coding, and analysis, while human verification remains essential.

Thank you for watching.
