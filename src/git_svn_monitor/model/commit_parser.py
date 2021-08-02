from datetime import datetime
import re
from typing import Optional, Union

from git_svn_monitor.core.config import DateLike, GitCommit


TICKET_PREFIX = "refs #"
TICKET_PATTERN = re.compile(f"{TICKET_PREFIX}[0-9]*")


def parse_ticket_number(message: Union[bytes, str]) -> Optional[str]:
    """ Get ticket number written in commit message.
    We can find to match the pattern of `refs #****`.

    Return
    ------
    ticket_number: str or None
        The ticket number of ticket registered in redmine is related to inputted commit.
        Return None when a number is not written in commit message.
    """
    _message = message
    if isinstance(_message, bytes):
        _message = _message.decode("utf-8")

    matched = TICKET_PATTERN.search(_message)
    if matched is None:
        return None

    ticket_number = matched.group().replace(TICKET_PREFIX, "")
    return ticket_number


def build_message_for_redmine(
    summary: str,
    author_name: str,
    message: str,
    timestamp: Union[datetime, str]
) -> str:
    """ Build message for upload redmine.
    """
    # title for the collapsed message
    _title = f"{summary}: {author_name}".strip()

    # Set timestamp message for it is committed
    if isinstance(timestamp, datetime):
        timestamp = timestamp.isoformat()
    _timestamp = f"Datetime: {timestamp}"

    # Main containts is able to show when open the collapsed message.
    _containts = f"{_timestamp}\n\n{message}"

    # need new line at the both start and end of message to define collect collapsed sentence.
    msg = f"{{{{collapse({_title})\n{_containts}\n}}}}"

    return msg
