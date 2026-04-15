# Step 1: Import necessary modules
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import uuid

# Step 2: Create the FastAPI instance
app = FastAPI()

# Step 3: Create the data models
class ItemCreate(BaseModel):
    name: str
    description: str

class Item(BaseModel):
    id: str
    name: str
    description: str

# Step 4: In-memory storage
Items = {}

# Create CRUD methods
# POST
@app.post("/items/")
def create_item(item: ItemCreate):
    item_id = str(uuid.uuid4())
    new_Item = Item(id=item_id, **item.model_dump())
    Items[item_id] = new_Item
    return {"message": "Item created", "item": new_Item}

# READ all items
@app.get("/items/")
def read_items():
    return {"items": list(Items.values())}

# READ single item
@app.get("/items/{item_id}")
def read_item(item_id: str):
    if not item_id in Items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": Items[item_id]}

# UPDATE single item
@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    if not item_id in Items:
        raise HTTPException(status_code=404, detail="Item not found")
    Items[item_id] = item
    return {"message": "Item Updated", "item": item}

# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if not item_id in Items:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = Items.pop(item_id)
    return {"message": "Item Deleted", "item": deleted_item}

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

# DONE Python Project
# TODO Dockerize project
# TODO Production release project
# TODO SSL/DNS manage project