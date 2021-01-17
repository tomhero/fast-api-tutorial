from typing import Optional, List

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

EXCEPTION_WORD = "Prayut"


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


items: List[Item] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_item():
    return {"item_list": items}


@app.get("/items/{item_id}")
def read_item(item_id: int, response: Response, q: Optional[str] = None):
    if len(items) < item_id or item_id <= 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"item_id": None, "item_detail": None, "queries": q}
    return {"item_id": item_id, "item_detail": items[item_id - 1], "queries": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, new_item: Item, response: Response):
    if len(items) < item_id or item_id <= 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"item_name": None, "item_id": None}
    items[item_id - 1] = new_item
    return {"item_name": new_item.name, "item_id": item_id}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item, response: Response):
    if item.name.capitalize() == EXCEPTION_WORD:
        response.status_code = status.HTTP_409_CONFLICT
        return {"item_name": None, "item_id": None}
    items.append(item)
    return {"item_name": item.name, "item_id": len(items)}
