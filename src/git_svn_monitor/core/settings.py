from datetime import datetime
import json
from typing import Any, Optional, Union

from git.repo.base import Repo

from git_svn_monitor.core.config import PathLike


class Setting:
    def __init__(self, **kwargs: Any) -> None:
        self.repositories: list[Repository] = kwargs.get("repositories", [Repository()])
        self.email: str = kwargs.get("email", "example@email.com")

        if "lastUpdated" in kwargs:
            self.last_updated: Optional[datetime] = datetime.fromisoformat(kwargs["lastUpdated"])
        else:
            # Avoid to fail `datetime.fromisoformat` when does not exist "lastUpdated"
            self.last_updated = datetime.now()


class Repository:
    def __init__(self, **kwargs: Any) -> None:
        self.name: str = kwargs.get("name", "")
        self.url: str = kwargs.get("url", "")


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
