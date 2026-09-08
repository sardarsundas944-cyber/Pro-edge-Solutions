import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("data/titanic.csv")

X = df.drop(["PassengerId", "Survived"], axis=1)
y = df["Survived"]

numerical_features = ["Pclass", "Age", "SibSp", "Parch", "Fare"]
categorical_features = ["Sex", "Embarked"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numerical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numerical_pipeline, numerical_features),
    ("cat", categorical_pipeline, categorical_features)
])

model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000))
])

model_pipeline.fit(X_train, y_train)

y_pred = model_pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("Pipeline Model Results")
print("Accuracy:", acc)
print(classification_report(y_test, y_pred))

joblib.dump(model_pipeline, "model/titanic_pipeline.joblib")
print("pipeline saved to model/titanic_pipeline.joblib")

new_passenger = pd.DataFrame([{
    "Pclass": 3,
    "Sex": "female",
    "Age": None,
    "SibSp": 1,
    "Parch": 0,
    "Fare": 15.5,
    "Embarked": "S"
}])

prediction = model_pipeline.predict(new_passenger)
print("Raw new passenger data")
print(new_passenger)
print("Prediction on raw data (1 = survived, 0 = not survived):", prediction[0])
