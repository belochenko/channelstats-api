from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_get_all_stats(client):
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert isinstance(stats, dict)
    for channel_stats in stats.values():
        assert isinstance(channel_stats, dict)
        assert all(key in channel_stats for key in ['mean', 'std', 'min', 'max', 'count'])
        assert isinstance(channel_stats['mean'], (int, float))
        assert isinstance(channel_stats['std'], (int, float))
        assert isinstance(channel_stats['min'], (int, float))
        assert isinstance(channel_stats['max'], (int, float))
        assert isinstance(channel_stats['count'], int)

def test_get_stats_for_specific_channels(client):
    response = client.get("/stats?channels=vel58.3&channels=temp56.8")
    assert response.status_code == 200
    data = response.json()
    assert "vel58.3" in data
    assert "temp56.8" in data
    for channel in ["vel58.3", "temp56.8"]:
        channel_stats = data[channel]
        print(key in channel_stats for key in ['mean', 'std', 'min', 'max', 'count'])
        assert all(key in channel_stats for key in ['mean', 'std', 'min', 'max', 'count'])
        assert isinstance(channel_stats['mean'], (int, float))
        assert isinstance(channel_stats['std'], (int, float))
        assert isinstance(channel_stats['min'], (int, float))
        assert isinstance(channel_stats['max'], (int, float))
        assert isinstance(channel_stats['count'], int)

def test_get_stats_with_date_range(client):
    response = client.get("/stats?start_date=2019-06-27&end_date=2019-06-28")
    assert response.status_code == 200
    stats = response.json()
    assert isinstance(stats, dict)
    for channel_stats in stats.values():
        assert isinstance(channel_stats, dict)
        assert all(key in channel_stats for key in ['mean', 'std', 'min', 'max', 'count'])
        assert isinstance(channel_stats['mean'], (int, float))
        assert isinstance(channel_stats['std'], (int, float))
        assert isinstance(channel_stats['min'], (int, float))
        assert isinstance(channel_stats['max'], (int, float))
        assert isinstance(channel_stats['count'], int)

def test_get_stats_with_only_start_date(client):
    response = client.get("/stats?start_date=2019-06-27%2003:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_stats_with_only_end_date(client):
    response = client.get("/stats?end_date=2019-06-27%2004:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_stats_invalid_channel(client):
    response = client.get("/stats?channels=invalid_channel")
    assert response.status_code == 400
    assert "Invalid channel(s)" in response.json()["detail"]

def test_get_stats_invalid_date_range(client):
    response = client.get("/stats?start_date=2030-01-01%2000:00:00&end_date=2030-01-02%2000:00:00")
    assert response.status_code == 404
    assert "No data found for the given parameters" in response.json()["detail"]

def test_get_stats_invalid_date_format(client):
    response = client.get("/stats?start_date=2019-13-01%2000:00:00")
    assert response.status_code == 400
    assert "Invalid datetime format" in response.json()["detail"]

def test_get_stats_with_specific_time(client):
    response = client.get("/stats?start_date=2019-06-27%2004:00:00&end_date=2019-06-27%2005:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
