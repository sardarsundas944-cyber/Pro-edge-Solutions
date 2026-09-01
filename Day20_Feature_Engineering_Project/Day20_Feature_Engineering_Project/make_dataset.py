import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000

age = np.random.randint(18, 70, n)
gender = np.random.choice(["Male", "Female"], n)
city = np.random.choice(["Karachi", "Lahore", "Islamabad", "Peshawar"], n)
monthly_charges = np.round(np.random.uniform(20, 150, n), 2)
tenure_months = np.random.randint(1, 72, n)
contract_type = np.random.choice(["Month-to-Month", "One Year", "Two Year"], n)
support_calls = np.random.randint(0, 10, n)
signup_date = pd.date_range("2018-01-01", "2023-01-01", periods=n)

total_charges = monthly_charges * tenure_months
total_charges = total_charges + np.random.normal(0, 50, n)

churn_score = (
    (contract_type == "Month-to-Month").astype(int) * 30
    + support_calls * 5
    - tenure_months * 0.5
    + (monthly_charges > 100).astype(int) * 10
    + np.random.normal(0, 15, n)
)

churn = (churn_score > 40).astype(int)

df = pd.DataFrame({
    "age": age,
    "gender": gender,
    "city": city,
    "monthly_charges": monthly_charges,
    "tenure_months": tenure_months,
    "contract_type": contract_type,
    "support_calls": support_calls,
    "signup_date": signup_date,
    "total_charges": total_charges,
    "churn": churn
})

missing_idx = np.random.choice(df.index, size=40, replace=False)
df.loc[missing_idx, "total_charges"] = np.nan

missing_idx2 = np.random.choice(df.index, size=25, replace=False)
df.loc[missing_idx2, "monthly_charges"] = np.nan

df.to_csv("dataset/customer_churn.csv", index=False)

print("Dataset created successfully")
print(df.shape)
print(df.head())
