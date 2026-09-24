from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

data = load_iris()
X = data.data
y = data.target

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model trained and saved as model.pkl")
