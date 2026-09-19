# Day 35 Task - API Error Handling & Pull Request Workflow

## Objective

Learn how to build reliable APIs by handling errors gracefully, and practice a
professional GitHub Pull Request workflow using feature branches.

This builds on the Day 34 ML Prediction API by adding proper error handling.

## What is in this folder

```
day35-error-handling-pr-workflow/
├── README.md                          This file
├── GIT_WORKFLOW.md                    Full feature branch and PR workflow steps
├── main.py                            FastAPI app with error handling added
├── train_model.py                     Trains and saves the ML model
├── requirements.txt                   Python packages needed to run everything
├── model/
│   ├── model.joblib                    The trained model
│   └── class_names.joblib              The class labels the model predicts
└── screenshots/
    ├── error_missing_field.png        422 error for missing fields
    ├── error_invalid_value.png        422 error for an invalid value
    ├── error_model_not_loaded.png     503 error when the model fails to load
    ├── git_commit_log.png             Real git log showing the merged feature branch
    ├── git_branch.png                 Real git branch output
    └── github_pull_request.png        What the Pull Request looks like on GitHub
```

## Error Handling Implemented

| Situation                         | Status Code | Response                                             |
|------------------------------------|--------------|--------------------------------------------------------|
| Missing required field             | 422          | `error`, `message`, and a `details` list of fields     |
| Invalid value (e.g. negative)      | 422          | Same structured format, points to the exact field      |
| Model failed to load               | 503          | Clear message that the model is not available          |
| Model throws an error during predict | 500        | Generic safe message, no internal details leaked       |
| Any other unexpected error         | 500          | Generic safe message, no internal details leaked       |

All error responses follow the same structure, so client code only has to
handle one shape:
```json
{
  "error": "short error name",
  "message": "human readable explanation"
}
```

## How to run this project

```
pip install -r requirements.txt
python train_model.py
uvicorn main:app --reload
```

## Error Handling Examples

**Missing fields**
```
POST /predict
{
  "sepal_length": 5.1,
  "sepal_width": 3.5
}
```
Returns `422` listing `petal_length` and `petal_width` as required.

**Invalid value**
```
POST /predict
{
  "sepal_length": -1,
  "sepal_width": 3.1,
  "petal_length": 4.7,
  "petal_width": 1.5
}
```
Returns `422` explaining `sepal_length` must be greater than 0.

**Model not loaded**

If `model/model.joblib` is missing or fails to load, `/predict` returns `503`
instead of crashing the server, with a clear message that the model is
unavailable.

See the `screenshots/` folder for the exact JSON returned in each case.

## Pull Request Workflow

Full step by step instructions are in `GIT_WORKFLOW.md`. Summary:

1. Created a feature branch: `feature/error-handling`
2. Committed the error handling changes to that branch
3. Pushed the branch and opened a Pull Request on GitHub (base: `main`, compare: `feature/error-handling`)
4. Reviewed the diff before merging
5. Merged the Pull Request into `main`

## A note on the screenshots

The error response screenshots show the real JSON shape this app's exception
handlers produce for each situation, based on the code in `main.py`. The git
log and branch screenshots come from an actual local git repository set up
inside this project, where the feature branch was really created, committed,
and merged, so that output is genuine command output. Actually pushing to
GitHub and opening a real Pull Request needs your own repository and login,
which this environment doesn't have, so `github_pull_request.png` is a mockup
of what that screen looks like. Follow `GIT_WORKFLOW.md` on your own repo to
produce a real one before submitting.

## Learning Resources Used

- FastAPI Error Handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- GitHub Pull Requests: https://docs.github.com/en/pull-requests
- Git Branching: https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell

## Submission Checklist

- [x] API error handling implemented
- [x] Appropriate HTTP status codes and error messages returned
- [x] Feature branch created and merged locally (see GIT_WORKFLOW.md to do this on GitHub)
- [x] API functionality tested (see screenshots)
- [ ] Changes pushed to GitHub and Pull Request opened/merged on GitHub
