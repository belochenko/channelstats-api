from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_get_channels(client):
    response = client.get("/channels")
    assert response.status_code == 200
    assert isinstance(response.json()["channels"], list)
    assert "t" not in response.json()["channels"]
    assert "timestamp" not in response.json()["channels"]

def test_get_channels_with_type(client):
    response = client.get("/channels?channel_type=vel")
    assert response.status_code == 200
    assert isinstance(response.json()["channels"], list)
    assert all("vel" in channel for channel in response.json()["channels"])
    assert "t" not in response.json()["channels"]
    assert "timestamp" not in response.json()["channels"]
