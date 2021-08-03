from datetime import datetime
from typing import Any, List, NamedTuple, Optional, Tuple


class LogEntry(NamedTuple):
    """ Helper class to use svn library
    """
    author: str
    date: datetime
    msg: str
    revision: str
    changelist: Optional[List[Tuple[Any]]] = None
