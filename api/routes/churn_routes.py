from fastapi import APIRouter, HTTPException

from api.schemas.prediction_schema import CustomerInput, PredictionResponse
from api.services.prediction_service import predict_customer_churn


router = APIRouter(
    prefix="/predict",
    tags=["Churn Prediction"]
)


@router.post("/churn", response_model=PredictionResponse)
def predict_churn(customer: CustomerInput):
    try:
        customer_data = customer.model_dump()
        result = predict_customer_churn(customer_data)
        return result

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(error)}")