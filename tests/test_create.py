from .conftest import client

def test_create_item():
    response = client.post("/items/", json={"name": "Another", "description": "Extra"})
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["name"] == "Another"
    assert data["item"]["description"] == "Extra"