from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# Define a data model for the request body
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

# Define an endpoint to create an item
@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

# Define an endpoint to get an item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Here you could add logic to retrieve the item from a database
    return {"item_id": item_id, "name": "Sample Item"}
