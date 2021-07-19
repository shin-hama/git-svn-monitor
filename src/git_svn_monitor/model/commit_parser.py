import re
from typing import Optional

import git


TICKET_PREFIX = "refs #"
TICKET_PATTERN = re.compile(f"{TICKET_PREFIX}[0-9]*")


def parse_ticket_number(message: str) -> Optional[str]:
    """ Get ticket number written in commit message.
    We can find to match the pattern of `refs #****`.

    Return
    ------
    ticket_number: str or None
        The ticket number of ticket registered in redmine is related to inputted commit.
        Return None when a number is not written in commit message.
    """
    _message = message
    matched = TICKET_PATTERN.search(_message)
    if matched is None:
        return None

    ticket_number = matched.group().replace(TICKET_PREFIX, "")
    return ticket_number


def build_message_for_redmine(commit: git.base.Commit) -> str:
    """ Build message for upload redmine.
    """
    # title for the collapsed message
    _title = f"{commit.summary.strip()}: {commit.author.name}".strip()
    # Main containts is able to show when open the collapsed message.
    _timestamp = f"Datetime: {commit.authored_datetime.isoformat()}"
    _containts = f"{_timestamp}\n\n{commit.message.strip()}"

    # need new line at the both start and end of message to define collect collapsed sentence.
    message = f"{{{{collapse({_title})\n{_containts}\n}}}}"

    return message
