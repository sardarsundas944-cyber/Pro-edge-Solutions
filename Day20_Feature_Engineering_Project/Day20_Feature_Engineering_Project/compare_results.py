baseline = {}
improved = {}

with open("baseline_results.txt") as f:
    for line in f:
        if ":" in line:
            key, value = line.strip().split(":", 1)
            baseline[key.strip()] = value.strip()

with open("improved_results.txt") as f:
    for line in f:
        if ":" in line:
            key, value = line.strip().split(":", 1)
            improved[key.strip()] = value.strip()

print("Performance Comparison")
print("Metric      | Baseline (Day 19) | Improved (Day 20)")
print("Accuracy    |", baseline["Accuracy"], "            |", improved["Accuracy"])
print("Precision   |", baseline["Precision"], "            |", improved["Precision"])
print("Recall      |", baseline["Recall"], "            |", improved["Recall"])
print("F1 Score    |", baseline["F1 Score"], "            |", improved["F1 Score"])

acc_gain = float(improved["Accuracy"]) - float(baseline["Accuracy"])
f1_gain = float(improved["F1 Score"]) - float(baseline["F1 Score"])

print("Accuracy improved by:", round(acc_gain, 4))
print("F1 Score improved by:", round(f1_gain, 4))
