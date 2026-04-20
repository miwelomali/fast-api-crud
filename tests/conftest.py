import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def fresh_item_id():
    """Create one item per test module and return its ID."""
    response = client.post("/items/", json={"name": "FixtureTest", "description": "FixtureDesc"})
    assert response.status_code == 200
    return response.json()["item"]["id"]