import pytest
from app.services.data_service import DataService

@pytest.fixture
def data_service():
    return DataService()

def test_data_service_initialization(data_service):
    assert data_service.data is not None
    assert isinstance(data_service.data, object)  # xarray.Dataset

def test_get_channels(data_service):
    channels = data_service.get_channels()
    print(channels)
    assert isinstance(channels, list)

def test_get_channels_with_type(data_service):
    vel_channels = data_service.get_channels('vel')
    assert all('vel' in channel for channel in vel_channels)
