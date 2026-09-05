import pandas as pd
from sklearn.preprocessing import StandardScaler

def prepare_data(df):
    data = df.copy()
    data["Churn"] = data["Churn"].map({"Yes": 1, "No": 0})
    y = data["Churn"]
    X = data.drop("Churn", axis=1)
    X = pd.get_dummies(X, drop_first=True)

    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges", "AvgMonthlySpend",
                     "TotalServices", "SeniorCitizen"]
    numeric_cols = [c for c in numeric_cols if c in X.columns]

    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    return X, y
