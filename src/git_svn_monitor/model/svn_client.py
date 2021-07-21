from typing import Any, Iterator

from svn.exception import SvnException
from svn.utility import get_client

from git_svn_monitor.core.config import PathLike


class SvnClient:
    def __init__(self, path: PathLike):
        self.repo = get_client(path)
        try:
            self.repo.info()
        except SvnException as e:
            # Raise exception if path is not collect svn repository
            raise e

    def iter_log(self, **kwargs: Any) -> Iterator[Any]:
        """ Get all commits log. You can get iterator of LogEntry instance. LogEntry has 'date',
        'msg', 'revision', 'author', 'changelist'.

        Paramters
        ---------
        timestamp_from_dt, timestamp_to_dt : datetime or None
        limit: int or None
            Maximum number of log
        rel_filepath: str
            Target branch path relational from client
        stop_on_copy: bool default is False
        revision_from, revision_to: int or str
            You can set revision number or revision alias like HEAD, BASE and more.
        changelist: bool default is False
            Show changed file if set True
        use_merge_history: bool default is False

        Return
        ------
        log_entry: Iterator[LogEntry]
            The object of commit log
        """
        return self.repo.log_default(**kwargs)
