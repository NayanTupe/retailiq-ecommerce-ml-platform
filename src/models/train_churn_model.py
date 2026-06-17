import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


PROCESSED_DATA_PATH = Path("data/processed/final_features.csv")
MODEL_PATH = Path("models/churn_model.pkl")
PREPROCESSOR_PATH = Path("models/preprocessor.pkl")


def load_features() -> pd.DataFrame:
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(f"Feature file not found: {PROCESSED_DATA_PATH}")

    return pd.read_csv(PROCESSED_DATA_PATH)


def prepare_data(df: pd.DataFrame):
    """
    Prepare features and target for churn prediction.

    Leakage columns removed because churn label was created using:
    - days_since_last_purchase
    - satisfaction_level
    - is_inactive_customer
    """

    target = "churn"

    drop_columns = [
        "customer_id",
        "churn",
        "days_since_last_purchase",
        "satisfaction_level",
        "is_inactive_customer"
    ]

    X = df.drop(columns=drop_columns)
    y = df[target]

    categorical_features = [
        "gender",
        "city",
        "membership_type",
        "discount_applied"
    ]

    numerical_features = [
        "age",
        "total_spend",
        "items_purchased",
        "average_rating",
        "avg_spend_per_item",
        "is_high_value_customer",
        "is_frequent_buyer",
        "low_rating_flag",
        "discount_used_flag"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ]
    )

    return X, y, preprocessor


def train_churn_model(X_train, y_train, preprocessor):
    """
    Train Random Forest churn prediction model.
    """

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    return pipeline


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance.
    """

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\nModel Performance")
    print("=" * 50)

    print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
    print("Precision:", round(precision_score(y_test, y_pred), 4))
    print("Recall:", round(recall_score(y_test, y_pred), 4))
    print("F1 Score:", round(f1_score(y_test, y_pred), 4))
    print("ROC AUC:", round(roc_auc_score(y_test, y_proba), 4))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


def save_model(model):
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved successfully at: {MODEL_PATH}")


if __name__ == "__main__":
    df = load_features()

    X, y, preprocessor = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Training rows:", X_train.shape[0])
    print("Testing rows:", X_test.shape[0])

    churn_model = train_churn_model(X_train, y_train, preprocessor)

    evaluate_model(churn_model, X_test, y_test)

    save_model(churn_model)