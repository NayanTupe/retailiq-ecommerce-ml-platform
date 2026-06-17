from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.churn_routes import router as churn_router


app = FastAPI(
    title="RetailIQ API",
    description="API for ecommerce customer churn prediction and analytics",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(churn_router)


@app.get("/")
def root():
    return {
        "message": "RetailIQ API is running successfully",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RetailIQ Churn Prediction API"
    }