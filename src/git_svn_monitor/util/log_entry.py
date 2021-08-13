from datetime import datetime
from typing import Any, List, NamedTuple, Optional, Tuple


class LogEntry(NamedTuple):
    """ Helper class to use svn library
    """
    author: Optional[str]
    date: Optional[datetime]
    msg: Optional[str]
    revision: int
    changelist: Optional[List[Tuple[Any]]] = None
