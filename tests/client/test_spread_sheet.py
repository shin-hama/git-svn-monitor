from datetime import datetime

from git_svn_monitor.client import spread_seat
from git_svn_monitor.core.config import TIMESTAMP_FORMAT


def test__convert_datetime_to_str() -> None:
    timestamp = "2021-01-01 12:34:56"
    _timestamp = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    converted = spread_seat._convert_to_str(_timestamp)
    assert timestamp == converted


def test__convert_int_to_str() -> None:
    num = 1
    converted = spread_seat._convert_to_str(num)
    assert converted == "1"


def test__convert_str_with_new_line() -> None:
    text = "new line"
    converted = spread_seat._convert_to_str(text+"\n")
    assert converted == text
