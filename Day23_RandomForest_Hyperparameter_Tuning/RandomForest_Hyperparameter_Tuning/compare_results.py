import matplotlib.pyplot as plt

baseline_lines = open("results/baseline_results.txt").readlines()
tuning_lines = open("results/tuning_results.txt").readlines()

baseline_accuracy = float(baseline_lines[1].split(":")[1].strip())
baseline_precision = float(baseline_lines[2].split(":")[1].strip())
baseline_recall = float(baseline_lines[3].split(":")[1].strip())
baseline_f1 = float(baseline_lines[4].split(":")[1].strip())

optimized_accuracy = float(tuning_lines[6].split(":")[1].strip())
optimized_precision = float(tuning_lines[7].split(":")[1].strip())
optimized_recall = float(tuning_lines[8].split(":")[1].strip())
optimized_f1 = float(tuning_lines[9].split(":")[1].strip())

improvement = (optimized_accuracy - baseline_accuracy) * 100

print("PERFORMANCE COMPARISON")
print("Baseline Accuracy:", baseline_accuracy)
print("Optimized Accuracy:", optimized_accuracy)
print("Accuracy Improvement:", improvement, "%")

with open("results/comparison_results.txt", "w") as f:
    f.write("PERFORMANCE COMPARISON: BASELINE VS OPTIMIZED\n\n")
    f.write("Metric        Baseline      Optimized\n")
    f.write("Accuracy      " + str(round(baseline_accuracy, 4)) + "        " + str(round(optimized_accuracy, 4)) + "\n")
    f.write("Precision     " + str(round(baseline_precision, 4)) + "        " + str(round(optimized_precision, 4)) + "\n")
    f.write("Recall        " + str(round(baseline_recall, 4)) + "        " + str(round(optimized_recall, 4)) + "\n")
    f.write("F1 Score      " + str(round(baseline_f1, 4)) + "        " + str(round(optimized_f1, 4)) + "\n\n")
    f.write("Accuracy Improvement: " + str(round(improvement, 4)) + " %\n")

metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
baseline_values = [baseline_accuracy, baseline_precision, baseline_recall, baseline_f1]
optimized_values = [optimized_accuracy, optimized_precision, optimized_recall, optimized_f1]

x = range(len(metrics))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar([i - width/2 for i in x], baseline_values, width, label="Baseline")
plt.bar([i + width/2 for i in x], optimized_values, width, label="Optimized")
plt.xticks(list(x), metrics)
plt.ylim(0, 1.1)
plt.ylabel("Score")
plt.title("Baseline vs Optimized Random Forest Performance")
plt.legend()
plt.tight_layout()
plt.savefig("results/comparison_chart.png")
plt.close()
