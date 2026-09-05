import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                              confusion_matrix, roc_auc_score, roc_curve, ConfusionMatrixDisplay)
from preprocess_helper import prepare_data
import csv
import os

df = pd.read_csv("outputs/data_engineered.csv")
X, y = prepare_data(df)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Train shape:", X_train.shape, "Test shape:", X_test.shape)
print("Train churn ratio:\n", y_train.value_counts(normalize=True))
print("Test churn ratio:\n", y_test.value_counts(normalize=True))

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Decision Tree": DecisionTreeClassifier(random_state=42, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(random_state=42, class_weight="balanced")
}

log_rows = []
results_summary = []
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)

    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="f1")

    print("\nModel:", name)
    print("Accuracy:", round(acc, 4))
    print("Precision:", round(prec, 4))
    print("Recall:", round(rec, 4))
    print("F1 Score:", round(f1, 4))
    print("ROC-AUC:", round(roc_auc, 4))
    print("Cross Val F1 scores:", cv_scores)
    print("Cross Val F1 mean:", round(cv_scores.mean(), 4))
    print("Confusion Matrix:\n", cm)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Churn", "Churn"])
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix - " + name)
    plt.tight_layout()
    plt.savefig("screenshots/cm_" + name.replace(" ", "_") + ".png")
    plt.close()

    results_summary.append({
        "Model": name,
        "Accuracy": round(acc, 4),
        "Precision": round(prec, 4),
        "Recall": round(rec, 4),
        "F1 Score": round(f1, 4),
        "ROC-AUC": round(roc_auc, 4),
        "CV F1 Mean": round(cv_scores.mean(), 4)
    })

    log_rows.append({
        "Experiment": "Baseline Model Comparison",
        "Model": name,
        "Parameters": str(model.get_params()),
        "Accuracy": round(acc, 4),
        "Precision": round(prec, 4),
        "Recall": round(rec, 4),
        "F1_Score": round(f1, 4),
        "ROC_AUC": round(roc_auc, 4),
        "CV_F1_Mean": round(cv_scores.mean(), 4)
    })

plt.figure(figsize=(7, 6))
for name, model in models.items():
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.plot(fpr, tpr, label=name)

plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.tight_layout()
plt.savefig("screenshots/05_roc_curve_comparison.png")
plt.close()

summary_df = pd.DataFrame(results_summary)
print("\nFinal Comparison Table:")
print(summary_df)
summary_df.to_csv("outputs/model_comparison_baseline.csv", index=False)

log_file = "experiment_log.csv"
file_exists = os.path.isfile(log_file)
with open(log_file, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=log_rows[0].keys())
    if not file_exists:
        writer.writeheader()
    for row in log_rows:
        writer.writerow(row)

print("\nExperiment results logged to experiment_log.csv")
