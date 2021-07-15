import os
from pathlib import Path
from typing import Union


PathLike = Union[str, 'os.PathLike[str]']

TARGET_DIR = Path.home() / ".progress_monitor" / "monitor.git/"
SETTING_FILE = Path(TARGET_DIR) / "settings.json"
