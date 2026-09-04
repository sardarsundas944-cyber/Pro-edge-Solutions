import subprocess

print("STEP 1: Running Baseline Model")
subprocess.run(["python3", "baseline_model.py"])

print("STEP 2: Running Hyperparameter Tuning")
subprocess.run(["python3", "hyperparameter_tuning.py"])

print("STEP 3: Comparing Results")
subprocess.run(["python3", "compare_results.py"])

print("ALL STEPS COMPLETED. CHECK THE results FOLDER.")
