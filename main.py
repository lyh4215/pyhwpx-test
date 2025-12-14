from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"안녕": "FastAPI"}

#path operation
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

#query
@app.get("/search")
def search(q: str | None = None, limit: int = 10):
    return {"q": q, "limit": limit}

from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    is_sale: bool = False

#
@app.post("/items")
def create_item(item: ItemCreate):
    return item
