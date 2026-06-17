import pandas as pd
import joblib
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


PROCESSED_DATA_PATH = Path("data/processed/final_features.csv")
SEGMENT_MODEL_PATH = Path("models/segmentation_model.pkl")
SCALER_PATH = Path("models/segmentation_scaler.pkl")
SEGMENTED_DATA_PATH = Path("data/processed/customer_segments.csv")


def load_features() -> pd.DataFrame:
    """
    Load feature-engineered customer dataset.
    """
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(f"Feature file not found: {PROCESSED_DATA_PATH}")

    return pd.read_csv(PROCESSED_DATA_PATH)


def prepare_segmentation_features(df: pd.DataFrame):
    """
    Select customer behavior features for segmentation.
    """
    segmentation_features = [
        "age",
        "total_spend",
        "items_purchased",
        "average_rating",
        "avg_spend_per_item",
        "discount_used_flag",
        "low_rating_flag",
        "is_high_value_customer",
        "is_frequent_buyer"
    ]

    X = df[segmentation_features].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled, scaler, segmentation_features


def train_kmeans_model(X_scaled, n_clusters: int = 4):
    """
    Train KMeans customer segmentation model.
    """
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    return model


def assign_segment_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign business-friendly segment names based on customer behavior.
    """
    df = df.copy()

    segment_summary = df.groupby("customer_segment").agg(
        avg_total_spend=("total_spend", "mean"),
        avg_items_purchased=("items_purchased", "mean"),
        avg_rating=("average_rating", "mean"),
        churn_rate=("churn", "mean")
    ).reset_index()

    spend_rank = segment_summary["avg_total_spend"].rank(method="dense", ascending=False)
    churn_rank = segment_summary["churn_rate"].rank(method="dense", ascending=False)

    segment_name_map = {}

    for index, row in segment_summary.iterrows():
        segment_id = row["customer_segment"]

        if row["avg_total_spend"] == segment_summary["avg_total_spend"].max():
            segment_name = "High Value Customers"
        elif row["churn_rate"] == segment_summary["churn_rate"].max():
            segment_name = "At Risk Customers"
        elif row["avg_rating"] >= segment_summary["avg_rating"].median():
            segment_name = "Satisfied Regular Customers"
        else:
            segment_name = "Low Engagement Customers"

        segment_name_map[segment_id] = segment_name

    df["segment_name"] = df["customer_segment"].map(segment_name_map)

    return df


def save_outputs(model, scaler, segmented_df: pd.DataFrame):
    """
    Save segmentation model, scaler, and segmented customer data.
    """
    SEGMENT_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEGMENTED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, SEGMENT_MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    segmented_df.to_csv(SEGMENTED_DATA_PATH, index=False)

    print(f"Segmentation model saved at: {SEGMENT_MODEL_PATH}")
    print(f"Scaler saved at: {SCALER_PATH}")
    print(f"Segmented data saved at: {SEGMENTED_DATA_PATH}")


if __name__ == "__main__":
    df = load_features()

    X, X_scaled, scaler, segmentation_features = prepare_segmentation_features(df)

    model = train_kmeans_model(X_scaled, n_clusters=4)

    df["customer_segment"] = model.labels_

    df = assign_segment_names(df)

    score = silhouette_score(X_scaled, model.labels_)

    print("\nCustomer Segmentation Completed")
    print("=" * 50)

    print("\nFeatures Used:")
    print(segmentation_features)

    print("\nSilhouette Score:")
    print(round(score, 4))

    print("\nSegment Distribution:")
    print(df["segment_name"].value_counts())

    print("\nSegment Summary:")
    print(
        df.groupby("segment_name").agg(
            customers=("customer_id", "count"),
            avg_total_spend=("total_spend", "mean"),
            avg_items_purchased=("items_purchased", "mean"),
            avg_rating=("average_rating", "mean"),
            churn_rate=("churn", "mean")
        ).round(2)
    )

    save_outputs(model, scaler, df)