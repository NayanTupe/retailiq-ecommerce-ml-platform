import os
import pandas as pd
import joblib
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/predict", tags=["Prediction"])

# =========================
# SAFE MODEL LOADING (RENDER READY)
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_model.pkl")

model = None

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model loading failed:", str(e))


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

    # Safety check
    if model is None:
        return {
            "error": "Model not loaded",
            "message": "Check model file path or deployment"
        }

    # Convert input to DataFrame
    df = pd.DataFrame([data.dict()])

    # =========================
    # FEATURE ENGINEERING
    # =========================

    items = max(data.items_purchased, 1)

    df["avg_spend_per_item"] = data.total_spend / items
    df["is_high_value_customer"] = int(data.total_spend > 10000)
    df["is_frequent_buyer"] = int(data.items_purchased > 5)
    df["low_rating_flag"] = int(data.average_rating < 3)
    df["discount_used_flag"] = 1
    df["discount_applied"] = 1

    # categorical defaults
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
    # PREDICTION (SAFE)
    # =========================
    try:
        prediction = model.predict(df)[0]

        # safe probability handling
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(df)[0][1]
        else:
            probability = 0.5

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
            "message": "Prediction failed due to model/feature mismatch"
        }