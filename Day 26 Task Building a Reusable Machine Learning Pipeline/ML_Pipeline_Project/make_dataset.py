import numpy as np
import pandas as pd

np.random.seed(42)

n = 400

pclass = np.random.choice([1, 2, 3], size=n, p=[0.2, 0.3, 0.5])
sex = np.random.choice(["male", "female"], size=n, p=[0.55, 0.45])
age = np.random.normal(30, 12, size=n)
age = np.clip(age, 1, 75)
sibsp = np.random.choice([0, 1, 2, 3], size=n, p=[0.6, 0.25, 0.1, 0.05])
parch = np.random.choice([0, 1, 2], size=n, p=[0.7, 0.2, 0.1])
fare = np.random.exponential(30, size=n) + (4 - pclass) * 10
embarked = np.random.choice(["S", "C", "Q"], size=n, p=[0.6, 0.25, 0.15])

survive_prob = 0.5
survive_prob = survive_prob + (sex == "female") * 0.35
survive_prob = survive_prob - (pclass - 1) * 0.12
survive_prob = survive_prob + (age < 12) * 0.15
survive_prob = np.clip(survive_prob, 0.05, 0.95)
survived = np.random.binomial(1, survive_prob)

df = pd.DataFrame({
    "PassengerId": range(1, n + 1),
    "Pclass": pclass,
    "Sex": sex,
    "Age": age.round(1),
    "SibSp": sibsp,
    "Parch": parch,
    "Fare": fare.round(2),
    "Embarked": embarked,
    "Survived": survived
})

missing_age_idx = np.random.choice(df.index, size=40, replace=False)
df.loc[missing_age_idx, "Age"] = np.nan

missing_emb_idx = np.random.choice(df.index, size=10, replace=False)
df.loc[missing_emb_idx, "Embarked"] = np.nan

df.to_csv("data/titanic.csv", index=False)
print("dataset created")
print(df.shape)
print(df.isnull().sum())
