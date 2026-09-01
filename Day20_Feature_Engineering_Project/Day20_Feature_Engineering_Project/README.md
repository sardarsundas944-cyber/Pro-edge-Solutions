# Day 20 Task: Feature Engineering for Model Improvement

## Objective
Learn how Feature Engineering can improve Machine Learning model performance by creating, transforming, and selecting useful features. Compare model performance before and after feature engineering.

## Note on Dataset
This project reuses the same **Customer Churn dataset** and baseline model created on Day 19. The dataset generator script (`make_dataset.py`) is included so the exact same dataset can be reproduced. The dataset is a telecom style customer churn dataset with 1000 rows and includes both numeric and categorical columns, along with some missing values, so that feature engineering techniques can be applied in a meaningful way.

## Project Structure
```
Day20_Feature_Engineering_Project/
│
├── dataset/
│   └── customer_churn.csv          # dataset used since Day 19
│
├── screenshots/
│   ├── 01_baseline_model_output.png
│   ├── 02_improved_model_output.png
│   ├── 03_performance_comparison.png
│   └── 04_performance_chart.png
│
├── make_dataset.py                 # generates the dataset
├── day19_baseline_model.py         # Day 19 baseline model
├── day20_feature_engineering.py    # Day 20 feature engineered model
├── compare_results.py              # prints before vs after comparison
├── baseline_results.txt            # saved baseline metrics
├── improved_results.txt            # saved improved metrics
├── requirements.txt
└── README.md
```

## Dataset Columns
- age
- gender
- city
- monthly_charges
- tenure_months
- contract_type
- support_calls
- signup_date
- total_charges
- churn (target column)

## Step 1: Baseline Model (Day 19)
File: `day19_baseline_model.py`

What it does:
- Loads the dataset
- Drops the signup_date column
- Fills missing values in monthly_charges and total_charges with the mean
- Converts gender, city and contract_type to numbers using Label Encoding
- Trains a Logistic Regression model
- Evaluates the model on the test set

### Baseline Results
| Metric | Score |
|--------|-------|
| Accuracy | 0.855 |
| Precision | 0.7778 |
| Recall | 0.5714 |
| F1 Score | 0.6588 |

Screenshot: `screenshots/01_baseline_model_output.png`

## Step 2: Feature Engineering (Day 20)
File: `day20_feature_engineering.py`

Techniques applied:
1. **New features created**
   - `charge_per_tenure` = total_charges divided by tenure_months
   - `high_support_calls` = 1 if support_calls is more than 5, else 0
   - `is_long_term` = 1 if tenure_months is more than 24, else 0
   - `signup_year` extracted from the signup_date column
2. **Feature transformation**
   - Applied `log1p` transformation on total_charges to reduce skewness (`log_total_charges`)
   - Scaled all numeric features using `StandardScaler`
3. **Better handling of categorical variables**
   - Used One-Hot Encoding (`pd.get_dummies`) for gender, city and contract_type instead of Label Encoding, since these columns are not ordinal
4. **Feature selection**
   - Used `SelectKBest` with the ANOVA F-test (`f_classif`) to keep the 10 most useful features and remove the rest
5. **Missing value handling**
   - Used median instead of mean to fill missing values, since median is less affected by outliers

### Selected Features After Feature Selection
age, monthly_charges, tenure_months, support_calls, charge_per_tenure, high_support_calls, is_long_term, log_total_charges, contract_type_One Year, contract_type_Two Year

### Improved Model Results
| Metric | Score |
|--------|-------|
| Accuracy | 0.865 |
| Precision | 0.8438 |
| Recall | 0.551 |
| F1 Score | 0.6667 |

Screenshot: `screenshots/02_improved_model_output.png`

## Step 3: Performance Comparison
File: `compare_results.py`

| Metric | Baseline (Day 19) | Improved (Day 20) | Change |
|--------|--------------------|--------------------|--------|
| Accuracy | 0.855 | 0.865 | +0.01 |
| Precision | 0.7778 | 0.8438 | +0.066 |
| Recall | 0.5714 | 0.551 | -0.0204 |
| F1 Score | 0.6588 | 0.6667 | +0.0079 |

Screenshot: `screenshots/03_performance_comparison.png`
Chart: `screenshots/04_performance_chart.png`

## What Improved and Why
- **Accuracy and Precision went up** mainly because of the new features `charge_per_tenure`, `high_support_calls` and `is_long_term`. These features give the model a clearer signal about churn behavior instead of raw numbers alone.
- **One-Hot Encoding** for contract_type helped the model since contract type has no natural order, and Label Encoding was wrongly treating it like ranked numbers.
- **Log transformation** on total_charges reduced the effect of extreme values and made the feature more normally distributed.
- **Feature scaling** helped Logistic Regression converge better and treat all features fairly.
- **Recall dropped slightly**, which shows that feature engineering can trade off between precision and recall. In this project we selected features that made the model more confident and precise, but slightly more conservative in predicting churn.
- Overall, the **F1 Score improved from 0.6588 to 0.6667** and **Accuracy improved from 0.855 to 0.865**, showing that feature engineering had a positive impact on the model.

## How to Run
```
pip install -r requirements.txt
python3 make_dataset.py
python3 day19_baseline_model.py
python3 day20_feature_engineering.py
python3 compare_results.py
```

## Tools Used
- Pandas and NumPy for data handling and feature engineering
- Scikit-Learn for model training, scaling, encoding and evaluation
- Matplotlib for the comparison chart
