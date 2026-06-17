from pydantic import BaseModel


class CustomerInput(BaseModel):
    gender: str
    age: int
    city: str
    membership_type: str
    total_spend: float
    items_purchased: int
    average_rating: float
    discount_applied: bool
    avg_spend_per_item: float
    is_high_value_customer: int
    is_frequent_buyer: int
    low_rating_flag: int
    discount_used_flag: int


class PredictionResponse(BaseModel):
    churn_prediction: int
    churn_probability: float
    risk_level: str
    recommendation: str