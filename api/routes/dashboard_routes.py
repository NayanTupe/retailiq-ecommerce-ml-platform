import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/analytics",
    tags=["Dashboard Analytics"]
)

# -----------------------------
# DATA PATHS
# -----------------------------
SEGMENTED_DATA_PATH = Path("data/processed/customer_segments.csv")
FEATURE_DATA_PATH = Path("data/processed/final_features.csv")


# -----------------------------
# LOAD DATA FUNCTION
# -----------------------------
def load_dashboard_data() -> pd.DataFrame:
    if SEGMENTED_DATA_PATH.exists():
        return pd.read_csv(SEGMENTED_DATA_PATH)

    if FEATURE_DATA_PATH.exists():
        return pd.read_csv(FEATURE_DATA_PATH)

    raise FileNotFoundError(
        "Processed data not found. Please run feature engineering and segmentation first."
    )


# -----------------------------
# 1. SUMMARY API
# -----------------------------
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


# -----------------------------
# 2. SEGMENTS API
# -----------------------------
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


# -----------------------------
# 3. CHURN BY MEMBERSHIP API
# -----------------------------
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


# -----------------------------
# 4. COMPREHENSIVE DETAILS API
# -----------------------------
@router.get("/details")
def get_details():
    try:
        df = load_dashboard_data()

        # 1. KPIs
        total_customers = int(df["customer_id"].nunique())
        total_revenue = round(float(df["total_spend"].sum()), 2)
        average_spend = round(float(df["total_spend"].mean()), 2)
        churn_rate = round(float(df["churn"].mean() * 100), 2)
        average_rating = round(float(df["average_rating"].mean()), 2)

        # 2. Revenue & Churn by City
        city_data = (
            df.groupby("city")
            .agg(
                revenue=("total_spend", "sum"),
                churn_rate=("churn", "mean"),
                customers=("customer_id", "count")
            )
            .reset_index()
        )
        city_data["churn_rate"] = (city_data["churn_rate"] * 100).round(2)
        city_data["revenue"] = city_data["revenue"].round(2)
        city_list = city_data.to_dict(orient="records")

        # 3. Membership Mix & Churn
        mem_data = (
            df.groupby("membership_type")
            .agg(
                customers=("customer_id", "count"),
                churn_rate=("churn", "mean"),
                revenue=("total_spend", "sum"),
                average_spend=("total_spend", "mean"),
                average_rating=("average_rating", "mean")
            )
            .reset_index()
        )
        mem_data["churn_rate"] = (mem_data["churn_rate"] * 100).round(2)
        mem_data["revenue"] = mem_data["revenue"].round(2)
        mem_data["average_spend"] = mem_data["average_spend"].round(2)
        mem_data["average_rating"] = mem_data["average_rating"].round(2)
        mem_list = mem_data.to_dict(orient="records")

        # 4. Age Distribution
        # Use simple integer bins for age distribution
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 25, 35, 45, 55, 65, 120],
            labels=["Under 25", "25-34", "35-44", "45-54", "55-64", "65+"]
        )
        age_data = df.groupby("age_group", observed=False)["customer_id"].count().reset_index()
        age_data.columns = ["age_group", "customers"]
        age_list = age_data.to_dict(orient="records")

        # 5. Churn Distribution
        churn_counts = df["churn"].value_counts().to_dict()
        churn_dist = {
            "no_churn": int(churn_counts.get(0, 0)),
            "churn_risk": int(churn_counts.get(1, 0))
        }

        # 6. Rating Quality (low_rating_flag check)
        if "low_rating_flag" not in df.columns:
            df["low_rating_flag"] = (df["average_rating"] < 3.0).astype(int)

        rating_churn = (
            df.groupby("low_rating_flag")
            .agg(
                customers=("customer_id", "count"),
                churn_rate=("churn", "mean")
            )
            .reset_index()
        )
        rating_churn["rating_group"] = rating_churn["low_rating_flag"].map({
            0: "Normal Rating (3-5)",
            1: "Low Rating (1-2)"
        })
        rating_churn["churn_rate"] = (rating_churn["churn_rate"] * 100).round(2)
        rating_list = rating_churn[["rating_group", "customers", "churn_rate"]].to_dict(orient="records")

        # 7. Segments
        segments_list = []
        if "segment_name" in df.columns:
            seg_data = (
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
            seg_data["churn_rate"] = (seg_data["churn_rate"] * 100).round(2)
            seg_data["total_revenue"] = seg_data["total_revenue"].round(2)
            seg_data["average_spend"] = seg_data["average_spend"].round(2)
            seg_data["average_rating"] = seg_data["average_rating"].round(2)
            segments_list = seg_data.to_dict(orient="records")

        return {
            "summary": {
                "total_customers": total_customers,
                "total_revenue": total_revenue,
                "average_spend": average_spend,
                "churn_rate": churn_rate,
                "average_rating": average_rating
            },
            "revenue_by_city": city_list,
            "membership_mix": mem_list,
            "age_distribution": age_list,
            "churn_distribution": churn_dist,
            "rating_quality": rating_list,
            "segments": segments_list
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))