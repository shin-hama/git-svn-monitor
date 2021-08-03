from datetime import datetime
from typing import Any


class SvnCommit(object):
    def __init__(self, commit: Any) -> None:
        self.author: str = commit.author
        self.timestamp: datetime = commit.date
        self.message: str = commit.msg
        # The default summary is first line of the message.
        self.summary: str = self.message.split("\n", 1)[0]
