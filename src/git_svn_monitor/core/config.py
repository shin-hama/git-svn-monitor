from datetime import date
from logging import getLogger
import os
from pathlib import Path
from typing import Optional, Union

import dotenv
from pydantic import BaseSettings, ValidationError


logger = getLogger(__name__)
DOTENV_FILE = ".env"


class EnvConfig(BaseSettings):
    debug: Optional[bool]
    redmine_url: str
    redmine_api_key: str

    class Config:
        env_file = DOTENV_FILE
        env_file_encoding = "utf-8"


DateLike = Optional[Union[date, str]]
PathLike = Union[str, 'os.PathLike[str]']

TARGET_DIR = Path.home() / ".progress_monitor"
SETTING_FILE = Path(TARGET_DIR) / "settings.json"
GIT_LOCAL_REPOSITORY = TARGET_DIR / "monitor.git"

# Logging in target directory
LOG_FILE = TARGET_DIR / "log" / "script.log"

try:
    env_config = EnvConfig()
except ValidationError:
    logger.warning(".env file is incorrect, you have to initialize it.")
    url = input("Enter Redmine host url: ")
    key = input("Enter Redmine API key: ")
    env_config = EnvConfig(_env_file=None, redmine_url=url, redmine_api_key=key)
    dotenv.set_key(DOTENV_FILE, "REDMINE_URL", url)
    dotenv.set_key(DOTENV_FILE, "REDMINE_API_KEY", key)
