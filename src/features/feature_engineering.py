import pandas as pd
from pathlib import Path


INTERIM_DATA_PATH = Path("data/interim/cleaned_customer_data.csv")
PROCESSED_DATA_PATH = Path("data/processed/final_features.csv")


def load_clean_data() -> pd.DataFrame:
    """
    Load cleaned customer data.
    """
    if not INTERIM_DATA_PATH.exists():
        raise FileNotFoundError(f"Cleaned data file not found: {INTERIM_DATA_PATH}")

    return pd.read_csv(INTERIM_DATA_PATH)


def create_churn_label(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create churn label using business logic.

    Churn = 1 if:
    - days_since_last_purchase >= 45
    OR
    - satisfaction_level is Unsatisfied
    """
    df = df.copy()

    df["churn"] = (
        (df["days_since_last_purchase"] >= 45) |
        (df["satisfaction_level"] == "Unsatisfied")
    ).astype(int)

    return df


def create_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create business and ML-ready features.
    """
    df = df.copy()

    df["avg_spend_per_item"] = df["total_spend"] / df["items_purchased"].replace(0, 1)

    df["is_high_value_customer"] = (
        df["total_spend"] >= df["total_spend"].quantile(0.75)
    ).astype(int)

    df["is_frequent_buyer"] = (
        df["items_purchased"] >= df["items_purchased"].quantile(0.75)
    ).astype(int)

    df["is_inactive_customer"] = (
        df["days_since_last_purchase"] >= 45
    ).astype(int)

    df["low_rating_flag"] = (
        df["average_rating"] < 3
    ).astype(int)

    df["discount_used_flag"] = df["discount_applied"].astype(int)

    return df


def save_features(df: pd.DataFrame) -> None:
    """
    Save final feature-engineered dataset.
    """
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Feature-engineered data saved at: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    df = load_clean_data()

    df = create_churn_label(df)
    df = create_customer_features(df)

    print("Final shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nChurn Distribution:")
    print(df["churn"].value_counts())
    print(df["churn"].value_counts(normalize=True) * 100)

    print("\nSample Data:")
    print(df.head())

    save_features(df)