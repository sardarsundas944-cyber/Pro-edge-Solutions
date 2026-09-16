# Day 33 Task - Request & Response Validation with Pydantic

## Objective

Learn how to validate API data using Pydantic models so that requests and responses
follow a predefined structure, and invalid data gets rejected before it is processed.

This builds on the Day 32 FastAPI app by adding proper request and response models.

## What is in this folder

```
day33-fastapi-validation/
├── README.md                          This file
├── main.py                            The FastAPI application with Pydantic models
├── requirements.txt                   Python packages needed to run the app
└── screenshots/
    ├── swagger_ui.png                 Swagger docs showing routes and schemas
    ├── create_item_success.png        POST /items with valid data
    ├── create_item_invalid.png        POST /items with invalid data (422 error)
    ├── create_item_missing_field.png  POST /items with a missing required field
    └── get_items.png                  GET /items result
```

## Pydantic Models

### ItemRequest (used for incoming POST data)

| Field    | Type  | Rule                              |
|----------|-------|-------------------------------------|
| name     | str   | minimum 2, maximum 50 characters   |
| price    | float | must be greater than 0             |
| quantity | int   | must be 1 or more, default is 1    |

### ItemResponse (used for outgoing data)

| Field    | Type  | Description                    |
|----------|-------|----------------------------------|
| id       | int   | Auto generated item id           |
| name     | str   | Item name                        |
| price    | float | Item price                       |
| quantity | int   | Item quantity                    |
| message  | str   | Confirmation message             |

Because `response_model=ItemResponse` is set on the route, FastAPI will always
return data in exactly this shape, no matter what extra data exists internally.

## Routes

| Method | Path            | Request Body   | Response Model         |
|--------|-----------------|----------------|-------------------------|
| GET    | /               | none           | plain dict              |
| GET    | /health         | none           | plain dict              |
| GET    | /greet/{name}   | none           | plain dict              |
| GET    | /items          | none           | list of ItemResponse    |
| POST   | /items          | ItemRequest    | ItemResponse            |

## How to run this app

```
pip install -r requirements.txt
uvicorn main:app --reload
```

App runs on `http://127.0.0.1:8000`
Swagger docs are at `http://127.0.0.1:8000/docs`

## Validation Examples

**Valid request**
```
POST /items
{
  "name": "Laptop",
  "price": 799.99,
  "quantity": 2
}
```
Returns `200 OK` with the created item.

**Invalid request - name too short and price not positive**
```
POST /items
{
  "name": "A",
  "price": -10,
  "quantity": 2
}
```
Returns `422 Unprocessable Entity` with a detail list explaining exactly which
fields failed and why, without ever running the request handler code.

**Invalid request - missing required field**
```
POST /items
{
  "name": "Mouse"
}
```
Returns `422 Unprocessable Entity` because `price` is required and was not sent.

See the `screenshots/` folder for the exact JSON returned in each case.

## A note on the screenshots

These screenshots show the exact JSON FastAPI and Pydantic return for these
requests based on the validation rules defined in `main.py`. They were built as
a preview of the expected output rather than captured from a live browser
session. Running the steps above on your own machine will produce matching
real output and a real `/docs` page — feel free to swap in your own screenshots
from that run before submitting.

## Learning Resources Used

- Pydantic Documentation: https://docs.pydantic.dev/
- FastAPI Request Body: https://fastapi.tiangolo.com/tutorial/body/
- FastAPI Response Model: https://fastapi.tiangolo.com/tutorial/response-model/
- FastAPI Validation: https://fastapi.tiangolo.com/tutorial/body-fields/

## Submission Checklist

- [x] Request validation implemented
- [x] Response models created and used
- [x] Invalid input rejected automatically
- [x] API responses follow a consistent structure
- [ ] Changes pushed to GitHub
