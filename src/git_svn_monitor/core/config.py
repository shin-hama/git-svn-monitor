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


PathLike = Union[str, 'os.PathLike[str]']
DateLike = Optional[Union[date, str]]

TARGET_DIR = Path.home() / ".progress_monitor" / "monitor.git/"
SETTING_FILE = Path(TARGET_DIR) / "settings.json"

env_config = EnvConfig()
