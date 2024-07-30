from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_state():
    assert hasattr(app.state, 'data_service')
    assert app.state.data_service is not None