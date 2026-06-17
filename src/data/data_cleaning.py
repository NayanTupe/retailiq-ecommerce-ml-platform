import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("data/raw/ecommerce_customer_data.csv")
INTERIM_DATA_PATH = Path("data/interim/cleaned_customer_data.csv")


def load_data() -> pd.DataFrame:
    """
    Load raw ecommerce customer data.
    """
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Raw data file not found: {RAW_DATA_PATH}")

    return pd.read_csv(RAW_DATA_PATH)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names to clean snake_case format.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean ecommerce customer dataset.
    """
    df = df.copy()

    df = clean_column_names(df)

    df = df.drop_duplicates()

    categorical_columns = [
        "gender",
        "city",
        "membership_type",
        "satisfaction_level"
    ]

    for col in categorical_columns:
        df[col] = df[col].astype(str).str.strip().str.title()

    df["discount_applied"] = df["discount_applied"].astype(bool)

    numeric_columns = [
        "age",
        "total_spend",
        "items_purchased",
        "average_rating",
        "days_since_last_purchase"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    df = df[
        (df["age"] >= 10) &
        (df["age"] <= 100) &
        (df["total_spend"] >= 0) &
        (df["items_purchased"] >= 0) &
        (df["average_rating"] >= 0) &
        (df["average_rating"] <= 5) &
        (df["days_since_last_purchase"] >= 0)
    ]

    return df


def save_clean_data(df: pd.DataFrame) -> None:
    """
    Save cleaned data to data/interim folder.
    """
    INTERIM_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(INTERIM_DATA_PATH, index=False)
    print(f"Cleaned data saved successfully at: {INTERIM_DATA_PATH}")


if __name__ == "__main__":
    raw_df = load_data()
    cleaned_df = clean_data(raw_df)

    print("Raw shape:", raw_df.shape)
    print("Cleaned shape:", cleaned_df.shape)

    print("\nCleaned Columns:")
    print(cleaned_df.columns.tolist())

    print("\nMissing Values:")
    print(cleaned_df.isnull().sum())

    print("\nDuplicate Rows:")
    print(cleaned_df.duplicated().sum())

    print("\nSample Data:")
    print(cleaned_df.head())

    save_clean_data(cleaned_df)