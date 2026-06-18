import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

DATA_PATH = Path("data/processed/final_features.csv")
MODEL_PATH = Path("models/churn_model.pkl")


def load_data():
    return pd.read_csv(DATA_PATH)


def prepare_data(df):
    target = "churn"

    drop_cols = [
        "customer_id",
        "churn",
        "days_since_last_purchase",
        "satisfaction_level",
        "is_inactive_customer"
    ]

    X = df.drop(columns=drop_cols)
    y = df[target]

    return X, y


def train_model(X_train, y_train):

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)
    return model


def save_model(model):
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("Model saved at:", MODEL_PATH)


if __name__ == "__main__":

    df = load_data()

    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    model = train_model(X_train, y_train)

    preds = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))

    save_model(model)