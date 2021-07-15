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
        "email": "test@email.com",
        "last_updated": "2021-01-01T01:23:45"
    }


@pytest.fixture
def setting(sample_settings: dict[str, Any]) -> settings.Setting:
    return settings.Setting(
        repositories=[settings.Repository(**sample_settings["repositories"][0])],
        email=sample_settings["email"],
        last_updated=sample_settings["last_updated"],
    )


@pytest.fixture
def settings_file(sample_settings: dict[str, Any]) -> Iterator[Path]:
    settings_file = Path(__file__).resolve().parent / "settings.json"
    with open(settings_file, mode="w", encoding="utf-8") as f:
        json.dump(sample_settings, f)

    yield settings_file
    # delete file after testing
    settings_file.unlink()


def test_load_settings_into_instance(settings_file: Path) -> None:
    """ Test to convert the parameters in settings file into collect object
    """
    _settings = settings.load_settings(settings_file)
    assert isinstance(_settings, settings.Setting)
    assert isinstance(_settings.last_updated, datetime)
    assert all([isinstance(repo, settings.Repository) for repo in _settings.repositories])


def test_loaded_settings_value(
    setting: settings.Setting,
    settings_file: Path
) -> None:
    _settings = settings.load_settings(settings_file)
    assert _settings.email == setting.email
    assert _settings.last_updated == setting.last_updated
    assert _settings.repositories[0].name == setting.repositories[0].name
    assert _settings.repositories[0].url == setting.repositories[0].url


def test_load_not_existed_path() -> None:
    """ Load default values when doesn't exist setting file.
    """
    default_settings = settings.Setting()
    _settings = settings.load_settings("")
    assert isinstance(_settings, settings.Setting)
    # last_updated is not same value because defined by datetime.now()
    assert _settings.email == default_settings.email
    assert _settings.repositories[0].name == default_settings.repositories[0].name
    assert _settings.repositories[0].url == default_settings.repositories[0].url


def test_save_settings(setting: settings.Setting) -> None:
    """ Test to be able to create setting file from Setting instance.
    """
    filepath = Path(__file__).resolve().parent / "settings.json"
    settings.save_settings(filepath, setting)
    assert filepath.exists()
    filepath.unlink()


def test_overwrite_settings(settings_file: Path, setting: settings.Setting) -> None:
    """ Overwrite settings file if already exists.
    """
    setting.last_updated = datetime.now()
    org_timestamp = settings_file.stat().st_mtime
    settings.save_settings(settings_file, setting)
    updated_timestamp = settings_file.stat().st_mtime
    assert org_timestamp < updated_timestamp
