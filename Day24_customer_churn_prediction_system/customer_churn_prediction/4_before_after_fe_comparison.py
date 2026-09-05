import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from preprocess_helper import prepare_data

df_basic = pd.read_csv("outputs/data_basic.csv")
df_fe = pd.read_csv("outputs/data_engineered.csv")

results = []

for name, data in [("Before Feature Engineering", df_basic), ("After Feature Engineering", df_fe)]:
    X, y = prepare_data(data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    lr = LogisticRegression(max_iter=1000, class_weight="balanced")
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    rf = RandomForestClassifier(random_state=42, class_weight="balanced")
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    results.append({
        "Stage": name,
        "Model": "Logistic Regression",
        "Accuracy": round(accuracy_score(y_test, lr_pred), 4),
        "F1 Score": round(f1_score(y_test, lr_pred), 4)
    })
    results.append({
        "Stage": name,
        "Model": "Random Forest",
        "Accuracy": round(accuracy_score(y_test, rf_pred), 4),
        "F1 Score": round(f1_score(y_test, rf_pred), 4)
    })

result_df = pd.DataFrame(results)
print(result_df)
result_df.to_csv("outputs/before_after_fe_comparison.csv", index=False)
print("\nComparison saved to outputs/before_after_fe_comparison.csv")
