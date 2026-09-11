# House Price ML Project - Testing & Logging

This project is a simple Machine Learning application that predicts house prices.
It has been enhanced with Unit Testing (pytest) and Structured Logging (Python logging module) to make it more reliable and easier to maintain.

## Project Structure

```
ml_project/
  data/
    house_data.csv
  logs/
    app.log
  models/
    house_price_model.pkl
  screenshots/
    pytest_run.png
    log_file_output.png
    main_run_output.png
  tests/
    test_data_preprocessing.py
    test_feature_engineering.py
    test_model_loading.py
    test_prediction.py
  data_preprocessing.py
  feature_engineering.py
  model.py
  predict.py
  logger_config.py
  main.py
  requirements.txt
  pytest.ini
  README.md
```

## What This Project Does

The project loads house data (size, bedrooms, age, price), cleans it, creates a new feature, trains a Linear Regression model, saves the model, loads it back, and makes predictions.

## How To Run The Project

1. Install the required packages:
```
pip install -r requirements.txt
```

2. Run the main pipeline:
```
python main.py
```

3. Run the unit tests:
```
pytest -v
```

## Unit Testing

Unit tests were written using **pytest** and are located in the `tests/` folder.

Tests were created for:
1. **Data preprocessing functions** (`test_data_preprocessing.py`) - loading data, cleaning data, splitting data
2. **Feature engineering functions** (`test_feature_engineering.py`) - creating new features, scaling features
3. **Prediction functions** (`test_prediction.py`) - generating predictions from a model
4. **Model loading functions** (`test_model_loading.py`) - training, saving, and loading a model

### Test Validation Covered
- Verifying expected outputs (correct shapes, correct columns, correct number of predictions)
- Testing different input scenarios (valid data, missing columns, empty input)
- Handling invalid inputs (missing files, `None` values, wrong column names) using `pytest.raises`
- Making sure critical functions like `load_model`, `make_prediction`, and `train_model` behave correctly

Running `pytest -v` from the project folder gives:

```
collected 20 items
20 passed
```

See `screenshots/pytest_run.png` for the test run output.

## Logging System

Logging was implemented using Python's built-in `logging` module. The setup is in `logger_config.py` and is used across all modules.

Logging covers:
1. **Application Startup** - logged in `main.py` when the pipeline starts
2. **Data Loading** - logged in `data_preprocessing.py`
3. **Model Training** - logged in `model.py`
4. **Prediction Generation** - logged in `predict.py`
5. **Error Handling** - logged whenever invalid input or a missing file is detected

### Log Levels Used
- **INFO** - normal operations, such as data loaded successfully or model trained successfully
- **WARNING** - unexpected situations, such as missing values being removed or an empty dataset
- **ERROR** - failures, such as a missing file, a missing column, or invalid input like `None`

All logs are saved to `logs/app.log`. See `screenshots/log_file_output.png` for an example of the generated log file, and `screenshots/main_run_output.png` for the console output when running `main.py`.

## Screenshots

The `screenshots/` folder contains:
- `pytest_run.png` - result of running the unit tests
- `log_file_output.png` - contents of the generated `logs/app.log` file
- `main_run_output.png` - console output when running the full pipeline with `main.py`

## Notes

- The trained model is saved to `models/house_price_model.pkl`.
- The `logs/app.log` file is created automatically the first time the project is run, so it does not need to be created manually.
- All functions were written with error handling so that invalid inputs are logged and raised properly instead of crashing silently.
