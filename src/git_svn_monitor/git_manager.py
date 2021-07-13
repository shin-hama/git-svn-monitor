from typing import Any, Iterator
import git
from git.util import IterableList

from git_svn_monitor.core.config import SETTING_FILE, TARGET_DIR
from git_svn_monitor.core.settings import load_settings
from git_svn_monitor.git_client import GitClient


class GitManager:
    def __init__(self) -> None:
        self.settings = load_settings(SETTING_FILE)
        self.git = GitClient(TARGET_DIR)

    def parse_latest_commit(self) -> list[Any]:
        results = []
        for fetched in self.fetch_all_remote():
            print(fetched)
            results.extend([
                commit.message
                for commit in self.iter_commits_from_last_updated(fetched)
            ])
        return results

    def iter_commits_from_last_updated(self, remote: Any = None) -> Iterator[git.base.Commit]:
        """ Get all the latest commits since the last update according to the configuration file.
        """
        args = {
            "author": self.settings.author,
            "after": self.settings.last_updated,
        }
        for commit in self.git.iter_commits_(remote, **args):
            yield commit

    def fetch_all_remote(self) -> Iterator[IterableList[git.FetchInfo]]:
        """ Fetch the latest changes for all remotes specified in settings file.
        """
        for repo in self.settings.repositories:
            if all([repo.name == remote.name for remote in self.git.remotes]):
                self.git.add_remote(repo.name, repo.url.replace("\\", "/"))

            print(f"------{repo.name}------")
            yield self.git.fetch_remote(repo.name)


test = GitManager().parse_latest_commit()
print(test)
