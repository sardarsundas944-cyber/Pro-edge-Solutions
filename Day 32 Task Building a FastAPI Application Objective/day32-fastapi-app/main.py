from fastapi import FastAPI

app = FastAPI(title="Day 32 FastAPI App")

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI app"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items")
def get_items():
    items = [
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Phone"},
        {"id": 3, "name": "Headphones"}
    ]
    return {"items": items}

@app.post("/items")
def create_item(item: dict):
    return {"message": "Item created successfully", "item": item}
