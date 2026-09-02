import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    classification_report
)

model = joblib.load("churn_model.pkl")
scaler = joblib.load("churn_scaler.pkl")

X_test = pd.read_csv("churn_X_test.csv")
y_test = pd.read_csv("churn_y_test.csv")["churn"]

X_test_scaled = scaler.transform(X_test)

y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)
cm = confusion_matrix(y_test, y_pred)

print("Classification Model Evaluation")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("ROC-AUC Score:", roc_auc)
print("Confusion Matrix:")
print(cm)
print(classification_report(y_test, y_pred))

results = {
    "Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1 Score": f1,
    "ROC-AUC": roc_auc
}

results_df = pd.DataFrame(list(results.items()), columns=["Metric", "Score"])
results_df.to_csv("classification_results.csv", index=False)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["No Churn", "Churn"], yticklabels=["No Churn", "Churn"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Churn Prediction")
plt.tight_layout()
plt.savefig("screenshots/confusion_matrix.png")
plt.close()

fpr, tpr, thresholds = roc_curve(y_test, y_prob)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label="ROC Curve (AUC = %.2f)" % roc_auc)
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Churn Prediction")
plt.legend()
plt.tight_layout()
plt.savefig("screenshots/roc_curve.png")
plt.close()

plt.figure(figsize=(6, 5))
plt.bar(results.keys(), results.values(), color="skyblue")
plt.ylim(0, 1)
plt.title("Classification Metrics Comparison")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("screenshots/classification_metrics_bar.png")
plt.close()

print("Evaluation finished and screenshots saved")
