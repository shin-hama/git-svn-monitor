from datetime import datetime
import json
from typing import Any, Optional, Union

from git_svn_monitor.core.config import PathLike, TARGET_DIR


class Setting:
    def __init__(self, **kwargs: Any) -> None:
        self.repositories: list[Repository] = kwargs.get("repositories", [])
        self.email: str = kwargs.get("email", "")
        self.last_updated: Optional[datetime] = kwargs.get("lastUpdated", None)


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
