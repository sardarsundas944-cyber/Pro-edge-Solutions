# Iris ML Package

This is a simple machine learning project restructured into a proper, installable Python
package with a command-line interface. The project trains a Random Forest model on the
classic Iris dataset and can then use that model to make predictions.

## Project Structure

```
iris_ml_project/
├── src/
│   └── irisml/
│       ├── __init__.py
│       ├── config.py
│       ├── preprocessing.py
│       ├── train.py
│       ├── predict.py
│       └── cli.py
├── data/
│   └── iris.csv
├── models/
│   └── (trained models are saved here)
├── configs/
│   └── config.yaml
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py
│   └── test_train.py
├── screenshots/
│   ├── install.png
│   ├── train.png
│   └── predict.png
├── pyproject.toml
└── README.md
```

### What each part does

- `src/irisml/preprocessing.py` loads the dataset and splits it into train and test sets.
- `src/irisml/train.py` trains a Random Forest model and saves it to the `models/` folder.
- `src/irisml/predict.py` loads the saved model and predicts on new data.
- `src/irisml/config.py` loads settings from `configs/config.yaml`.
- `src/irisml/cli.py` connects everything to command line entry points.
- `data/iris.csv` is the dataset used for training.
- `configs/config.yaml` holds paths and training settings so nothing is hardcoded.
- `tests/` has simple tests to check the preprocessing and training code works.

## Installation

Install the package in editable mode:

```
pip install -e .
```

This will install all dependencies and register the CLI commands. After installing,
you can check that the package works from anywhere, even outside the project folder:

```
python -c "import irisml; print(irisml.__version__)"
```

## Running Training

Use the `irisml-train` command to train the model:

```
irisml-train --config configs/config.yaml
```

This loads the dataset, trains the model, prints the accuracy, and saves the trained
model to `models/iris_model.joblib`.

## Running Prediction

Use the `irisml-predict` command to make predictions on a csv file:

```
irisml-predict --config configs/config.yaml --input data/iris.csv
```

This loads the saved model and prints the predicted class for each row in the input file.

## Alternative: Running Without Installed Commands

If you do not want to install the console scripts, you can also run the CLI as a module:

```
python -m irisml.cli
```

## Running Tests

```
pytest tests/
```
