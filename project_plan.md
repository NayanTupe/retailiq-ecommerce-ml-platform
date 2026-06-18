# RetailIQ Project Plan

## Project Name

RetailIQ: E-commerce Customer Churn Prediction Platform

---

## Project Goal

Build an end-to-end industry-style data science and machine learning platform for e-commerce customer analytics.

The project helps business owners:

* Understand customer behavior
* Predict customer churn
* Segment customers
* Track business KPIs
* Take retention actions
* Connect analytics with a future dashboard and website

---

## Current Project Status

Completed:

* Project folder structure
* Git and GitHub setup
* Raw data loading pipeline
* Data cleaning pipeline
* Feature engineering pipeline
* Churn label creation
* Data leakage detection and fix
* Churn prediction model
* Single customer prediction script
* Customer segmentation model
* Model performance report
* Customer segmentation report
* FastAPI backend setup
* Churn prediction API endpoint
* Dashboard analytics API endpoints
* API documentation report

Upcoming:

* README update with API endpoints
* Basic tests
* Optional Streamlit demo
* React / Next.js dashboard
* Deployment
* Docker setup
* CI/CD improvements

---

## Phase 1: Project Setup

Status: Completed

Files and folders created:

```text
retailiq-ecommerce-ml-platform/
├── data/
├── notebooks/
├── src/
├── models/
├── reports/
├── dashboard/
├── api/
├── database/
├── deployment/
├── tests/
├── requirements.txt
├── README.md
├── project_plan.md
└── .gitignore
```

Purpose:

* Create a scalable project structure
* Separate raw data, processed data, source code, reports, API, dashboard, and tests
* Prepare project for GitHub and future deployment

---

## Phase 2: Data Pipeline

Status: Completed

Files:

```text
src/data/data_loader.py
src/data/data_cleaning.py
src/features/feature_engineering.py
```

Input file:

```text
data/raw/ecommerce_customer_data.csv
```

Generated output files locally:

```text
data/interim/cleaned_customer_data.csv
data/processed/final_features.csv
```

Purpose:

* Load raw CSV dataset
* Inspect dataset shape, columns, missing values, and duplicates
* Clean and validate data
* Standardize column names
* Create ML-ready features
* Create churn target label

Dataset summary:

```text
Rows: 100,000
Columns before feature engineering: 11
Columns after feature engineering: 18
Missing values: 0
Duplicate rows: 0
```

---

## Phase 3: Feature Engineering

Status: Completed

File:

```text
src/features/feature_engineering.py
```

Features created:

* `avg_spend_per_item`
* `is_high_value_customer`
* `is_frequent_buyer`
* `is_inactive_customer`
* `low_rating_flag`
* `discount_used_flag`
* `churn`

Churn label logic:

```text
Customer is churn-risk if:
days_since_last_purchase >= 45
OR
satisfaction_level = Unsatisfied
```

Purpose:

* Convert raw customer records into ML-ready features
* Create business-friendly customer behavior indicators
* Prepare the dataset for churn prediction and segmentation

---

## Phase 4: Churn Prediction Model

Status: Completed

Files:

```text
src/models/train_churn_model.py
src/models/predict.py
```

Model used:

```text
Random Forest Classifier
```

Model configuration:

```text
n_estimators = 200
max_depth = 12
class_weight = balanced
random_state = 42
```

Final model performance:

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

Important learning:

Initial model accuracy was 100%, which indicated data leakage. Leakage columns were removed to make the model realistic and industry-ready.

Leakage columns removed from model training:

* `days_since_last_purchase`
* `satisfaction_level`
* `is_inactive_customer`

Purpose:

* Predict whether a customer is likely to churn
* Generate churn probability
* Convert model output into a business-friendly risk level
* Provide a retention recommendation

---

## Phase 5: Single Customer Prediction

Status: Completed

File:

```text
src/models/predict.py
```

Example output:

```text
Churn Prediction: Yes
Churn Probability: 84.14%
Risk Level: High Risk
Recommendation: Offer retention discount, loyalty reward, or personal follow-up.
```

Purpose:

* Test model inference on a single customer
* Prepare logic for API prediction endpoint
* Convert ML prediction into owner-friendly business recommendation

---

## Phase 6: Customer Segmentation

Status: Completed

File:

```text
src/models/train_segmentation_model.py
```

Model used:

```text
K-Means Clustering
```

Number of clusters:

```text
4
```

Silhouette Score:

```text
0.2898
```

Customer segments created:

* High Value Customers
* At Risk Customers
* Low Engagement Customers
* Satisfied Regular Customers

Segment distribution:

| Segment Name                | Customers |
| --------------------------- | --------: |
| Satisfied Regular Customers |    47,380 |
| High Value Customers        |    21,323 |
| At Risk Customers           |    20,277 |
| Low Engagement Customers    |    11,020 |

Purpose:

* Group customers by behavior
* Support targeted marketing
* Help dashboard users understand business priorities
* Provide segment-level insights for retention and growth

---

## Phase 7: Reports

Status: Completed

Files:

```text
reports/model_performance_report.md
reports/customer_segmentation_report.md
reports/api_documentation.md
```

Purpose:

* Explain churn model results
* Explain segmentation insights
* Document API endpoints
* Make the project interview-ready
* Make business decisions easy to understand

---

## Phase 8: FastAPI Backend

Status: Completed

Files:

```text
api/main.py
api/routes/churn_routes.py
api/routes/dashboard_routes.py
api/schemas/prediction_schema.py
api/services/prediction_service.py
```

Available endpoints:

```text
GET /
GET /health
POST /predict/churn
GET /analytics/summary
GET /analytics/segments
GET /analytics/churn-by-membership
```

Purpose:

* Convert ML model into a usable backend service
* Prepare backend for future React dashboard
* Serve analytics data as JSON
* Support real-time churn prediction

FastAPI local URL:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Phase 9: Analytics API

Status: Completed

Files:

```text
api/routes/dashboard_routes.py
```

Endpoints:

```text
GET /analytics/summary
GET /analytics/segments
GET /analytics/churn-by-membership
```

Purpose:

* Serve dashboard KPIs
* Serve customer segment summary
* Serve churn rate by membership type
* Prepare APIs for React frontend

Example dashboard data:

```json
{
  "total_customers": 100000,
  "total_revenue": 32224102.09,
  "average_spend": 322.24,
  "churn_rate": 60.21,
  "average_rating": 3.56
}
```

---

## Phase 10: Streamlit Dashboard

Status: Optional / Prototype

Purpose:

* Quick ML demo
* Show KPIs and charts
* Validate dashboard logic before React frontend

Recommended approach:

Use Streamlit only as a quick prototype. Build the final UI later in React + MUI for a stronger portfolio presentation.

---

## Phase 11: React Dashboard

Status: Upcoming

Recommended tech stack:

```text
React / Next.js
MUI
Recharts or ApexCharts
Axios
FastAPI backend
```

Planned pages:

* Dashboard Overview
* Churn Analytics
* Customer Segmentation
* Customer Prediction Form
* Business Insights
* Reports

Purpose:

* Build a professional portfolio website
* Connect frontend with FastAPI
* Show an end-to-end full-stack ML product
* Make the project visually impressive for job applications

---

## Phase 12: Deployment

Status: Upcoming

Planned deployment:

```text
Frontend: Vercel
Backend: Render / Railway
Database: PostgreSQL / Supabase optional
Model hosting: Backend local model artifact
```

Future deployment tasks:

* Add Dockerfile
* Add docker-compose configuration
* Add environment variables
* Add production CORS settings
* Add API deployment config
* Add frontend deployment config

---

## Phase 13: Testing

Status: Upcoming

Planned tests:

```text
tests/test_data_cleaning.py
tests/test_feature_engineering.py
tests/test_prediction.py
```

Purpose:

* Validate data cleaning pipeline
* Validate feature engineering logic
* Validate prediction response
* Improve production quality

---

## Final Portfolio Positioning

This project can be described as:

An end-to-end e-commerce customer intelligence platform that predicts customer churn, segments customers, exposes ML predictions through FastAPI, and prepares analytics endpoints for a future React dashboard.

---

## Skills Demonstrated

This project demonstrates:

* Python programming
* Data cleaning
* Feature engineering
* Exploratory data analysis preparation
* Machine learning classification
* Customer segmentation
* Data leakage detection and prevention
* Model evaluation
* Business reporting
* FastAPI backend development
* API documentation
* Git and GitHub workflow
* Industry-style project structure

---

## Next Immediate Tasks

1. Update README with API endpoints
2. Add basic tests
3. Add optional Streamlit demo
4. Build React + MUI frontend
5. Deploy FastAPI backend
6. Deploy frontend
7. Add Docker support
8. Add CI/CD workflow

---

## GitHub Commit Strategy

Recommended commit flow:

```text
Initial project setup
Add data loading pipeline
Add data cleaning pipeline
Add feature engineering and churn label creation
Add leakage-safe churn prediction training pipeline
Add single customer churn prediction script
Add customer segmentation model pipeline
Add model performance report
Add customer segmentation business report
Add FastAPI application entrypoint
Add churn prediction API endpoint
Add dashboard analytics API endpoints
Add FastAPI documentation report
Add project roadmap and implementation plan
```

---

## Notes

Generated files are ignored using `.gitignore` and are not pushed to GitHub.

Ignored generated folders:

```text
data/raw/
data/interim/
data/processed/
models/
logs/
venv/
```

To reproduce the project locally, the user should place the dataset in `data/raw/`, then run the data pipeline, model training scripts, and API server.
