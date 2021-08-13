from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, Iterator

import pytest

from git_svn_monitor.core import settings


@pytest.fixture
def sample_settings() -> Dict[str, Any]:
    return {
        "git_repositories": [{
            "name": "name",
            "url": "http://example.git",
        }],
        "svn_repositories": [{
            "name": "name",
            "url": "http://example.git",
        }],
        "git_author": "git",
        "svn_author": "svn",
        "last_updated": "2021-01-01T01:23:45"
    }


@pytest.fixture
def setting(sample_settings: Dict[str, Any]) -> settings.Setting:
    return settings.Setting(
        git_repositories=[settings.Repository(**sample_settings["git_repositories"][0])],
        svn_repositories=[settings.Repository(**sample_settings["svn_repositories"][0])],
        git_author=sample_settings["git_author"],
        svn_author=sample_settings["svn_author"],
        last_updated=sample_settings["last_updated"],
    )


@pytest.fixture
def settings_file(sample_settings: Dict[str, Any]) -> Iterator[Path]:
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
    assert all([isinstance(repo, settings.Repository) for repo in _settings.git_repositories])
    assert all([isinstance(repo, settings.Repository) for repo in _settings.svn_repositories])


def test_loaded_settings_value(
    setting: settings.Setting,
    settings_file: Path
) -> None:
    _settings = settings.load_settings(settings_file)
    assert _settings.git_author == setting.git_author
    assert _settings.svn_author == setting.svn_author
    assert _settings.last_updated == setting.last_updated
    assert _settings.git_repositories[0].name == setting.git_repositories[0].name
    assert _settings.git_repositories[0].url == setting.git_repositories[0].url
    assert _settings.svn_repositories[0].name == setting.svn_repositories[0].name
    assert _settings.svn_repositories[0].url == setting.svn_repositories[0].url


def test_load_not_exist_path() -> None:
    """ Load default values when doesn't exist setting file.
    """
    with pytest.raises(Exception):
        settings.load_settings("nothing.json")


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
    setting.git_author = "updated"
    settings.save_settings(settings_file, setting)
    updated = settings.load_settings(settings_file)
    assert updated.git_author == setting.git_author
