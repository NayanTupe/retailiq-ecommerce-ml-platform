import os
import pandas as pd
import joblib
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/predict", tags=["Prediction"])

# =========================
# SAFE MODEL LOADING (RENDER FIX)
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_model.pkl")

model = joblib.load(MODEL_PATH)


# =========================
# INPUT SCHEMA
# =========================
class CustomerInput(BaseModel):
    age: int
    total_spend: float
    items_purchased: int
    average_rating: float


# =========================
# PREDICTION ENDPOINT
# =========================
@router.post("/churn")
def predict_churn(data: CustomerInput):

    # Convert input to DataFrame
    df = pd.DataFrame([data.dict()])

    # =========================
    # FEATURE ENGINEERING (SAFE)
    # =========================

    df["avg_spend_per_item"] = df["total_spend"] / max(df["items_purchased"].values[0], 1)

    df["is_high_value_customer"] = (df["total_spend"] > 10000).astype(int)

    df["is_frequent_buyer"] = (df["items_purchased"] > 5).astype(int)

    df["low_rating_flag"] = (df["average_rating"] < 3).astype(int)

    df["discount_used_flag"] = 1

    df["discount_applied"] = 1

    # categorical defaults (must match training)
    df["gender"] = "Male"
    df["city"] = "Unknown"
    df["membership_type"] = "Gold"

    # =========================
    # FINAL COLUMN ORDER
    # =========================
    expected_cols = [
        "age",
        "total_spend",
        "items_purchased",
        "average_rating",
        "avg_spend_per_item",
        "is_high_value_customer",
        "is_frequent_buyer",
        "low_rating_flag",
        "discount_used_flag",
        "discount_applied",
        "gender",
        "city",
        "membership_type"
    ]

    df = df[expected_cols]

    # =========================
    # PREDICTION
    # =========================
    try:
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]

        return {
            "churn_prediction": "Yes" if prediction == 1 else "No",
            "churn_probability": round(probability * 100, 2),
            "risk_level": (
                "High Risk" if probability > 0.7
                else "Medium Risk" if probability > 0.4
                else "Low Risk"
            )
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Model prediction failed. Check feature mismatch or model file."
        }