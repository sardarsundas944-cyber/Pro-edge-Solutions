import pandas as pd
import numpy as np

df = pd.read_csv("outputs/cleaned_data.csv")

df_basic = df.copy()
df_basic.to_csv("outputs/data_basic.csv", index=False)

df_fe = df.copy()

def tenure_group(t):
    if t <= 12:
        return "0-1yr"
    elif t <= 24:
        return "1-2yr"
    elif t <= 48:
        return "2-4yr"
    else:
        return "4yr+"

df_fe["TenureGroup"] = df_fe["tenure"].apply(tenure_group)

df_fe["AvgMonthlySpend"] = df_fe["TotalCharges"] / (df_fe["tenure"] + 1)

services = ["PhoneService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies"]

def count_services(row):
    count = 0
    for s in services:
        if row[s] == "Yes":
            count = count + 1
    return count

df_fe["TotalServices"] = df_fe.apply(count_services, axis=1)

df_fe["IsNewCustomer"] = np.where(df_fe["tenure"] <= 6, 1, 0)

df_fe["HighMonthlyCharge"] = np.where(df_fe["MonthlyCharges"] > df_fe["MonthlyCharges"].median(), 1, 0)

df_fe.to_csv("outputs/data_engineered.csv", index=False)

print("Basic data shape:", df_basic.shape)
print("Engineered data shape:", df_fe.shape)
print("\nNew features added:")
print(["TenureGroup", "AvgMonthlySpend", "TotalServices", "IsNewCustomer", "HighMonthlyCharge"])
print("\nSample of engineered features:")
print(df_fe[["tenure", "TenureGroup", "AvgMonthlySpend", "TotalServices", "IsNewCustomer", "HighMonthlyCharge"]].head())
