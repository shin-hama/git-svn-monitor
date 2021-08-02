from typing import Any, Iterator, List

from git_svn_monitor.core.config import SETTING_FILE
from git_svn_monitor.core.settings import load_settings
from git_svn_monitor.model.commit_parser import build_message_for_redmine, parse_ticket_number
from git_svn_monitor.model.svn_client import SvnClient


class SvnManager:
    def __init__(self) -> None:
        self.settings = load_settings(SETTING_FILE)

    def get_latest_commits(self) -> List[Any]:
        """ Get all commits log for all repositories written in settings file
        """
        commits = [
            log
            for repo in self.settings.svn_repositories
            for log in self.iter_commits_from_last_updated(SvnClient(repo.url))
            if log.author == "hamada"
        ]

        print(commits)
        return commits

    def iter_commits_from_last_updated(self, client: SvnClient) -> Iterator[Any]:
        args = {
            "timestamp_from_dt": self.settings.last_updated
        }

        return client.iter_log(**args)

    def _parse_commit(self, commit: Any):
        id = parse_ticket_number(commit.msg)
        msg = build_message_for_redmine()


test = SvnManager()
test.get_latest_commits()
