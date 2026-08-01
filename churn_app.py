# app.py — Flask Web Application
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
from sqldatabase_connection import load_data

app = Flask(__name__)

# ── Models for the DASHBOARD / METRICS (full 19-feature model) ─────────
model         = joblib.load('model.pkl')
scaler        = joblib.load('scaler.pkl')
feature_names = joblib.load('feature_names.pkl')

# ── Model for the LIVE PREDICTION FORM (dedicated 4-feature model) ──────
model_4feat         = joblib.load('model_4feat.pkl')
scaler_4feat        = joblib.load('scaler_4feat.pkl')
feature_names_4feat = joblib.load('feature_names_4feat.pkl')  # ['SeniorCitizen','Tenure','MonthlyCharges','TotalCharges']


# ── Route 1: Home / Dashboard ─────────────────────────
@app.route('/')
def index():
    df = load_data()
    total      = len(df)
    churned    = int((df['Churn'] == 'Yes').sum())
    churn_pct  = round(churned / total * 100, 1)
    avg_tenure = round(df['Tenure'].mean(), 1)
    avg_charges = round(df['MonthlyCharges'].mean(), 2)
    return render_template('index.html',
        total=total, churned=churned, churn_pct=churn_pct,
        avg_tenure=avg_tenure, avg_charges=avg_charges)


# ── Route 2: Predict a single customer ────────────────
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Collect form data — these are EXACTLY the 4 features model_4feat was trained on
        senior_citizen = int(request.form['SeniorCitizen'])
        tenure         = float(request.form['tenure'])
        monthly        = float(request.form['MonthlyCharges'])
        total_charges  = float(request.form['TotalCharges'])

        df_input = pd.DataFrame(
            [[senior_citizen, tenure, monthly, total_charges]],
            columns=feature_names_4feat  # ['SeniorCitizen','Tenure','MonthlyCharges','TotalCharges']
        )

        # No reindex needed — df_input already has exactly the right 4 columns
        scaled = scaler_4feat.transform(df_input)

        pred = model_4feat.predict(scaled)[0]
        prob = model_4feat.predict_proba(scaled)[0][1] * 100  # P(class=1) = P(Churn)

        # Churn was mapped explicitly as {'No': 0, 'Yes': 1} during training,
        # so pred == 1 means the model predicts churn.
        label = "⚠️ Will Churn" if pred == 1 else "✅ Will Stay"

        return render_template('result.html',
            prediction=label,
            probability=round(prob, 2),
            form_data=request.form)

    return render_template('predict.html')


# ── Route 3: View database table (JSON) ───────────────
@app.route('/data')
def view_data():
    df = load_data()
    sample = df.head(50).to_dict(orient='records')
    return jsonify(sample)


if __name__ == '__main__':
    app.run(debug=True)