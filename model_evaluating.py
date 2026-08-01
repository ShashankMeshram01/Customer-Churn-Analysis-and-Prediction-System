# evaluate.py — Full model evaluation and charts
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import (classification_report, confusion_matrix,
                               roc_curve, auc, accuracy_score)
from model_training import train_all_models

model, X_test, y_test = train_all_models()
y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# ── 1. Classification Report ──────────────────────────
print("\n━━━ Classification Report ━━━")
print(classification_report(y_test, y_pred))

# ── 2. Confusion Matrix ───────────────────────────────
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Churn','Churn'],
            yticklabels=['No Churn','Churn'])
plt.title('Confusion Matrix')
plt.ylabel('Actual'); plt.xlabel('Predicted')
plt.tight_layout(); plt.savefig('static/confusion_matrix.png'); plt.show()

# ── 3. ROC Curve ──────────────────────────────────────
fpr, tpr, _ = roc_curve(y_test, y_proba, pos_label='Yes')
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, color='darkorange', lw=2,
         label=f'AUC = {roc_auc:.3f}')
plt.plot([0,1],[0,1],'--',color='gray')
plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate')
plt.title('ROC Curve'); plt.legend(); plt.tight_layout()
plt.savefig('static/roc_curve.png'); plt.show()

# ── 4. Feature Importance (if supported) ─────────────
if hasattr(model, 'feature_importances_'):
    feature_names = joblib.load('feature_names.pkl')
    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:15]    # top 15
    plt.figure(figsize=(9, 5))
    plt.bar(range(15), importances[idx], color='steelblue')
    plt.xticks(range(15), [feature_names[i] for i in idx], rotation=45, ha='right')
    plt.title('Top 15 Feature Importances')
    plt.tight_layout(); plt.savefig('static/feature_importance.png'); plt.show()

print(f"\n✅ Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%  |  AUC: {roc_auc:.3f}")