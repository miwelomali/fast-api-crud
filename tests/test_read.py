from .conftest import client

def test_read_items(fresh_item_id):
    response = client.get("/items/")
    assert response.status_code == 200
    items = response.json()["items"]
    assert any(item["id"] == fresh_item_id for item in items)

def test_read_single_item(fresh_item_id):
    response = client.get(f"/items/{fresh_item_id}")
    assert response.status_code == 200
    assert response.json()["item"]["id"] == fresh_item_id