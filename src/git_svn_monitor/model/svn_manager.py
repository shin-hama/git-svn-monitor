from typing import Any, Iterator

from git_svn_monitor.core.config import SETTING_FILE
from git_svn_monitor.core.settings import load_settings
from git_svn_monitor.model.svn_client import SvnClient
from git_svn_monitor.model.commit_parser import SvnCommit


class SvnManager:
    def __init__(self) -> None:
        self.settings = load_settings(SETTING_FILE)

    def get_latest_commits(self) -> Iterator[SvnCommit]:
        """ Get all commits log that is committed by specific author for all repositories written
        in settings file
        """
        for repo in self.settings.svn_repositories:
            for log in self.iter_commits_from_last_updated(repo.url):
                if log.author == self.settings.svn_author:
                    yield SvnCommit(log)

    def iter_commits_from_last_updated(self, url: str) -> Iterator[Any]:
        client = SvnClient(url)
        args = {
            "timestamp_from_dt": self.settings.last_updated
        }

        return client.iter_log(**args)


test = SvnManager()
test.get_latest_commits()
