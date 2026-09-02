import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib

np.random.seed(42)

n_rows = 1000

area_sqft = np.random.randint(500, 4000, n_rows)
bedrooms = np.random.randint(1, 6, n_rows)
bathrooms = np.random.randint(1, 4, n_rows)
age_of_house = np.random.randint(0, 40, n_rows)
distance_to_city = np.random.uniform(1, 30, n_rows)

price = (
    area_sqft * 150
    + bedrooms * 20000
    + bathrooms * 15000
    - age_of_house * 800
    - distance_to_city * 1000
    + np.random.normal(0, 15000, n_rows)
)

data = pd.DataFrame({
    "area_sqft": area_sqft,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "age_of_house": age_of_house,
    "distance_to_city": distance_to_city,
    "price": price
})

data.to_csv("house_dataset.csv", index=False)

X = data.drop("price", axis=1)
y = data["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

joblib.dump(model, "house_model.pkl")
joblib.dump(scaler, "house_scaler.pkl")
X_test.to_csv("house_X_test.csv", index=False)
y_test.to_csv("house_y_test.csv", index=False)

print("Regression model trained and saved")
print("Train rows:", len(X_train))
print("Test rows:", len(X_test))
