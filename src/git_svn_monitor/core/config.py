import os
from pathlib import Path
from typing import Union


PathLike = Union[str, 'os.PathLike[str]']

TARGET_DIR = Path(r"D:\workspace\hamada\test_python")
SETTING_FILE = Path(TARGET_DIR) / "settings.json"
