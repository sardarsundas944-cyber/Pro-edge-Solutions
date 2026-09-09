import pandas as pd


def compare_experiments():
    df = pd.read_csv("experiments/experiment_log.csv")

    print("Full Experiment History:")
    print(df.to_string(index=False))

    best_row = df.loc[df["Accuracy"].idxmax()]
    print("")
    print("Best Performing Model So Far:")
    print("Model Name:", best_row["Model Name"])
    print("Model Version:", best_row["Model Version"])
    print("Accuracy:", best_row["Accuracy"])
    print("F1 Score:", best_row["F1 Score"])

    print("")
    print("Improvement from first run to latest run:")
    first_accuracy = df.iloc[0]["Accuracy"]
    last_accuracy = df.iloc[-1]["Accuracy"]
    improvement = last_accuracy - first_accuracy
    print("First Run Accuracy:", first_accuracy)
    print("Latest Run Accuracy:", last_accuracy)
    print("Accuracy Change:", round(improvement, 4))


if __name__ == "__main__":
    compare_experiments()
