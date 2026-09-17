from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

data = load_iris()
X = data.data
y = data.target

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "model/model.joblib")
joblib.dump(data.target_names.tolist(), "model/class_names.joblib")

print("Model trained and saved to model/model.joblib")
