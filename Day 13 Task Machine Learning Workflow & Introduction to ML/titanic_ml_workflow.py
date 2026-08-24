from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


DATA_PATHS = [
    Path("data/train.csv"),
    Path("data/titanic.csv"),
    Path("train.csv"),
    Path("titanic.csv"),
    Path("data/sample_titanic.csv"),
]


def find_dataset():
    for path in DATA_PATHS:
        if path.exists():
            return path
    raise FileNotFoundError(
        "No Titanic dataset was found. Place train.csv or titanic.csv in the project root or data/ folder."
    )


def prepare_features(df):
    target = "Survived"
    feature_cols = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]

    working = df[feature_cols + [target]].copy()
    working["Age"] = working["Age"].fillna(working["Age"].median())
    working["Fare"] = working["Fare"].fillna(working["Fare"].median())
    working["Embarked"] = working["Embarked"].fillna(working["Embarked"].mode()[0])

    working["Sex"] = working["Sex"].map({"male": 1, "female": 0})
    working["Embarked"] = working["Embarked"].map({"S": 0, "C": 1, "Q": 2})

    X = working[feature_cols]
    y = working[target]
    return X, y


def save_visuals(df, y_test, y_pred):
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    survival_by_sex = df.groupby("Sex")["Survived"].mean().sort_values()
    ax = survival_by_sex.plot(kind="bar", color=["#2f6fed", "#dd4b39"], title="Average survival rate by gender")
    ax.set_xlabel("Sex")
    ax.set_ylabel("Survival rate")
    plt.tight_layout()
    plt.savefig(out_dir / "survival_by_sex.png")
    plt.close()

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted label")
    plt.ylabel("Actual label")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, cm[i, j], ha="center", va="center", color="black")
    plt.xticks([0, 1], ["Not Survived", "Survived"])
    plt.yticks([0, 1], ["Not Survived", "Survived"])
    plt.tight_layout()
    plt.savefig(out_dir / "confusion_matrix.png")
    plt.close()


def main():
    dataset_path = find_dataset()
    df = pd.read_csv(dataset_path)

    print("Titanic dataset loaded successfully.")
    print(f"Dataset shape: {df.shape}")
    print("\nColumns and data types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print("\nFirst 5 rows:")
    print(df.head())

    target = "Survived"
    print(f"\nTarget variable identified: {target}")
    print("\nKey observations:")
    print(df[["Sex", "Pclass", "Age", "Fare", "Embarked", target]].describe(include="all"))

    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel accuracy: {accuracy:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=["Not Survived", "Survived"]))

    save_visuals(df, y_test, y_pred)

    print("\nSaved charts to outputs/survival_by_sex.png and outputs/confusion_matrix.png")
    print("\nMachine Learning concepts covered in this project:")
    print("- Supervised Learning: learning from labeled examples where the target is known.")
    print("- Unsupervised Learning: finding hidden patterns without labeled targets.")
    print("- Regression: predicting continuous numeric outcomes.")
    print("- Classification: predicting categorical labels such as survival (0/1).")
    print("- Features: predictor variables like Pclass, Sex, Age, Fare.")
    print("- Labels: target values such as Survived.")
    print("- Training Data: used to fit the model.")
    print("- Testing Data: used to evaluate model performance.")


if __name__ == "__main__":
    main()
