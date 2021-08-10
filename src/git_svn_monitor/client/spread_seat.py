from logging import getLogger
import os
from typing import Any, Callable, List, Optional

import gspread

from git_svn_monitor.core.config import (
    env_config, GOOGLE_API_CREDENTIALS_FILE, PathLike, TIMESTAMP_FORMAT
)
from git_svn_monitor.model.commit_parser import BaseCommit


logger = getLogger(__name__)


def open_spread_sheet(json_file: PathLike, sheet_key: str) -> gspread.Worksheet:
    """ Autharise by secret key from json file and open first worksheet.
    """
    gc = gspread.service_account(json_file)
    worksheet = gc.open_by_key(sheet_key).sheet1
    return worksheet


def upload_commit(commit: BaseCommit) -> Optional[str]:
    """ Upload commit parameter to spread sheet.
    """
    # Set up a proxy to connect spread sheet api temporarily.
    if env_config.proxy is not None:
        os.environ.update({"http_proxy": env_config.proxy})
        os.environ.update({"https_proxy": env_config.proxy})

    try:
        if env_config.debug:
            sheet_key = env_config.debug_spread_sheet_key
        else:
            sheet_key = env_config.spread_sheet_key
        if sheet_key is None:
            logger.warning("No SPREAD_SHEET_KEY, please set up.")
            return None

        ws = open_spread_sheet(GOOGLE_API_CREDENTIALS_FILE, sheet_key)
    except Exception as e:
        logger.warning("Fail to connect spread sheet")
        logger.warning(e.args)
        return None

    # Get header row
    cols = ws.row_values(1)

    vals = [_convert_to_str(getattr(commit, col)) for col in cols]
    ws.append_row(vals, value_input_option="USER_ENTERED")

    os.environ.update({"http_proxy": ""})
    os.environ.update({"https_proxy": ""})

    return ws.url


def _convert_to_str(val: Any) -> str:
    """ Convert any types of value to string, supported type is defined in `funcs`
    """
    funcs: List[Callable[[Any], str]] = [
        lambda x: x.strftime(format=TIMESTAMP_FORMAT),  # datetime
        str
    ]

    for f in funcs:
        try:
            return f(val).strip()
        except AttributeError or ValueError:
            continue
    logger.error(f"Cannot convert {type(val)} to str, you have to define function")
    raise NotImplementedError
