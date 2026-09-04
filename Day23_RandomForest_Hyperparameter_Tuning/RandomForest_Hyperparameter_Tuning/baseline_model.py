import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dataset.csv")

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

start_time = time.time()

baseline_model = RandomForestClassifier(random_state=42)
baseline_model.fit(X_train, y_train)

end_time = time.time()

y_pred_baseline = baseline_model.predict(X_test)

baseline_accuracy = accuracy_score(y_test, y_pred_baseline)
baseline_precision = precision_score(y_test, y_pred_baseline)
baseline_recall = recall_score(y_test, y_pred_baseline)
baseline_f1 = f1_score(y_test, y_pred_baseline)
baseline_time = end_time - start_time

print("BASELINE RANDOM FOREST MODEL (DEFAULT PARAMETERS)")
print("Accuracy:", baseline_accuracy)
print("Precision:", baseline_precision)
print("Recall:", baseline_recall)
print("F1 Score:", baseline_f1)
print("Training Time (seconds):", baseline_time)
print("Default Parameters Used:", baseline_model.get_params())

with open("results/baseline_results.txt", "w") as f:
    f.write("BASELINE RANDOM FOREST MODEL (DEFAULT PARAMETERS)\n")
    f.write("Accuracy: " + str(baseline_accuracy) + "\n")
    f.write("Precision: " + str(baseline_precision) + "\n")
    f.write("Recall: " + str(baseline_recall) + "\n")
    f.write("F1 Score: " + str(baseline_f1) + "\n")
    f.write("Training Time (seconds): " + str(baseline_time) + "\n")
    f.write("n_estimators: " + str(baseline_model.n_estimators) + "\n")
    f.write("max_depth: " + str(baseline_model.max_depth) + "\n")
    f.write("min_samples_split: " + str(baseline_model.min_samples_split) + "\n")
    f.write("min_samples_leaf: " + str(baseline_model.min_samples_leaf) + "\n")

cm = confusion_matrix(y_test, y_pred_baseline)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix - Baseline Model")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("results/confusion_matrix_baseline.png")
plt.close()
