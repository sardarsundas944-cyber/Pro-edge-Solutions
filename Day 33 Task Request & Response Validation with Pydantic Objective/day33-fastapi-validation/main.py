from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Day 33 FastAPI Validation App")

class ItemRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=1, default=1)

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    message: str

items_db = []
next_id = 1

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI app"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items", response_model=List[ItemResponse])
def get_items():
    return items_db

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemRequest):
    global next_id
    new_item = ItemResponse(
        id=next_id,
        name=item.name,
        price=item.price,
        quantity=item.quantity,
        message="Item created successfully"
    )
    items_db.append(new_item)
    next_id += 1
    return new_item
