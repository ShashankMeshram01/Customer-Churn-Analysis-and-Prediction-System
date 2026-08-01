# model_training.py — Train models and save the best one
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from preprocessing import preprocess


def train_all_models():
    """Trains the full (19-feature) models used for analysis/evaluation/reporting."""
    X_train, X_test, y_train, y_test, scaler, feature_names = preprocess()

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting":   GradientBoostingClassifier(n_estimators=100, random_state=42),
    }

    best_model, best_acc, best_name = None, 0, ""
    for name, model in models.items():
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        print(f"  {name}: {acc * 100:.2f}%")
        if acc > best_acc:
            best_acc, best_model, best_name = acc, model, name

    print(f"\n🏆 Best Model (full feature set): {best_name} ({best_acc*100:.2f}%)")

    # Save the full model + scaler — used for evaluation / metrics / reporting
    joblib.dump(best_model, 'model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(feature_names, 'feature_names.pkl')
    print("✅ Saved: model.pkl, scaler.pkl, feature_names.pkl (full 19-feature model)")

    return best_model, X_test, y_test


def train_prediction_form_model():
    """
    Trains a SEPARATE model using only the 4 features the live prediction
    form actually collects: SeniorCitizen, Tenure, MonthlyCharges, TotalCharges.

    Why: feeding a 19-feature model with 15 zero-filled (reindexed) columns
    produces an unrealistic, fixed "fake customer" profile that swamps the
    4 real inputs, causing predictions to barely change and collapse toward
    one class regardless of input. Training a dedicated model on exactly the
    4 fields the form provides avoids that mismatch entirely.
    """
    from sqldatabase_connection import load_data

    df = load_data()

    # Clean TotalCharges the same way preprocessing.py does
    import pandas as pd
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(subset=['TotalCharges'], inplace=True)

    # Force explicit, unambiguous target mapping — do NOT use LabelEncoder here
    df['Churn'] = df['Churn'].astype(str).str.strip().map({'No': 0, 'Yes': 1})

    features = ['SeniorCitizen', 'Tenure', 'MonthlyCharges', 'TotalCharges']
    X = df[features].copy()
    y = df['Churn']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler_4 = StandardScaler()
    X_train_scaled = scaler_4.fit_transform(X_train)
    X_test_scaled = scaler_4.transform(X_test)

    model_4 = LogisticRegression(max_iter=1000, random_state=42)
    model_4.fit(X_train_scaled, y_train)

    acc = accuracy_score(y_test, model_4.predict(X_test_scaled))
    print(f"\n📋 4-feature prediction-form model accuracy: {acc * 100:.2f}%")

    joblib.dump(model_4, 'model_4feat.pkl')
    joblib.dump(scaler_4, 'scaler_4feat.pkl')
    joblib.dump(features, 'feature_names_4feat.pkl')
    print("✅ Saved: model_4feat.pkl, scaler_4feat.pkl, feature_names_4feat.pkl")

    return model_4, X_test, y_test


if __name__ == "__main__":
    print("Training full 19-feature model (for dashboard/metrics)...")
    train_all_models()

    print("\nTraining 4-feature model (for live prediction form)...")
    train_prediction_form_model()