from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Union

from git_svn_monitor.core.config import env_config, PathLike, SETTING_FILE


class Repository:
    def __init__(self, **kwargs: Any) -> None:
        self.name: str = kwargs.get("name", "")
        self.url: str = kwargs.get("url", "")


class Setting:
    def __init__(self, **kwargs: Any) -> None:
        self.git_repositories: List[Repository] = kwargs.get("git_repositories", [Repository()])
        self.svn_repositories: List[Repository] = kwargs.get("svn_repositories", [Repository()])
        self.git_author: str = kwargs.get("git_author", "author")
        self.svn_author: str = kwargs.get("svn_author", "author")

        if "last_updated" in kwargs:
            self.last_updated: datetime = datetime.fromisoformat(kwargs["last_updated"])
        else:
            # Avoid to fail `datetime.fromisoformat` when does not exist "lastUpdated"
            self.last_updated = datetime.now()


_setting: Union[Setting, None] = None


def load_settings(path: PathLike = SETTING_FILE) -> Setting:
    """ Load setting file and convert into Setting instance. Return default instacne when setting
    file is not existed.
    """
    def _decode_settings(data: Dict[str, Any]) -> Union[Setting, Repository]:
        if "git_repositories" in data or "svn_repositories" in data:
            return Setting(**data)
        else:
            # nested data
            return Repository(**data)
    global _setting
    if _setting is not None:
        return _setting

    _path = Path(path)
    if _path.is_dir():
        raise Exception(f"{path} is directory, not setting file")

    if _path.exists():
        with open(path, mode="r", encoding="utf-8") as f:
            _setting = json.load(f, object_hook=_decode_settings)
    else:
        _setting = Setting()

    return _setting


def save_settings() -> None:
    """ Save Setting instance to json to update last update. Overwrite file if already exists.
    """
    def encode_settings(o: Any) -> Union[Dict[str, Any], str]:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, (Repository, Setting)):
            return o.__dict__
        return o

    if _setting is None:
        return None

    if env_config.debug is False:
        _setting.last_updated = datetime.now()

    with open(SETTING_FILE, mode="w", encoding="utf-8") as f:
        json.dump(_setting, f, default=encode_settings, indent=2)
