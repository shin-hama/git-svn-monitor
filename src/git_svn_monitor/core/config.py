from datetime import date
import os
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    debug: Optional[bool]
    redmine_url: str
    redmine_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


DateLike = Optional[Union[date, str]]
PathLike = Union[str, 'os.PathLike[str]']

TARGET_DIR = Path.home() / ".progress_monitor"
SETTING_FILE = Path(TARGET_DIR) / "settings.json"
GIT_LOCAL_REPOSITORY = TARGET_DIR / "monitor.git"

# Logging in target directory
LOG_FILE = TARGET_DIR / "monitor.log"

env_config = EnvConfig()
