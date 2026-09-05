import pandas as pd

baseline = pd.read_csv("outputs/model_comparison_baseline.csv")
tuned = pd.read_csv("outputs/tuned_vs_untuned_comparison.csv")

print("Baseline Model Comparison:")
print(baseline)

print("\nTuned vs Untuned Random Forest:")
print(tuned)

all_models = baseline[["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]].copy()
tuned_only = tuned[tuned["Model"] == "Random Forest (Tuned)"][["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]]
all_models = pd.concat([all_models, tuned_only], ignore_index=True)

all_models = all_models.sort_values(by="F1 Score", ascending=False)
print("\nAll Models Ranked by F1 Score:")
print(all_models)

best_model = all_models.iloc[0]
print("\nBest performing model is:", best_model["Model"])
print("With F1 Score of:", best_model["F1 Score"], "and ROC-AUC of:", best_model["ROC-AUC"])

all_models.to_csv("outputs/final_model_ranking.csv", index=False)
