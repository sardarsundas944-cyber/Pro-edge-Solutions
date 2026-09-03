import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

print("Dataset Shape:", X.shape)
print(X.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt_model = DecisionTreeClassifier(random_state=42)
rf_model = RandomForestClassifier(random_state=42)

dt_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

dt_train_test_pred = dt_model.predict(X_test)
rf_train_test_pred = rf_model.predict(X_test)

dt_train_test_acc = accuracy_score(y_test, dt_train_test_pred)
rf_train_test_acc = accuracy_score(y_test, rf_train_test_pred)

print("\nSingle Train-Test Split Results")
print("Decision Tree Accuracy:", dt_train_test_acc)
print("Random Forest Accuracy:", rf_train_test_acc)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

dt_cv_scores = cross_val_score(dt_model, X, y, cv=kf)
rf_cv_scores = cross_val_score(rf_model, X, y, cv=kf)

print("\nDecision Tree Cross-Validation Scores")
print(dt_cv_scores)
print("Decision Tree Average Score:", dt_cv_scores.mean())
print("Decision Tree Std Deviation:", dt_cv_scores.std())

print("\nRandom Forest Cross-Validation Scores")
print(rf_cv_scores)
print("Random Forest Average Score:", rf_cv_scores.mean())
print("Random Forest Std Deviation:", rf_cv_scores.std())

results_df = pd.DataFrame({
    "Fold": [1, 2, 3, 4, 5],
    "Decision_Tree_Score": dt_cv_scores,
    "Random_Forest_Score": rf_cv_scores
})

print("\nCross Validation Results Table")
print(results_df)

results_df.to_csv("results/cv_results.csv", index=False)

summary_df = pd.DataFrame({
    "Model": ["Decision Tree", "Random Forest"],
    "TrainTestSplit_Accuracy": [dt_train_test_acc, rf_train_test_acc],
    "CV_Average_Score": [dt_cv_scores.mean(), rf_cv_scores.mean()],
    "CV_Std_Deviation": [dt_cv_scores.std(), rf_cv_scores.std()]
})

print("\nModel Comparison Summary")
print(summary_df)

summary_df.to_csv("results/summary_results.csv", index=False)

plt.figure(figsize=(8, 5))
folds = [1, 2, 3, 4, 5]
plt.plot(folds, dt_cv_scores, marker="o", label="Decision Tree")
plt.plot(folds, rf_cv_scores, marker="o", label="Random Forest")
plt.title("Cross Validation Scores Across Folds")
plt.xlabel("Fold Number")
plt.ylabel("Accuracy Score")
plt.legend()
plt.grid(True)
plt.savefig("screenshots/fold_scores_comparison.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.boxplot([dt_cv_scores, rf_cv_scores], labels=["Decision Tree", "Random Forest"])
plt.title("Model Stability Comparison (Boxplot)")
plt.ylabel("Accuracy Score")
plt.savefig("screenshots/model_stability_boxplot.png")
plt.close()

plt.figure(figsize=(8, 5))
bar_labels = ["DT Train-Test", "DT CV Average", "RF Train-Test", "RF CV Average"]
bar_values = [dt_train_test_acc, dt_cv_scores.mean(), rf_train_test_acc, rf_cv_scores.mean()]
plt.bar(bar_labels, bar_values, color=["skyblue", "blue", "lightgreen", "green"])
plt.title("Train-Test Split vs Cross Validation Average")
plt.ylabel("Accuracy Score")
plt.ylim(0.8, 1.0)
plt.savefig("screenshots/traintest_vs_cv_comparison.png")
plt.close()

if dt_cv_scores.std() < rf_cv_scores.std():
    stable_model = "Decision Tree"
else:
    stable_model = "Random Forest"

if dt_cv_scores.mean() > rf_cv_scores.mean():
    better_model = "Decision Tree"
else:
    better_model = "Random Forest"

print("\nFinal Observation")
print("Most Stable Model based on lowest std deviation:", stable_model)
print("Best Performing Model based on average CV score:", better_model)
