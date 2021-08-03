""" Test only the SvnCommit class because the method is shared in base class and it is easy to init.
"""
from datetime import datetime

import pytest

from git_svn_monitor.model.commit_parser import SvnCommit
from git_svn_monitor.util.log_entry import LogEntry


@pytest.fixture
def svn_commit() -> SvnCommit:
    return SvnCommit(LogEntry(**{
        "author": "author",
        "date": datetime.now(),
        "msg": "commit messsage",
        "revision": "tA23qtUg"
    }))


def test_perse_ticket_number(svn_commit: SvnCommit) -> None:
    """ Get the number
    """
    test_num = 12345
    svn_commit.message = f"refs #{test_num} test message"
    num = svn_commit.parse_ticket_number()
    assert num == test_num


def test_perse_no_ticket_number(svn_commit: SvnCommit) -> None:
    """ Get None when parse message with no ticket number
    """
    svn_commit.message = "no ticket number"
    num = svn_commit.parse_ticket_number()
    assert num is None
