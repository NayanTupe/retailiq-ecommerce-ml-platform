# Model Performance Report

## Project Name

RetailIQ: E-commerce Customer Churn Prediction Platform

## Objective

The objective of this project is to predict whether an e-commerce customer is likely to churn based on customer profile, spending behavior, purchase activity, membership type, ratings, and discount usage.

This model helps business owners identify high-risk customers early and take retention actions such as personalized offers, loyalty rewards, or follow-up campaigns.

---

## Dataset Summary

The dataset contains 100,000 customer records with the following information:

* Customer ID
* Gender
* Age
* City
* Membership Type
* Total Spend
* Items Purchased
* Average Rating
* Discount Applied
* Days Since Last Purchase
* Satisfaction Level

There were no missing values and no duplicate records in the dataset.

---

## Data Cleaning Summary

The following cleaning steps were performed:

* Standardized column names into snake_case format
* Removed duplicate records
* Cleaned categorical values
* Converted numeric columns into proper numeric format
* Validated age, spend, rating, and purchase-related values
* Saved cleaned data into the interim data layer

---

## Feature Engineering

New business and machine learning features were created:

* avg_spend_per_item
* is_high_value_customer
* is_frequent_buyer
* is_inactive_customer
* low_rating_flag
* discount_used_flag
* churn

The churn label was created using business logic:

A customer is considered churn-risk if:

* days_since_last_purchase is greater than or equal to 45, or
* satisfaction_level is Unsatisfied

---

## Data Leakage Handling

Initial model accuracy was 100%, which indicated data leakage.

The issue occurred because the model was trained using columns that were directly used to create the churn label:

* days_since_last_purchase
* satisfaction_level
* is_inactive_customer

To make the model realistic and industry-ready, these leakage columns were removed from training.

---

## Final Model

Algorithm used:

Random Forest Classifier

Model configuration:

* n_estimators: 200
* max_depth: 12
* class_weight: balanced
* random_state: 42

---

## Model Performance

Final model performance after fixing data leakage:

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 0.7450 |
| Precision | 0.7142 |
| Recall    | 0.9609 |
| F1 Score  | 0.8194 |
| ROC AUC   | 0.7590 |

Confusion Matrix:

| Actual / Predicted | Predicted No Churn | Predicted Churn |
| ------------------ | -----------------: | --------------: |
| Actual No Churn    |               3328 |            4630 |
| Actual Churn       |                471 |           11571 |

---

## Business Interpretation

The model has a high recall score of 96.09%, which means it successfully identifies most customers who are likely to churn.

For a churn prediction use case, high recall is important because missing a churn-risk customer can result in revenue loss. It is better for the business to identify more potentially risky customers and take retention actions.

The model has some false positives, meaning some customers are predicted as churn-risk even though they may not churn. In a business context, this is acceptable if the retention campaign cost is lower than the cost of losing customers.

---

## Recommendation

This model can be used by an e-commerce business to:

* Identify high-risk customers
* Prioritize retention campaigns
* Offer discounts or loyalty rewards
* Monitor customer satisfaction
* Improve customer lifetime value

Future improvements:

* Try XGBoost and LightGBM models
* Perform hyperparameter tuning
* Add customer transaction history
* Add time-based purchase behavior
* Build Streamlit dashboard
* Deploy prediction API using FastAPI
