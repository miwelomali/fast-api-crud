from fastapi import FastAPI, HTTPException
from uuid import uuid4

# Import from the app package
from app.schemas import ItemCreate, Item
from app.storage import Items

app = FastAPI()

@app.post("/items/")
def create_item(item: ItemCreate):
    item_id = str(uuid4())
    new_item = Item(id=item_id, **item.model_dump())
    Items[item_id] = new_item
    return {"message": "Item created", "item": new_item}

@app.get("/items/")
def read_items():
    return {"items": list(Items.values())}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in Items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": Items[item_id]}

@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    if item_id not in Items:
        raise HTTPException(status_code=404, detail="Item not found")
    Items[item_id] = item
    return {"message": "Item Updated", "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in Items:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = Items.pop(item_id)
    return {"message": "Item Deleted", "item": deleted_item}

# DONE Python Project
# DONE Dockerize project
# DONE SSL/DNS manage project
# DONE Production release project
# DONE Project change locations into folders
# DONE TEST Casing w/ Dagger
# TODO CI/CD w/ Dagger and Github actions
# TODO k8s w/ Argo CD
