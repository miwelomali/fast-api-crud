from .conftest import client

def test_update_item(fresh_item_id):
    response = client.put(
        f"/items/{fresh_item_id}",
        json={"id": fresh_item_id, "name": "Updated", "description": "Updated Desc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["name"] == "Updated"
    assert data["item"]["description"] == "Updated Desc"