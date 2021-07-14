from datetime import datetime
import json
from pathlib import Path
from typing import Any, Iterator

import pytest

from git_svn_monitor.core import settings


@pytest.fixture
def sample_settings() -> dict[str, Any]:
    return {
        "repositories": [{
            "name": "name",
            "url": "http://example.git",
        }],
        "email": "example@email.com",
        "last_updated": "2021-01-01T01:23:45"
    }


@pytest.fixture
def settings_path(sample_settings: dict[str, Any]) -> Iterator[Path]:
    settings_file = Path(__file__).resolve().parent / "settings.json"
    with open(settings_file, mode="w", encoding="utf-8") as f:
        json.dump(sample_settings, f)

    yield settings_file
    # delete file after testing
    settings_file.unlink()


def test_load_settings_into_instance(settings_path: Path) -> None:
    """ Test to convert the parameters in settings file into collect object
    """
    _settings = settings.load_settings(settings_path)
    assert isinstance(_settings, settings.Setting)
    assert isinstance(_settings.last_updated, datetime)
    assert all([isinstance(repo, settings.Repository) for repo in _settings.repositories])


def test_loaded_settings_value(
    sample_settings: dict[str, Any],
    settings_path: Path
) -> None:
    _settings = settings.load_settings(settings_path)
    assert _settings.email == sample_settings["email"]
    assert _settings.last_updated.isoformat() == sample_settings["last_updated"]
    assert _settings.repositories[0].name == sample_settings["repositories"][0]["name"]
    assert _settings.repositories[0].url == sample_settings["repositories"][0]["url"]
