import re
from typing import Optional, Union

from git_svn_monitor.core.config import GitCommit


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


def build_message_for_redmine(commit: GitCommit) -> str:
    """ Build message for upload redmine.
    """
    _summary = commit.summary.strip()
    if isinstance(_summary, bytes):
        _summary = _summary.decode("utf-8")
    # title for the collapsed message
    _title = f"{_summary}: {commit.author.name}".strip()

    _message = commit.message.strip()
    if isinstance(_message, bytes):
        _message = _message.decode("utf-8")
    # Main containts is able to show when open the collapsed message.
    _timestamp = f"Datetime: {commit.authored_datetime.isoformat()}"
    _containts = f"{_timestamp}\n\n{_message}"

    # need new line at the both start and end of message to define collect collapsed sentence.
    message = f"{{{{collapse({_title})\n{_containts}\n}}}}"

    return message
