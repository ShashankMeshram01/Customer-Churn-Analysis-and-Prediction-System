"""
Customer Churn Analysis
========================
Connects to MySQL and produces a full visual analysis report.

Requirements:
    pip install mysql-connector-python pandas matplotlib seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import mysql.connector

# ─────────────────────────────────────────
# 1. CONNECTION — fill in your credentials
# ─────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",       # ← change this
    password="869627",   # ← change this
    database="CUSTOMER_CHURN_PROJECT"
)

df = pd.read_sql("SELECT * FROM Customers", conn)
conn.close()

# ─────────────────────────────────────────
# 2. BASIC CLEANING
# ─────────────────────────────────────────
df.columns = df.columns.str.strip()
df['Churn'] = df['Churn'].str.strip().str.title()          # 'Yes' / 'No'
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(subset=['TotalCharges'], inplace=True)

churn_colors = {'Yes': '#e74c3c', 'No': '#2ecc71'}

# ─────────────────────────────────────────
# 3. HELPER
# ─────────────────────────────────────────
def churn_rate_by(col, ax, title):
    ct = df.groupby([col, 'Churn']).size().unstack(fill_value=0)
    ct['Rate'] = ct.get('Yes', 0) / (ct.get('Yes', 0) + ct.get('No', 0)) * 100
    ct['Rate'].sort_values().plot(kind='barh', ax=ax, color='#3498db', edgecolor='white')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Churn Rate (%)')
    ax.set_ylabel('')
    for bar in ax.patches:
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.1f}%", va='center', fontsize=9)

# ─────────────────────────────────────────
# 4. FIGURE 1 — Overview + Demographics
# ─────────────────────────────────────────
fig1, axes = plt.subplots(2, 3, figsize=(18, 11))
fig1.suptitle("Customer Churn Analysis — Overview & Demographics", fontsize=16, fontweight='bold', y=1.01)

# 4a. Overall churn pie
churn_counts = df['Churn'].value_counts()
axes[0, 0].pie(
    churn_counts,
    labels=churn_counts.index,
    autopct='%1.1f%%',
    colors=[churn_colors.get(c, '#95a5a6') for c in churn_counts.index],
    startangle=90,
    wedgeprops=dict(edgecolor='white', linewidth=2)
)
axes[0, 0].set_title("Overall Churn Rate", fontsize=12, fontweight='bold')

# 4b. Churn by Gender
churn_rate_by('Gender', axes[0, 1], "Churn Rate by Gender")

# 4c. Churn by Senior Citizen
df['SeniorLabel'] = df['SeniorCitizen'].map({0: 'Non-Senior', 1: 'Senior'})
churn_rate_by('SeniorLabel', axes[0, 2], "Churn Rate by Senior Citizen")

# 4d. Churn by Partner
churn_rate_by('Partner', axes[1, 0], "Churn Rate by Partner")

# 4e. Churn by Dependents
churn_rate_by('Dependents', axes[1, 1], "Churn Rate by Dependents")

# 4f. Tenure distribution by churn
for label, grp in df.groupby('Churn'):
    axes[1, 2].hist(grp['Tenure'], bins=20, alpha=0.6, label=label,
                    color=churn_colors.get(label, '#95a5a6'), edgecolor='white')
axes[1, 2].set_title("Tenure Distribution by Churn", fontsize=12, fontweight='bold')
axes[1, 2].set_xlabel("Tenure (months)")
axes[1, 2].set_ylabel("Count")
axes[1, 2].legend()

plt.tight_layout()
fig1.savefig("churn_overview_demographics.png", dpi=150, bbox_inches='tight')
print("Saved: churn_overview_demographics.png")

# ─────────────────────────────────────────
# 5. FIGURE 2 — Services
# ─────────────────────────────────────────
service_cols = ['PhoneService', 'MultipleLines', 'InternetService',
                'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                'TechSupport', 'StreamingTv', 'StreamingMovies']

fig2, axes2 = plt.subplots(3, 3, figsize=(18, 14))
fig2.suptitle("Customer Churn Analysis — Services", fontsize=16, fontweight='bold', y=1.01)

for ax, col in zip(axes2.flatten(), service_cols):
    churn_rate_by(col, ax, f"Churn by {col}")

plt.tight_layout()
fig2.savefig("churn_services.png", dpi=150, bbox_inches='tight')
print("Saved: churn_services.png")

# ─────────────────────────────────────────
# 6. FIGURE 3 — Contract & Payment
# ─────────────────────────────────────────
fig3, axes3 = plt.subplots(1, 3, figsize=(18, 6))
fig3.suptitle("Customer Churn Analysis — Contract & Payment", fontsize=16, fontweight='bold')

churn_rate_by('Contract', axes3[0], "Churn by Contract Type")
churn_rate_by('PapelessBilling', axes3[1], "Churn by Paperless Billing")
churn_rate_by('PaymentMethod', axes3[2], "Churn by Payment Method")

plt.tight_layout()
fig3.savefig("churn_contract_payment.png", dpi=150, bbox_inches='tight')
print("Saved: churn_contract_payment.png")

# ─────────────────────────────────────────
# 7. FIGURE 4 — Charges Analysis
# ─────────────────────────────────────────
fig4, axes4 = plt.subplots(1, 3, figsize=(18, 6))
fig4.suptitle("Customer Churn Analysis — Charges", fontsize=16, fontweight='bold')

# Monthly charges box
df.boxplot(column='MonthlyCharges', by='Churn', ax=axes4[0],
           patch_artist=True,
           boxprops=dict(facecolor='#3498db', color='navy'),
           medianprops=dict(color='red', linewidth=2))
axes4[0].set_title("Monthly Charges by Churn")
axes4[0].set_xlabel("Churn")
axes4[0].set_ylabel("Monthly Charges ($)")
plt.sca(axes4[0]); plt.title("Monthly Charges by Churn")

# Total charges box
df.boxplot(column='TotalCharges', by='Churn', ax=axes4[1],
           patch_artist=True,
           boxprops=dict(facecolor='#e67e22', color='saddlebrown'),
           medianprops=dict(color='red', linewidth=2))
axes4[1].set_title("Total Charges by Churn")
axes4[1].set_xlabel("Churn")
axes4[1].set_ylabel("Total Charges ($)")
plt.sca(axes4[1]); plt.title("Total Charges by Churn")

# Scatter: Monthly vs Total coloured by Churn
for label, grp in df.groupby('Churn'):
    axes4[2].scatter(grp['Tenure'], grp['MonthlyCharges'],
                     alpha=0.3, s=10, label=label,
                     color=churn_colors.get(label, '#95a5a6'))
axes4[2].set_title("Tenure vs Monthly Charges")
axes4[2].set_xlabel("Tenure (months)")
axes4[2].set_ylabel("Monthly Charges ($)")
axes4[2].legend()

plt.tight_layout()
fig4.savefig("churn_charges.png", dpi=150, bbox_inches='tight')
print("Saved: churn_charges.png")

# ─────────────────────────────────────────
# 8. SUMMARY STATS
# ─────────────────────────────────────────
print("\n========== SUMMARY ==========")
total = len(df)
churned = (df['Churn'] == 'Yes').sum()
print(f"Total Customers  : {total}")
print(f"Churned          : {churned} ({churned/total*100:.1f}%)")
print(f"Avg Tenure       : {df['Tenure'].mean():.1f} months")
print(f"Avg Monthly Charge: ${df['MonthlyCharges'].mean():.2f}")
print(f"Avg Total Charge  : ${df['TotalCharges'].mean():.2f}")
print("==============================\n")

plt.show()
print("✅ All charts generated successfully!")
