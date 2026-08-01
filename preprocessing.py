# preprocess.py — Clean and encode the dataset
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sqldatabase_connection import load_data

def preprocess():
    df = load_data()

    # ── Step 1: Drop useless columns ──────────────────
    df = df.drop(columns=['CustomerId'], errors='ignore')

    # ── Step 2: Fix TotalCharges (may be string/empty) ─
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

    # ── Step 3: Fill other missing values ─────────────
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna(df[col].mode()[0])
    df['Churn'] = df['Churn'].str.strip()
    df['Churn'] = df['Churn'].map({'No': 0, 'Yes': 1})

    # ── Step 4: Encode binary Yes/No columns ──────────
    binary_cols = [col for col in df.columns
                   if df[col].nunique() == 2 and df[col].dtype == 'object']
    le = LabelEncoder()
    for col in binary_cols:
        df[col] = le.fit_transform(df[col])

    # ── Step 5: One-hot encode remaining categoricals ──
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # ── Step 6: Split features and target ─────────────
    X = df.drop(columns=['Churn'])
    y = df['Churn']

    # ── Step 7: Scale numeric features ────────────────
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ── Step 8: Train/Test split ──────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"✅ Train size: {len(X_train)}, Test size: {len(X_test)}")
    return X_train, X_test, y_train, y_test, scaler, X.columns.tolist()

if __name__ == "__main__":
    preprocess()