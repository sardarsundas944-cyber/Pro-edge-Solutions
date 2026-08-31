import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv("data/breast_cancer_dataset.csv")

print("First 5 rows of data:")
print(df.head())

print("\nShape of data:")
print(df.shape)

print("\nMissing values in each column:")
print(df.isnull().sum().sum())

df = df.dropna()

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {}

log_model = LogisticRegression(max_iter=5000)
log_model.fit(X_train_scaled, y_train)
models["Logistic Regression"] = log_model

tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train, y_train)
models["Decision Tree"] = tree_model

forest_model = RandomForestClassifier(n_estimators=100, random_state=42)
forest_model.fit(X_train, y_train)
models["Random Forest"] = forest_model

results = []

for name, model in models.items():
    if name == "Logistic Regression":
        y_pred = model.predict(X_test_scaled)
    else:
        y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })

results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="Accuracy", ascending=False)

print("\nModel Comparison Results:")
print(results_df)

results_df.to_csv("results/model_comparison_results.csv", index=False)

best_model_name = results_df.iloc[0]["Model"]
print("\nBest performing model is:", best_model_name)

importances = forest_model.feature_importances_
feature_names = X.columns

feature_importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})

feature_importance_df = feature_importance_df.sort_values(by="Importance", ascending=False)

print("\nTop 10 Important Features from Random Forest:")
print(feature_importance_df.head(10))

feature_importance_df.to_csv("results/feature_importance.csv", index=False)

top_features = feature_importance_df.head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_features["Feature"], top_features["Importance"], color="skyblue")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.title("Top 10 Feature Importances - Random Forest")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("plots/feature_importance.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(results_df["Model"], results_df["Accuracy"], color="lightgreen")
plt.xlabel("Model")
plt.ylabel("Accuracy")
plt.title("Model Accuracy Comparison")
plt.tight_layout()
plt.savefig("plots/model_accuracy_comparison.png")
plt.close()

print("\nAll plots and results have been saved successfully.")
