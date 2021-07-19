from datetime import date
import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv


load_dotenv(".env")

PathLike = Union[str, 'os.PathLike[str]']
DateLike = Optional[Union[date, str]]

TARGET_DIR = Path.home() / ".progress_monitor" / "monitor.git/"
SETTING_FILE = Path(TARGET_DIR) / "settings.json"

REDMINE_URL = os.getenv("REDMINE_URL", "")
REDMINE_API_KEY = os.getenv("REDMINE_API_KEY", "")
