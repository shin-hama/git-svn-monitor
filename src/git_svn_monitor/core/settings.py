from datetime import datetime
import json
from logging import getLogger
from pathlib import Path
from typing import Any, Dict, List, Union

from git_svn_monitor.core.config import PathLike, SETTING_FILE


logger = getLogger(__name__)


class Repository:
    def __init__(self, **kwargs: Any) -> None:
        self.name: str = kwargs.get("name", "")
        self.url: str = kwargs.get("url", "")

    def __str__(self) -> str:
        return (
            f"name: {self.name}, "
            f"url: {self.url}"
        )


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

    def __str__(self) -> str:
        return (
            f"git_repositories: {[str(repo) for repo in self.git_repositories]}, "
            f"svn_repositories: {[str(repo) for repo in self.svn_repositories]}, "
            f"git_author: {self.git_author}, "
            f"svn_author: {self.svn_author}, "
            f"last_updated: {self.last_updated}"
        )


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
    logger.info(f"load setting file: {path}")
    _path = Path(path)
    if _path.is_dir():
        msg = f"{path} is directory, not setting file"
        logger.error(msg)
        raise Exception(msg)

    if _path.exists():
        with open(path, mode="r", encoding="utf-8") as f:
            setting = json.load(f, object_hook=_decode_settings)
    else:
        msg = f"The setting file doesn't exist on {_path}, please setup monitoring setting."
        logger.error(msg)
        raise Exception(msg)
    logger.debug(f"Current setting: {setting}")

    return setting


def save_settings(settings: Setting, filepath: PathLike = SETTING_FILE) -> None:
    """ Save Setting instance to json to update last update. Overwrite file if already exists.
    """
    def encode_settings(o: Any) -> Union[Dict[str, Any], str]:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, (Repository, Setting)):
            return o.__dict__
        return o

    logger.info(f"Save setting file to: {filepath}")
    logger.debug(f"Setting parameter: {settings}")

    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(settings, f, default=encode_settings, indent=2)
