import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("data/raw/ecommerce_customer_data.csv")


def load_raw_data() -> pd.DataFrame:
    """
    Load raw ecommerce customer dataset from data/raw folder.
    """
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"CSV file not found at: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    return df


def basic_data_summary(df: pd.DataFrame) -> None:
    """
    Print basic dataset information.
    """
    print("\nDataset loaded successfully")
    print("=" * 50)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nDataset Info:")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())


if __name__ == "__main__":
    dataframe = load_raw_data()
    basic_data_summary(dataframe)