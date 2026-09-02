import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

np.random.seed(42)

n_rows = 1000

age = np.random.randint(18, 70, n_rows)
tenure_months = np.random.randint(1, 72, n_rows)
monthly_charges = np.random.uniform(20, 120, n_rows)
support_calls = np.random.randint(0, 10, n_rows)
contract_type = np.random.randint(0, 3, n_rows)

churn_score = (
    (tenure_months < 12).astype(int) * 2
    + (monthly_charges > 80).astype(int) * 2
    + (support_calls > 4).astype(int) * 2
    + (contract_type == 0).astype(int) * 2
    - (age > 50).astype(int)
)

churn_prob = 1 / (1 + np.exp(-(churn_score - 3)))
churn = np.random.binomial(1, churn_prob)

data = pd.DataFrame({
    "age": age,
    "tenure_months": tenure_months,
    "monthly_charges": monthly_charges,
    "support_calls": support_calls,
    "contract_type": contract_type,
    "churn": churn
})

data.to_csv("churn_dataset.csv", index=False)

X = data.drop("churn", axis=1)
y = data["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

joblib.dump(model, "churn_model.pkl")
joblib.dump(scaler, "churn_scaler.pkl")
X_test.to_csv("churn_X_test.csv", index=False)
y_test.to_csv("churn_y_test.csv", index=False)

print("Classification model trained and saved")
print("Train rows:", len(X_train))
print("Test rows:", len(X_test))
