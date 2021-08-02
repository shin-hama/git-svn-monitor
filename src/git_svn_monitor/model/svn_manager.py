from typing import Any, Iterator, List

from git_svn_monitor.core.config import SETTING_FILE
from git_svn_monitor.core.settings import load_settings
from git_svn_monitor.model.svn_client import SvnClient


class SvnManager:
    def __init__(self) -> None:
        self.settings = load_settings(SETTING_FILE)
        self.svn = SvnClient("")

    def get_latest_commits(self) -> List[Any]:
        commits = [
            log for log in self.iter_commits_from_last_updated() if log.author == "shamada"
        ]

        print(commits)
        return commits

    def iter_commits_from_last_updated(self) -> Iterator[Any]:
        args = {
            "timestamp_from_dt": self.settings.last_updated
        }

        return self.svn.iter_log(**args)


test = SvnManager()
test.get_latest_commits()
