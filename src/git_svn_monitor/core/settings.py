from datetime import datetime
import json
from typing import Any, Union

from git_svn_monitor.core.config import PathLike


class Repository:
    def __init__(self, **kwargs: Any) -> None:
        self.name: str = kwargs.get("name", "")
        self.url: str = kwargs.get("url", "")


class Setting:
    def __init__(self, **kwargs: Any) -> None:
        self.repositories: list[Repository] = kwargs.get("repositories", [])
        self.email: str = kwargs.get("email", "example@email.com")

        if "last_updated" in kwargs:
            self.last_updated: datetime = datetime.fromisoformat(kwargs["last_updated"])
        else:
            # Avoid to fail `datetime.fromisoformat` when does not exist "lastUpdated"
            self.last_updated = datetime.now()


def load_settings(path: PathLike) -> Setting:
    def _decode_settings(data: dict[str, Any]) -> Union[Setting, Repository]:
        if "repositories" in data:
            return Setting(**data)
        else:
            # nested data
            return Repository(**data)

    with open(path, mode="r", encoding="utf-8") as f:
        settings = json.load(f, object_hook=_decode_settings)

    return settings


def save_settings(path: PathLike, setting: Setting) -> None:
    def encode_settings(o: Any) -> Union[dict[str, Any], str]:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, (Repository, Setting)):
            return o.__dict__
        return o

    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(setting, f, default=encode_settings)
