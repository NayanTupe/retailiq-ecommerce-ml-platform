import joblib
import pandas as pd
from pathlib import Path


MODEL_PATH = Path("models/churn_model.pkl")


def load_model():
    """
    Load trained churn prediction model.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Please train the model first."
        )

    return joblib.load(MODEL_PATH)


def get_risk_level(probability: float) -> str:
    """
    Convert churn probability into business-friendly risk level.
    """
    if probability >= 0.75:
        return "High Risk"
    elif probability >= 0.50:
        return "Medium Risk"
    else:
        return "Low Risk"


def get_recommendation(risk_level: str) -> str:
    """
    Generate business recommendation based on churn risk.
    """
    recommendations = {
        "High Risk": "Offer retention discount, loyalty reward, or personal follow-up.",
        "Medium Risk": "Send personalized offers and monitor customer engagement.",
        "Low Risk": "Maintain regular communication and loyalty benefits."
    }

    return recommendations.get(risk_level, "No recommendation available.")


def predict_churn(customer_data: dict) -> dict:
    """
    Predict churn risk for a single customer.
    """
    model = load_model()

    input_df = pd.DataFrame([customer_data])

    churn_prediction = model.predict(input_df)[0]
    churn_probability = model.predict_proba(input_df)[0][1]

    risk_level = get_risk_level(churn_probability)
    recommendation = get_recommendation(risk_level)

    return {
        "churn_prediction": int(churn_prediction),
        "churn_probability": round(float(churn_probability), 4),
        "risk_level": risk_level,
        "recommendation": recommendation
    }


if __name__ == "__main__":
    sample_customer = {
        "gender": "Female",
        "age": 32,
        "city": "Miami",
        "membership_type": "Bronze",
        "total_spend": 166.56,
        "items_purchased": 2,
        "average_rating": 2.5,
        "discount_applied": True,
        "avg_spend_per_item": 83.28,
        "is_high_value_customer": 0,
        "is_frequent_buyer": 0,
        "low_rating_flag": 1,
        "discount_used_flag": 1
    }

    result = predict_churn(sample_customer)

    print("\nChurn Prediction Result")
    print("=" * 50)
    print(f"Churn Prediction: {'Yes' if result['churn_prediction'] == 1 else 'No'}")
    print(f"Churn Probability: {result['churn_probability'] * 100:.2f}%")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Recommendation: {result['recommendation']}")