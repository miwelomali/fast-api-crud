from pydantic import BaseModel
class ItemCreate(BaseModel):
    name: str
    description: str

class Item(BaseModel):
    id: str
    name: str
    description: str