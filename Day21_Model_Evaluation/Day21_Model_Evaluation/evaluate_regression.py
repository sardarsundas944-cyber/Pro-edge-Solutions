import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

model = joblib.load("house_model.pkl")
scaler = joblib.load("house_scaler.pkl")

X_test = pd.read_csv("house_X_test.csv")
y_test = pd.read_csv("house_y_test.csv")["price"]

X_test_scaled = scaler.transform(X_test)

y_pred = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Regression Model Evaluation")
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r2)

results = {
    "MAE": mae,
    "MSE": mse,
    "RMSE": rmse,
    "R2 Score": r2
}

results_df = pd.DataFrame(list(results.items()), columns=["Metric", "Score"])
results_df.to_csv("regression_results.csv", index=False)

plt.figure(figsize=(6, 5))
plt.scatter(y_test, y_pred, alpha=0.5, color="green")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", linestyle="--")
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted House Price")
plt.tight_layout()
plt.savefig("screenshots/actual_vs_predicted.png")
plt.close()

residuals = y_test - y_pred

plt.figure(figsize=(6, 5))
plt.scatter(y_pred, residuals, alpha=0.5, color="purple")
plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("Predicted Price")
plt.ylabel("Residuals")
plt.title("Residual Plot - House Price Prediction")
plt.tight_layout()
plt.savefig("screenshots/residual_plot.png")
plt.close()

plt.figure(figsize=(6, 5))
plt.bar(["MAE", "RMSE"], [mae, rmse], color="orange")
plt.title("Regression Error Metrics Comparison")
plt.ylabel("Error Value")
plt.tight_layout()
plt.savefig("screenshots/regression_metrics_bar.png")
plt.close()

print("Evaluation finished and screenshots saved")
