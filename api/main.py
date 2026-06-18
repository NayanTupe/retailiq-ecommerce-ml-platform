from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.prediction_routes import router as prediction_router
from api.routes.dashboard_routes import router as dashboard_router

app = FastAPI(
    title="RetailIQ API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(prediction_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {"message": "RetailIQ API Running"}