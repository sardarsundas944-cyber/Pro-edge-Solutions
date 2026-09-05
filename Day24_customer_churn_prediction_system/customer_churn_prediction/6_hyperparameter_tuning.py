import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                              confusion_matrix, roc_auc_score, ConfusionMatrixDisplay)
from preprocess_helper import prepare_data
import csv
import os

df = pd.read_csv("outputs/data_engineered.csv")
X, y = prepare_data(df)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

untuned_rf = RandomForestClassifier(random_state=42, class_weight="balanced")
untuned_rf.fit(X_train, y_train)
untuned_pred = untuned_rf.predict(X_test)
untuned_prob = untuned_rf.predict_proba(X_test)[:, 1]

param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [5, 10, 15, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42, class_weight="balanced"),
    param_grid=param_grid,
    scoring="f1",
    cv=cv,
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

print("Best Parameters Found:")
print(grid_search.best_params_)
print("Best CV F1 Score:", round(grid_search.best_score_, 4))

tuned_rf = grid_search.best_estimator_
tuned_pred = tuned_rf.predict(X_test)
tuned_prob = tuned_rf.predict_proba(X_test)[:, 1]

def get_metrics(y_true, y_pred, y_prob):
    return {
        "Accuracy": round(accuracy_score(y_true, y_pred), 4),
        "Precision": round(precision_score(y_true, y_pred), 4),
        "Recall": round(recall_score(y_true, y_pred), 4),
        "F1 Score": round(f1_score(y_true, y_pred), 4),
        "ROC-AUC": round(roc_auc_score(y_true, y_prob), 4)
    }

untuned_metrics = get_metrics(y_test, untuned_pred, untuned_prob)
tuned_metrics = get_metrics(y_test, tuned_pred, tuned_prob)

print("\nUntuned Random Forest:", untuned_metrics)
print("Tuned Random Forest:", tuned_metrics)

compare_df = pd.DataFrame([
    {"Model": "Random Forest (Untuned)", **untuned_metrics},
    {"Model": "Random Forest (Tuned)", **tuned_metrics}
])
print("\n", compare_df)
compare_df.to_csv("outputs/tuned_vs_untuned_comparison.csv", index=False)

cm = confusion_matrix(y_test, tuned_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Churn", "Churn"])
disp.plot(cmap="Greens")
plt.title("Confusion Matrix - Tuned Random Forest")
plt.tight_layout()
plt.savefig("screenshots/cm_Tuned_Random_Forest.png")
plt.close()

importances = tuned_rf.feature_importances_
feat_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importances
}).sort_values(by="Importance", ascending=False).head(15)

plt.figure(figsize=(9, 7))
plt.barh(feat_importance_df["Feature"], feat_importance_df["Importance"], color="teal")
plt.gca().invert_yaxis()
plt.title("Top 15 Important Features - Tuned Random Forest")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("screenshots/06_feature_importance.png")
plt.close()

feat_importance_df.to_csv("outputs/feature_importance.csv", index=False)

log_rows = [
    {
        "Experiment": "Hyperparameter Tuning",
        "Model": "Random Forest (Untuned)",
        "Parameters": str(untuned_rf.get_params()),
        "Accuracy": untuned_metrics["Accuracy"],
        "Precision": untuned_metrics["Precision"],
        "Recall": untuned_metrics["Recall"],
        "F1_Score": untuned_metrics["F1 Score"],
        "ROC_AUC": untuned_metrics["ROC-AUC"],
        "CV_F1_Mean": ""
    },
    {
        "Experiment": "Hyperparameter Tuning",
        "Model": "Random Forest (Tuned)",
        "Parameters": str(grid_search.best_params_),
        "Accuracy": tuned_metrics["Accuracy"],
        "Precision": tuned_metrics["Precision"],
        "Recall": tuned_metrics["Recall"],
        "F1_Score": tuned_metrics["F1 Score"],
        "ROC_AUC": tuned_metrics["ROC-AUC"],
        "CV_F1_Mean": round(grid_search.best_score_, 4)
    }
]

log_file = "experiment_log.csv"
file_exists = os.path.isfile(log_file)
with open(log_file, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=log_rows[0].keys())
    if not file_exists:
        writer.writeheader()
    for row in log_rows:
        writer.writerow(row)

print("\nHyperparameter tuning results logged to experiment_log.csv")
