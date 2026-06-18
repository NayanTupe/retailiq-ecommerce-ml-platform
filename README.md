# RetailIQ: E-commerce Customer Churn Prediction Platform

RetailIQ is an industry-style machine learning project built to analyze e-commerce customer behavior and predict customer churn risk.

The project includes a complete data science workflow: data loading, data cleaning, feature engineering, churn label creation, leakage-safe model training, model evaluation, customer segmentation, FastAPI backend, analytics API endpoints, and single-customer churn prediction.

---

## Project Objective

The main objective of this project is to help an e-commerce business identify customers who are likely to churn and take proactive retention actions.

The model predicts whether a customer is at churn risk and provides a business-friendly recommendation.

Example output:

```text
Churn Prediction: Yes
Churn Probability: 84.14%
Risk Level: High Risk
Recommendation: Offer retention discount, loyalty reward, or personal follow-up.
```

---

## Dataset

Dataset used:

```text
ecommerce_customer_data.csv
```

The dataset contains 100,000 customer records with features such as:

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

The raw dataset is not included in this repository because it is stored locally and ignored using `.gitignore`.

Expected dataset location:

```text
data/raw/ecommerce_customer_data.csv
```

---

## Project Structure

```text
retailiq-ecommerce-ml-platform/
│
├── data/
│   ├── raw/
│   │   └── ecommerce_customer_data.csv
│   │
│   ├── interim/
│   │   └── cleaned_customer_data.csv
│   │
│   └── processed/
│       ├── final_features.csv
│       └── customer_segments.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_churn_prediction_model.ipynb
│   ├── 05_customer_segmentation.ipynb
│   └── 06_sales_dashboard_insights.ipynb
│
├── src/
│   ├── data/
│   │   ├── data_loader.py
│   │   ├── data_cleaning.py
│   │   └── data_validation.py
│   │
│   ├── features/
│   │   └── feature_engineering.py
│   │
│   ├── models/
│   │   ├── train_churn_model.py
│   │   ├── train_segmentation_model.py
│   │   ├── evaluate_model.py
│   │   └── predict.py
│   │
│   ├── utils/
│   │   ├── helper.py
│   │   └── logger.py
│   │
│   └── visualization/
│       └── charts.py
│
├── models/
│   ├── churn_model.pkl
│   ├── segmentation_model.pkl
│   └── segmentation_scaler.pkl
│
├── reports/
│   ├── model_performance_report.md
│   ├── customer_segmentation_report.md
│   ├── api_documentation.md
│   └── figures/
│
├── dashboard/
│   ├── streamlit_app.py
│   └── pages/
│
├── api/
│   ├── main.py
│   ├── routes/
│   │   ├── churn_routes.py
│   │   └── dashboard_routes.py
│   ├── schemas/
│   │   └── prediction_schema.py
│   └── services/
│       └── prediction_service.py
│
├── database/
│   ├── schema.sql
│   └── seed_data.sql
│
├── deployment/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── tests/
│   ├── test_data_cleaning.py
│   ├── test_feature_engineering.py
│   └── test_prediction.py
│
├── requirements.txt
├── README.md
├── project_plan.md
├── app.py
└── .gitignore
```

---

## Workflow

```text
Raw CSV Data
    ↓
Data Loading
    ↓
Data Cleaning
    ↓
Feature Engineering
    ↓
Churn Label Creation
    ↓
Leakage-Safe Model Training
    ↓
Model Evaluation
    ↓
Customer Segmentation
    ↓
Single Customer Prediction
    ↓
FastAPI Backend
    ↓
Analytics API Endpoints
    ↓
Future React Dashboard / Website
```

---

## Data Cleaning

The following data cleaning steps were performed:

* Standardized column names into snake_case format
* Removed duplicate records
* Cleaned categorical values
* Converted numeric columns into proper numeric format
* Validated customer age, spend, rating, and purchase-related values
* Saved cleaned data into the interim data layer

Cleaned data output:

```text
data/interim/cleaned_customer_data.csv
```

---

## Feature Engineering

The following features were created for business and machine learning use:

* `avg_spend_per_item`
* `is_high_value_customer`
* `is_frequent_buyer`
* `is_inactive_customer`
* `low_rating_flag`
* `discount_used_flag`
* `churn`

Feature-engineered data output:

```text
data/processed/final_features.csv
```

---

## Churn Label Logic

The churn label was created using business logic.

A customer is considered churn-risk if:

```text
days_since_last_purchase >= 45
OR
satisfaction_level = Unsatisfied
```

---

## Data Leakage Handling

Initial model accuracy was 100%, which indicated data leakage.

The issue occurred because the model was trained using columns that were directly used to create the churn label.

Leakage columns:

* `days_since_last_purchase`
* `satisfaction_level`
* `is_inactive_customer`

To make the model realistic and industry-ready, these columns were removed from model training.

---

## Model Used

The churn prediction model uses:

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

---

## Model Performance

Final leakage-safe model performance:

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

For a churn prediction business case, recall is very important because missing a churn-risk customer can result in revenue loss.

The model produces some false positives, meaning some customers are predicted as churn-risk even though they may not churn. In a business context, this can be acceptable if the cost of a retention campaign is lower than the cost of losing customers.

---

## Single Customer Prediction

The project includes a prediction script that can predict churn risk for a single customer.

Prediction script:

```text
src/models/predict.py
```

Example prediction result:

```text
Churn Prediction: Yes
Churn Probability: 84.14%
Risk Level: High Risk
Recommendation: Offer retention discount, loyalty reward, or personal follow-up.
```

---

## Customer Segmentation

The project includes a customer segmentation pipeline using K-Means clustering.

Segmentation script:

```text
src/models/train_segmentation_model.py
```

Segments created:

* High Value Customers
* At Risk Customers
* Low Engagement Customers
* Satisfied Regular Customers

Silhouette Score:

```text
0.2898
```

Segment distribution:

| Segment Name                | Customers |
| --------------------------- | --------: |
| Satisfied Regular Customers |    47,380 |
| High Value Customers        |    21,323 |
| At Risk Customers           |    20,277 |
| Low Engagement Customers    |    11,020 |

Business purpose:

* Identify high-value customers
* Detect at-risk customers
* Plan retention campaigns
* Create owner-level dashboard insights
* Support personalized marketing actions

---

## FastAPI Backend

This project includes a FastAPI backend for churn prediction and dashboard analytics.

### Run API Locally

```bash
source venv/bin/activate
python -m uvicorn api.main:app --reload
```

Local API URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint                         | Purpose                       |
| ------ | -------------------------------- | ----------------------------- |
| GET    | `/`                              | API root status               |
| GET    | `/health`                        | Health check                  |
| POST   | `/predict/churn`                 | Predict customer churn risk   |
| GET    | `/analytics/summary`             | Dashboard KPI summary         |
| GET    | `/analytics/segments`            | Customer segment analytics    |
| GET    | `/analytics/churn-by-membership` | Churn rate by membership type |

---

## Sample Churn Prediction Request

```json
{
  "gender": "Female",
  "age": 32,
  "city": "Miami",
  "membership_type": "Bronze",
  "total_spend": 166.56,
  "items_purchased": 2,
  "average_rating": 2.5,
  "discount_applied": true,
  "avg_spend_per_item": 83.28,
  "is_high_value_customer": 0,
  "is_frequent_buyer": 0,
  "low_rating_flag": 1,
  "discount_used_flag": 1
}
```

---

## Sample Churn Prediction Response

```json
{
  "churn_prediction": 1,
  "churn_probability": 0.8414,
  "risk_level": "High Risk",
  "recommendation": "Offer retention discount, loyalty reward, or personal follow-up."
}
```

---

## Sample Dashboard Summary Response

Endpoint:

```text
GET /analytics/summary
```

Sample response:

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

## Business Use Cases

This project can help an e-commerce business to:

* Identify high-risk customers
* Prioritize retention campaigns
* Offer personalized discounts
* Improve customer lifetime value
* Monitor customer satisfaction
* Understand customer behavior
* Segment customers for targeted marketing
* Build business dashboards for owners and managers
* Integrate ML predictions with a future React dashboard

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/NayanTupe/retailiq-ecommerce-ml-platform.git
cd retailiq-ecommerce-ml-platform
```

### 2. Create Virtual Environment

For Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Place Dataset

Place the dataset at:

```text
data/raw/ecommerce_customer_data.csv
```

### 5. Run Data Loader

```bash
python src/data/data_loader.py
```

### 6. Run Data Cleaning

```bash
python src/data/data_cleaning.py
```

### 7. Run Feature Engineering

```bash
python src/features/feature_engineering.py
```

### 8. Train Churn Model

```bash
python src/models/train_churn_model.py
```

### 9. Predict Single Customer Churn

```bash
python src/models/predict.py
```

### 10. Train Customer Segmentation Model

```bash
python src/models/train_segmentation_model.py
```

### 11. Run FastAPI Backend

```bash
python -m uvicorn api.main:app --reload
```

Open Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Current Status

Completed:

* Project structure
* Data loading pipeline
* Data cleaning pipeline
* Feature engineering pipeline
* Churn label creation
* Data leakage fix
* Leakage-safe churn model training
* Model evaluation
* Single customer churn prediction
* Customer segmentation model
* Model performance report
* Customer segmentation report
* FastAPI backend setup
* Churn prediction API endpoint
* Dashboard analytics API endpoints
* API documentation report
* Project roadmap
* GitHub version control setup

Upcoming:

* Basic automated tests
* Optional Streamlit dashboard demo
* React / Next.js dashboard
* Deployment
* Docker setup
* CI/CD pipeline
* Business insights dashboard

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Random Forest Classifier
* K-Means Clustering
* Joblib
* FastAPI
* Uvicorn
* Pydantic
* Streamlit
* Git
* GitHub

---

## Future Improvements

* Add XGBoost and LightGBM models
* Add hyperparameter tuning
* Add advanced customer segmentation
* Add Streamlit dashboard demo
* Add React / Next.js frontend
* Add Docker-based deployment
* Add MLflow experiment tracking
* Add automated testing
* Add CI/CD pipeline
* Add authentication for production use
* Deploy backend and frontend

---

## Reports

Detailed project reports are available in the `reports/` folder:

```text
reports/model_performance_report.md
reports/customer_segmentation_report.md
reports/api_documentation.md
```

---

## Notes

Generated datasets and model files are not pushed to GitHub because they are ignored using `.gitignore`.

Ignored folders:

```text
data/raw/
data/interim/
data/processed/
models/
logs/
venv/
```

To reproduce the project locally, place the dataset in `data/raw/`, then run the data pipeline and model training scripts.

---

---

## Testing

This project includes basic unit tests for core logic.

Test files:

```text
tests/test_data_cleaning.py
tests/test_feature_engineering.py
tests/test_prediction.py


python -m pytest tests/

The tests validate:

Data cleaning logic
Duplicate removal
Numeric value validation
Churn label creation
Feature engineering logic
Risk level mapping
Business recommendation logic

## Author

Nayan Tupe
