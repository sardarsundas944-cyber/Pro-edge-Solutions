# Day 23 Task: Hyperparameter Tuning with Random Forest

## Objective
Learn how Hyperparameter Tuning can improve Machine Learning model performance and understand the importance of selecting optimal model settings. This project uses GridSearchCV to optimize a Random Forest model and compares it with a default (baseline) Random Forest model.

## Dataset
This project uses the **Breast Cancer Wisconsin Dataset** (`dataset.csv`), a binary classification dataset with 569 rows and 30 numeric features. The target column (`target`) shows whether a tumor is malignant (0) or benign (1).

## Project Structure
```
RandomForest_Hyperparameter_Tuning/
│
├── dataset.csv                     Dataset used for training and testing
├── data_setup.py                   Loads and splits the dataset
├── baseline_model.py                Trains and evaluates the default Random Forest model
├── hyperparameter_tuning.py         Runs GridSearchCV and evaluates the optimized model
├── compare_results.py               Compares baseline vs optimized model performance
├── main.py                          Runs all steps in order
├── requirements.txt                 Python libraries needed
├── README.md                        This file
│
├── results/
│   ├── baseline_results.txt
│   ├── tuning_results.txt
│   ├── best_params.json
│   ├── comparison_results.txt
│   ├── confusion_matrix_baseline.png
│   ├── confusion_matrix_optimized.png
│   └── comparison_chart.png
│
└── screenshots/
    ├── 1_baseline_model_output.png
    ├── 2_hyperparameter_tuning_output.png
    ├── 3_comparison_output.png
    ├── 4_confusion_matrix_baseline.png
    ├── 5_confusion_matrix_optimized.png
    └── 6_comparison_chart.png
```

## How to Run
```
pip install -r requirements.txt
python3 main.py
```
This will run the baseline model, the hyperparameter tuning step, and the comparison step, one after another, and save all results into the `results/` folder.

You can also run each step separately:
```
python3 baseline_model.py
python3 hyperparameter_tuning.py
python3 compare_results.py
```

## Step 1: Baseline Model (Default Parameters)
A Random Forest model was trained using Scikit-Learn's default parameters (`n_estimators=100`, `max_depth=None`, `min_samples_split=2`, `min_samples_leaf=1`).

**Baseline Results:**
| Metric | Score |
|---|---|
| Accuracy | 0.9649 |
| Precision | 0.9589 |
| Recall | 0.9859 |
| F1 Score | 0.9722 |
| Training Time | 0.15 sec |

Screenshot: `screenshots/1_baseline_model_output.png`

## Step 2: Hyperparameter Tuning (GridSearchCV)
GridSearchCV was used with 5-fold cross validation to search over the following parameter grid:

| Parameter | Values Tried |
|---|---|
| n_estimators | 50, 100, 200 |
| max_depth | None, 5, 10, 20 |
| min_samples_split | 2, 5, 10 |
| min_samples_leaf | 1, 2, 4 |

This produced 108 parameter combinations, and with 5-fold cross validation, a total of 540 model fits were run.

**Best Parameters Found:**
```
{
    "max_depth": null,
    "min_samples_leaf": 1,
    "min_samples_split": 2,
    "n_estimators": 200
}
```

**Best Cross Validation Accuracy:** 0.9626
**Tuning Time:** 87.84 sec

Screenshot: `screenshots/2_hyperparameter_tuning_output.png`

## Step 3: Optimized Model Results
The optimized Random Forest model was trained using the best parameters found above.

**Optimized Results:**
| Metric | Score |
|---|---|
| Accuracy | 0.9649 |
| Precision | 0.9589 |
| Recall | 0.9859 |
| F1 Score | 0.9722 |

## Performance Comparison

| Metric | Baseline | Optimized | Change |
|---|---|---|---|
| Accuracy | 0.9649 | 0.9649 | 0.0% |
| Precision | 0.9589 | 0.9589 | 0.0% |
| Recall | 0.9859 | 0.9859 | 0.0% |
| F1 Score | 0.9722 | 0.9722 | 0.0% |

Screenshot: `screenshots/3_comparison_output.png`
Chart: `screenshots/6_comparison_chart.png`

Confusion Matrices:
- `screenshots/4_confusion_matrix_baseline.png`
- `screenshots/5_confusion_matrix_optimized.png`

## Results Analysis

**Did tuning improve results?**
On this dataset, GridSearchCV found that the best number of trees was `n_estimators=200` instead of the default `100`, but `max_depth`, `min_samples_split`, and `min_samples_leaf` all matched the default values. Because of this, the optimized model ended up almost identical to the baseline model, and the test set accuracy stayed the same at 96.49%.

**Why did this happen?**
The Breast Cancer dataset is small (569 rows) and fairly clean, with well-separated classes. Random Forest with default settings already performs close to its maximum possible accuracy on this data, so there is very little room left for hyperparameter tuning to improve it further. This is a normal and expected outcome — tuning does not always increase performance, especially on datasets that are already easy for the model to learn.

**How did the parameters affect the model?**
- `n_estimators` (number of trees): Increasing this from 100 to 200 makes the model average over more trees, usually giving slightly more stable predictions, but with diminishing returns once accuracy is already near its ceiling.
- `max_depth` (maximum tree depth): Keeping this at `None` allows trees to grow until every leaf is pure, which works well here because the dataset is not very noisy.
- `min_samples_split` and `min_samples_leaf`: Keeping these at their smallest default values (2 and 1) allows the trees to split more freely, which fits this dataset well.

**Conclusion:**
Hyperparameter tuning is still an important step because it confirms whether the default settings are already close to optimal, or whether better settings exist. In this project, the search confirmed the default Random Forest settings were already close to optimal for this dataset, while also showing exactly how each parameter affects the model. On larger, noisier, or more complex datasets, hyperparameter tuning is expected to make a much bigger difference than it did here.

## Technical Requirements Used
- Python 3
- pandas
- scikit-learn (RandomForestClassifier, GridSearchCV, train_test_split, evaluation metrics)
- matplotlib and seaborn (for charts and confusion matrices)

## Submission Checklist
- [x] Baseline Random Forest model trained and evaluated
- [x] Hyperparameter tuning performed using GridSearchCV
- [x] Best parameter values identified and documented
- [x] Performance comparison between default and optimized models completed
- [x] README.md updated with tuning results, observations, and screenshots
