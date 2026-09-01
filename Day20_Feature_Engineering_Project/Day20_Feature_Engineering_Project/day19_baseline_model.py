import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv("dataset/customer_churn.csv")

df = df.drop(columns=["signup_date"])

df["monthly_charges"] = df["monthly_charges"].fillna(df["monthly_charges"].mean())
df["total_charges"] = df["total_charges"].fillna(df["total_charges"].mean())

le = LabelEncoder()
df["gender"] = le.fit_transform(df["gender"])
df["city"] = le.fit_transform(df["city"])
df["contract_type"] = le.fit_transform(df["contract_type"])

X = df.drop(columns=["churn"])
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Day 19 Baseline Model Results")
print("Features used:", list(X.columns))
print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))

with open("baseline_results.txt", "w") as f:
    f.write("Day 19 Baseline Model Results\n")
    f.write("Features used: " + str(list(X.columns)) + "\n")
    f.write("Accuracy: " + str(round(accuracy, 4)) + "\n")
    f.write("Precision: " + str(round(precision, 4)) + "\n")
    f.write("Recall: " + str(round(recall, 4)) + "\n")
    f.write("F1 Score: " + str(round(f1, 4)) + "\n")
