# from datetime import datetime
from typing import Any, Iterator

import git
from git.util import IterableList

from git_svn_monitor.core.config import SETTING_FILE, TARGET_DIR
from git_svn_monitor.core.settings import load_settings, save_settings
from git_svn_monitor.model.git_client import GitClient
from git_svn_monitor.model.commit_parser import GitCommit


class GitManager:
    def __init__(self) -> None:
        self.settings = load_settings(SETTING_FILE)
        self.git = GitClient(TARGET_DIR)

    def parse_latest_commit(self) -> list[GitCommit]:
        """ Get all commits after you got last time.

        Return
        ------
        commits: List of commit
            All commit information you can get.
        """
        commits = ([
            GitCommit(commit)
            for fetched in self.fetch_all_remote()
            for commit in self.iter_commits_from_last_updated(fetched)
        ])

        self.update_settings()
        return commits

    def iter_commits_from_last_updated(self, remotes: Any = None) -> Iterator[git.base.Commit]:
        """ Get all the latest commits since the last update according to the configuration file.

        Parameter
        ---------
        remotes: Any
            The information of reachable git repositories
        """
        args = {
            "author": self.settings.email,
            "after": self.settings.last_updated,
        }
        for commit in self.git.iter_commits_(remotes, **args):
            yield commit

    def fetch_all_remote(self) -> Iterator[IterableList[git.FetchInfo]]:
        """ Fetch the latest changes for all remotes specified in settings file.
        """
        for repo in self.settings.repositories:
            if repo.url == "" or repo.name == "":
                continue
            if all([repo.name != remote.name for remote in self.git.remotes]):
                self.git.add_remote(repo.name, repo.url.replace("\\", "/"))

            print(f"------{repo.name}------")
            yield self.git.fetch_remote(repo.name)

    def update_settings(self) -> None:
        """ Update last_updated timestamp and save it
        """
        # Comment out update process temporary for dev
        # self.settings.last_updated = datetime.now()
        save_settings(SETTING_FILE, self.settings)