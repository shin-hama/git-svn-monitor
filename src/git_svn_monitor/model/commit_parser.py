from datetime import datetime
from logging import getLogger
import re
from typing import Any, Optional, Union

from git.objects import Commit

from git_svn_monitor.util.log_entry import LogEntry


logger = getLogger(__name__)

ID_PREFIX = "refs #"
TICKET_PATTERN = re.compile(f"{ID_PREFIX}[0-9]*")


class BaseCommit(object):
    author: Union[str, None]
    timestamp: datetime
    message: str
    summary: str

    def __init__(self, commit: Any):
        raise NotImplementedError

    def parse_ticket_number(self) -> Optional[int]:
        """ Get ticket number written in commit message.
        We can find to match the pattern of `refs #****`.

        Return
        ------
        ticket_number: str or None
            The ticket number of ticket registered in redmine is related to inputted commit.
            Return None when a number is not written in commit message.
        """
        matched = TICKET_PATTERN.search(self.message)
        if matched is None:
            logger.debug(f"No ticket refs: {self.message}")
            return None
        logger.debug(f"Matched: {matched}")

        ticket_number = matched.group().replace(ID_PREFIX, "")
        return int(ticket_number)

    def build_message_for_redmine(self) -> str:
        """ Build message for upload redmine.
        """
        # title for the collapsed message
        _title = f"{self.summary}: {self.author}".strip()

        # Set timestamp message for it is committed
        _timestamp = f"Datetime: {self.timestamp.isoformat()}"

        # Main containts is able to show when open the collapsed message.
        _containts = f"{_timestamp}\n\n{self.message}"

        # need new line at the both start and end of message to define collect collapsed sentence.
        msg = f"{{{{collapse({_title})\n{_containts}\n}}}}"

        return msg


class GitCommit(BaseCommit):
    def __init__(self, commit: Commit) -> None:
        self.author = commit.author.name
        self.timestamp = commit.authored_datetime

        # convert to string if the type of member is bytes.
        if isinstance(commit.message, bytes):
            self.message = commit.message.decode("utf-8")
        else:
            self.message = commit.message

        if isinstance(commit.summary, bytes):
            self.summary = commit.summary.decode("utf-8")
        else:
            self.summary = commit.summary


class SvnCommit(BaseCommit):
    def __init__(self, commit: LogEntry) -> None:
        self.author = commit.author
        self.timestamp = commit.date
        self.message = commit.msg
        # The default summary is first line of the message.
        self.summary = self.message.split("\n", 1)[0]
