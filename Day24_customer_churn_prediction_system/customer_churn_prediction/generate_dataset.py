import numpy as np
import pandas as pd

np.random.seed(42)

n = 2000

customer_id = ["CUST" + str(1000 + i) for i in range(n)]
gender = np.random.choice(["Male", "Female"], n)
senior_citizen = np.random.choice([0, 1], n, p=[0.84, 0.16])
partner = np.random.choice(["Yes", "No"], n, p=[0.48, 0.52])
dependents = np.random.choice(["Yes", "No"], n, p=[0.3, 0.7])
tenure = np.random.randint(0, 73, n)
phone_service = np.random.choice(["Yes", "No"], n, p=[0.9, 0.1])
multiple_lines = np.random.choice(["Yes", "No", "No phone service"], n, p=[0.42, 0.48, 0.1])
internet_service = np.random.choice(["DSL", "Fiber optic", "No"], n, p=[0.34, 0.44, 0.22])
online_security = np.random.choice(["Yes", "No", "No internet service"], n, p=[0.29, 0.49, 0.22])
online_backup = np.random.choice(["Yes", "No", "No internet service"], n, p=[0.34, 0.44, 0.22])
device_protection = np.random.choice(["Yes", "No", "No internet service"], n, p=[0.34, 0.44, 0.22])
tech_support = np.random.choice(["Yes", "No", "No internet service"], n, p=[0.29, 0.49, 0.22])
streaming_tv = np.random.choice(["Yes", "No", "No internet service"], n, p=[0.38, 0.4, 0.22])
streaming_movies = np.random.choice(["Yes", "No", "No internet service"], n, p=[0.38, 0.4, 0.22])
contract = np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.24, 0.21])
paperless_billing = np.random.choice(["Yes", "No"], n, p=[0.59, 0.41])
payment_method = np.random.choice(
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
    n, p=[0.34, 0.23, 0.22, 0.21]
)
monthly_charges = np.round(np.random.uniform(18, 120, n), 2)

total_charges = monthly_charges * tenure + np.random.normal(0, 50, n)
total_charges = np.round(np.clip(total_charges, 0, None), 2)

missing_idx = np.random.choice(n, 15, replace=False)
total_charges = total_charges.astype(object)
for i in missing_idx:
    total_charges[i] = " "

churn_score = np.zeros(n)
churn_score += (contract == "Month-to-month") * 2.2
churn_score += (contract == "One year") * 0.5
churn_score += (internet_service == "Fiber optic") * 1.0
churn_score += (payment_method == "Electronic check") * 0.9
churn_score += (tech_support == "No") * 0.6
churn_score += (online_security == "No") * 0.6
churn_score += (senior_citizen == 1) * 0.5
churn_score += (partner == "No") * 0.3
churn_score += (paperless_billing == "Yes") * 0.4
churn_score += (monthly_charges - 60) / 40
churn_score += (12 - np.clip(tenure, 0, 12)) / 12
churn_score += np.random.normal(0, 1.0, n)

churn_prob = 1 / (1 + np.exp(-(churn_score - 4.2)))
churn = np.where(np.random.rand(n) < churn_prob, "Yes", "No")

df = pd.DataFrame({
    "customerID": customer_id,
    "gender": gender,
    "SeniorCitizen": senior_citizen,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "Churn": churn
})

df.to_csv("data/churn_data.csv", index=False)
print("Dataset created with shape:", df.shape)
print(df["Churn"].value_counts())
