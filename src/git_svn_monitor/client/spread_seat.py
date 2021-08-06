import os

import gspread

from git_svn_monitor.core.config import env_config, GOOGLE_API_CREDENTIALS_FILE, PathLike


def connect_gspread(json_file: PathLike, sheet_key: str) -> gspread.Worksheet:
    gc = gspread.service_account(json_file)
    worksheet = gc.open_by_key(sheet_key).sheet1
    return worksheet


# Set up a proxy to connect spread sheet api temporarily.
if env_config.proxy is not None:
    os.environ.update({"http_proxy": env_config.proxy})
    os.environ.update({"https_proxy": env_config.proxy})

if env_config.spread_sheet_key:
    ws = connect_gspread(GOOGLE_API_CREDENTIALS_FILE, env_config.spread_sheet_key)

cols = ws.row_values(1)
ws.insert_row(cols, index=2)

os.environ.update({"http_proxy": ""})
os.environ.update({"https_proxy": ""})
