import json
from pathlib import Path
from typing import Any, Optional

from git_svn_monitor.core.config import PathLike


def load_settings(path: Optional[PathLike] = None) -> dict[str, Any]:
    setting_file = path
    if setting_file is None:
        setting_file = Path(__file__).resolve().parent / "./settings.json"

    with open(setting_file, mode="r", encoding="utf-8") as f:
        settings = json.load(f)

    return settings
