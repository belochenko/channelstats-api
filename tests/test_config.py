from app.config import Settings
import pytest

def test_settings():
    settings = Settings()
    assert hasattr(settings, 'DATA_FILE')
    assert isinstance(settings.DATA_FILE, str)