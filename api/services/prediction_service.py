import joblib
import pandas as pd
from pathlib import Path


MODEL_PATH = Path("models/churn_model.pkl")


def load_churn_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Please train the churn model first."
        )

    return joblib.load(MODEL_PATH)


def get_risk_level(probability: float) -> str:
    if probability >= 0.75:
        return "High Risk"
    elif probability >= 0.50:
        return "Medium Risk"
    return "Low Risk"


def get_recommendation(risk_level: str) -> str:
    recommendations = {
        "High Risk": "Offer retention discount, loyalty reward, or personal follow-up.",
        "Medium Risk": "Send personalized offers and monitor customer engagement.",
        "Low Risk": "Maintain regular communication and loyalty benefits."
    }

    return recommendations.get(risk_level, "No recommendation available.")


def predict_customer_churn(customer_data: dict) -> dict:
    model = load_churn_model()

    input_df = pd.DataFrame([customer_data])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    risk_level = get_risk_level(probability)
    recommendation = get_recommendation(risk_level)

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4),
        "risk_level": risk_level,
        "recommendation": recommendation
    }