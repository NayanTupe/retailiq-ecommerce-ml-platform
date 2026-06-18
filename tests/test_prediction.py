from src.models.predict import get_risk_level, get_recommendation


def test_get_risk_level_high():
    probability = 0.80
    result = get_risk_level(probability)

    assert result == "High Risk"


def test_get_risk_level_medium():
    probability = 0.60
    result = get_risk_level(probability)

    assert result == "Medium Risk"


def test_get_risk_level_low():
    probability = 0.30
    result = get_risk_level(probability)

    assert result == "Low Risk"


def test_get_recommendation_high_risk():
    result = get_recommendation("High Risk")

    assert result == "Offer retention discount, loyalty reward, or personal follow-up."


def test_get_recommendation_medium_risk():
    result = get_recommendation("Medium Risk")

    assert result == "Send personalized offers and monitor customer engagement."


def test_get_recommendation_low_risk():
    result = get_recommendation("Low Risk")

    assert result == "Maintain regular communication and loyalty benefits."
    