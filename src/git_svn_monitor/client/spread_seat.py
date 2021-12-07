from logging import getLogger
from typing import Any, Callable, List, Optional

import gspread

from git_svn_monitor.core.config import env_config, GOOGLE_API_CREDENTIALS_FILE, TIMESTAMP_FORMAT
from git_svn_monitor.model.commit_parser import BaseCommit


logger = getLogger(__name__)


def open_spread_sheet() -> gspread.Spreadsheet:
    """ Autharise by secret key from json file and open first worksheet.
    """
    try:
        if env_config.debug:
            sheet_key = env_config.debug_spread_sheet_key
        else:
            sheet_key = env_config.spread_sheet_key
        if sheet_key is None:
            logger.warning("No SPREAD_SHEET_KEY, please set up.")
            return None

    except Exception as e:
        logger.warning("Fail to connect spread sheet")
        logger.warning(e.args)
        return None
    client = gspread.service_account(GOOGLE_API_CREDENTIALS_FILE)
    spread_sheet = client.open_by_key(sheet_key)
    logger.info(f"Open SpreadSheet: {spread_sheet.url}")
    return spread_sheet


def upload_commits(commits: List[BaseCommit]) -> Optional[str]:
    """ Upload commit parameter to spread sheet.
    """
    spread_sheet = open_spread_sheet()
    ws = spread_sheet.sheet1

    # Get header row
    cols = ws.row_values(1)

    vals = [
        [
            _convert_to_str(getattr(commit, col))
            for col in cols
        ]
        for commit in commits
    ]
    ws.append_rows(vals, value_input_option="USER_ENTERED")

    return spread_sheet.url


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
    logger.error(f"Cannot convert {type(val)} to str, you have to implement converter")
    logger.error(f"Original value: {val}")
    raise NotImplementedError
