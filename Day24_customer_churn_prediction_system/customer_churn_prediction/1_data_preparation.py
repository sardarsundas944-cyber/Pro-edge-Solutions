import pandas as pd
import numpy as np

df = pd.read_csv("data/churn_data.csv")

print("Shape of dataset:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nMissing values before cleaning:")
print(df.isnull().sum())

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
print("\nMissing values in TotalCharges after converting to numeric:", df["TotalCharges"].isnull().sum())

df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

df = df.drop_duplicates()

df = df.drop("customerID", axis=1)

print("\nMissing values after cleaning:")
print(df.isnull().sum().sum())

print("\nChurn value counts:")
print(df["Churn"].value_counts())
print(df["Churn"].value_counts(normalize=True))

df.to_csv("outputs/cleaned_data.csv", index=False)
print("\nCleaned data saved to outputs/cleaned_data.csv")
