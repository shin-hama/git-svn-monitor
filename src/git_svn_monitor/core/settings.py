from datetime import datetime
import json
from typing import Any, Union

from git_svn_monitor.core.config import PathLike


class Repository:
    def __init__(self, **kwargs: Any) -> None:
        self.name: str = kwargs.get("name", "")
        self.url: str = kwargs.get("url", "")

    def to_dict(self) -> dict[str, str]:
        return self.__dict__


class Setting:
    def __init__(self, **kwargs: Any) -> None:
        self.repositories: list[Repository] = kwargs.get("repositories", [])
        self.email: str = kwargs.get("email", "example@email.com")

        if "lastUpdated" in kwargs:
            self.last_updated: datetime = datetime.fromisoformat(kwargs["lastUpdated"])
        else:
            # Avoid to fail `datetime.fromisoformat` when does not exist "lastUpdated"
            self.last_updated = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        return {
            "repositories": [
                repo.to_dict() for repo in self.repositories
            ],
            "email": self.email,
            "lastUpdated": self.last_updated.isoformat()
        }


def decode_settings(data: dict[str, Any]) -> Union[Setting, Repository]:
    if "repositories" in data:
        return Setting(**data)
    else:
        # nested data
        return Repository(**data)


def load_settings(path: PathLike) -> Setting:
    with open(path, mode="r", encoding="utf-8") as f:
        settings = json.load(f, object_hook=decode_settings)

    return settings


def save_settings(path: PathLike, setting: Setting) -> None:
    _dict = setting.to_dict()

    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(_dict, f)
