from .conftest import client

def test_delete_item(fresh_item_id):
    response = client.delete(f"/items/{fresh_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["id"] == fresh_item_id

def test_read_deleted_item(fresh_item_id):
    response = client.get(f"/items/{fresh_item_id}")
    assert response.status_code == 404