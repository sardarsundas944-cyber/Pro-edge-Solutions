import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv("dataset/customer_churn.csv")

df["signup_date"] = pd.to_datetime(df["signup_date"])
df["signup_year"] = df["signup_date"].dt.year
df = df.drop(columns=["signup_date"])

df["monthly_charges"] = df["monthly_charges"].fillna(df["monthly_charges"].median())
df["total_charges"] = df["total_charges"].fillna(df["total_charges"].median())

df["charge_per_tenure"] = df["total_charges"] / (df["tenure_months"] + 1)
df["high_support_calls"] = (df["support_calls"] > 5).astype(int)
df["is_long_term"] = (df["tenure_months"] > 24).astype(int)
df["log_total_charges"] = np.log1p(df["total_charges"])

df = df.drop(columns=["total_charges"])

df = pd.get_dummies(df, columns=["gender", "city", "contract_type"], drop_first=True)

X = df.drop(columns=["churn"])
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

selector = SelectKBest(score_func=f_classif, k=10)
X_train_selected = selector.fit_transform(X_train_scaled, y_train)
X_test_selected = selector.transform(X_test_scaled)

selected_columns = X.columns[selector.get_support()]

model = LogisticRegression(max_iter=1000)
model.fit(X_train_selected, y_train)

y_pred = model.predict(X_test_selected)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Day 20 Improved Model Results")
print("All features before selection:", list(X.columns))
print("Selected features:", list(selected_columns))
print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))

with open("improved_results.txt", "w") as f:
    f.write("Day 20 Improved Model Results\n")
    f.write("All features before selection: " + str(list(X.columns)) + "\n")
    f.write("Selected features: " + str(list(selected_columns)) + "\n")
    f.write("Accuracy: " + str(round(accuracy, 4)) + "\n")
    f.write("Precision: " + str(round(precision, 4)) + "\n")
    f.write("Recall: " + str(round(recall, 4)) + "\n")
    f.write("F1 Score: " + str(round(f1, 4)) + "\n")
