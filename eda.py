# eda.py — Exploratory Data Analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqldatabase_connection import load_data

df = load_data()

# ── 1. Basic Info ─────────────────────────────────────
print("Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())
print("\nChurn Distribution:\n", df['Churn'].value_counts())

# ── 2. Churn Count Plot ───────────────────────────────
plt.figure(figsize=(6, 4))
df['Churn'].value_counts().plot(kind='bar', color=['#10b981', '#ef4444'], edgecolor='white')
plt.title('Customer Churn Distribution')
plt.xlabel('Churn'); plt.ylabel('Count')
plt.xticks(rotation=0); plt.tight_layout()
plt.savefig('static/churn_dist.png'); plt.show()

# ── 3. Tenure vs Churn ────────────────────────────────
plt.figure(figsize=(8, 4))
sns.histplot(data=df, x='Tenure', hue='Churn', bins=30, palette='coolwarm')
plt.title('Tenure Distribution by Churn')
plt.tight_layout(); plt.savefig('static/tenure_churn.png'); plt.show()

# ── 4. Monthly Charges vs Churn ───────────────────────
plt.figure(figsize=(8, 4))
sns.boxplot(x='Churn', y='MonthlyCharges', data=df, palette='Set2')
plt.title('Monthly Charges vs Churn')
plt.tight_layout(); plt.savefig('static/charges_churn.png'); plt.show()

# ── 5. Contract Type vs Churn ─────────────────────────
plt.figure(figsize=(8, 4))
sns.countplot(x='Contract', hue='Churn', data=df, palette='viridis')
plt.title('Contract Type vs Churn')
plt.tight_layout(); plt.savefig('static/contract_churn.png'); plt.show()

# ── 6. Correlation Heatmap ────────────────────────────
df_encoded = df.copy()
df_encoded['Churn_binary'] = (df_encoded['Churn'] == 'Yes').astype(int)
numeric_df = df_encoded.select_dtypes(include='number')
plt.figure(figsize=(10, 7))
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap='Blues', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout(); plt.savefig('static/heatmap.png'); plt.show()