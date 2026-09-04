import time
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import json

df = pd.read_csv("dataset.csv")

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [None, 5, 10, 20],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

rf = RandomForestClassifier(random_state=42)

grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    verbose=1
)

start_time = time.time()
grid_search.fit(X_train, y_train)
end_time = time.time()

tuning_time = end_time - start_time
best_params = grid_search.best_params_
best_cv_score = grid_search.best_score_

print("HYPERPARAMETER TUNING RESULTS (GridSearchCV)")
print("Best Parameters:", best_params)
print("Best Cross Validation Accuracy:", best_cv_score)
print("Tuning Time (seconds):", tuning_time)

optimized_model = grid_search.best_estimator_
y_pred_optimized = optimized_model.predict(X_test)

optimized_accuracy = accuracy_score(y_test, y_pred_optimized)
optimized_precision = precision_score(y_test, y_pred_optimized)
optimized_recall = recall_score(y_test, y_pred_optimized)
optimized_f1 = f1_score(y_test, y_pred_optimized)

print("OPTIMIZED RANDOM FOREST MODEL (BEST PARAMETERS)")
print("Accuracy:", optimized_accuracy)
print("Precision:", optimized_precision)
print("Recall:", optimized_recall)
print("F1 Score:", optimized_f1)

with open("results/tuning_results.txt", "w") as f:
    f.write("HYPERPARAMETER TUNING RESULTS (GridSearchCV)\n")
    f.write("Best Parameters: " + str(best_params) + "\n")
    f.write("Best Cross Validation Accuracy: " + str(best_cv_score) + "\n")
    f.write("Tuning Time (seconds): " + str(tuning_time) + "\n\n")
    f.write("OPTIMIZED RANDOM FOREST MODEL (TEST SET RESULTS)\n")
    f.write("Accuracy: " + str(optimized_accuracy) + "\n")
    f.write("Precision: " + str(optimized_precision) + "\n")
    f.write("Recall: " + str(optimized_recall) + "\n")
    f.write("F1 Score: " + str(optimized_f1) + "\n")

with open("results/best_params.json", "w") as f:
    json.dump(best_params, f, indent=4)

cm = confusion_matrix(y_test, y_pred_optimized)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens")
plt.title("Confusion Matrix - Optimized Model")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("results/confusion_matrix_optimized.png")
plt.close()
