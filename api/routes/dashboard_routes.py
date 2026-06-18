import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/analytics",
    tags=["Dashboard Analytics"]
)


SEGMENTED_DATA_PATH = Path("data/processed/customer_segments.csv")
FEATURE_DATA_PATH = Path("data/processed/final_features.csv")


def load_dashboard_data() -> pd.DataFrame:
    if SEGMENTED_DATA_PATH.exists():
        return pd.read_csv(SEGMENTED_DATA_PATH)

    if FEATURE_DATA_PATH.exists():
        return pd.read_csv(FEATURE_DATA_PATH)

    raise FileNotFoundError(
        "Processed data not found. Please run feature engineering and segmentation first."
    )


@router.get("/summary")
def get_summary():
    try:
        df = load_dashboard_data()

        return {
            "total_customers": int(df["customer_id"].nunique()),
            "total_revenue": round(float(df["total_spend"].sum()), 2),
            "average_spend": round(float(df["total_spend"].mean()), 2),
            "churn_rate": round(float(df["churn"].mean() * 100), 2),
            "average_rating": round(float(df["average_rating"].mean()), 2)
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/segments")
def get_segments():
    try:
        df = load_dashboard_data()

        if "segment_name" not in df.columns:
            raise HTTPException(
                status_code=404,
                detail="Segment data not found. Run segmentation model first."
            )

        segment_summary = (
            df.groupby("segment_name")
            .agg(
                customers=("customer_id", "count"),
                total_revenue=("total_spend", "sum"),
                average_spend=("total_spend", "mean"),
                average_rating=("average_rating", "mean"),
                churn_rate=("churn", "mean")
            )
            .reset_index()
        )

        segment_summary["churn_rate"] = segment_summary["churn_rate"] * 100

        return segment_summary.round(2).to_dict(orient="records")

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/churn-by-membership")
def get_churn_by_membership():
    try:
        df = load_dashboard_data()

        churn_summary = (
            df.groupby("membership_type")
            .agg(
                customers=("customer_id", "count"),
                churn_rate=("churn", "mean"),
                average_spend=("total_spend", "mean")
            )
            .reset_index()
        )

        churn_summary["churn_rate"] = churn_summary["churn_rate"] * 100

        return churn_summary.round(2).to_dict(orient="records")

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))