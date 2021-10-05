from logging import getLogger
from typing import Any, Iterator, Tuple

import git
from git.objects import Commit
from git.util import IterableList

from git_svn_monitor.core.config import GIT_LOCAL_REPOSITORY
from git_svn_monitor.core.settings import Setting
from git_svn_monitor.model.git_client import GitClient
from git_svn_monitor.model.svn_client import SvnClient
from git_svn_monitor.model.commit_parser import BaseCommit, GitCommit, SvnCommit
from git_svn_monitor.util.log_entry import LogEntry


logger = getLogger(__name__)


class BaseManager(object):
    def __init__(self, settings: Setting) -> None:
        self.settings = settings

    def iter_latest_commits(self) -> Iterator[BaseCommit]:
        raise NotImplementedError


class GitManager(BaseManager):
    def __init__(self, settings: Setting) -> None:
        super().__init__(settings)
        self.git = GitClient(GIT_LOCAL_REPOSITORY)

    def iter_latest_commits(self) -> Iterator[GitCommit]:
        """ Get all commits after you got last time.

        Return
        ------
        commits: List of commit
            All commit information you can get.
        """
        for fetched, repo_name in self.fetch_all_remote():
            for commit in self.iter_commits_from_last_updated(fetched):
                yield GitCommit(commit, repo_name)

        repos = [repo.name for repo in self.settings.git_repositories]
        removed_remotes = [remote for remote in self.git.remotes if remote.name not in repos]
        for remote in removed_remotes:
            self.git.delete_remote(remote)

    def iter_commits_from_last_updated(self, remotes: Any = None) -> Iterator[Commit]:
        """ Get all the latest commits since the last update according to the configuration file.

        Parameter
        ---------
        remotes: Any
            The information of reachable git repositories
        """
        args = {
            "author": self.settings.git_author,
            "after": self.settings.last_updated,
        }
        logger.info(f"Git log condition: {args}")
        return self.git.iter_commits_(remotes, **args)

    def fetch_all_remote(self) -> Iterator[Tuple[IterableList[git.FetchInfo], str]]:
        """ Fetch the latest changes for all remotes specified in settings file.
        """
        for repo in self.settings.git_repositories:
            if repo.url == "" or repo.name == "":
                logger.warning("repo has no information to fetch")
                continue
            logger.info(f"Fetch to: {repo}")

            new_url = repo.url.replace("\\", "/")
            if all([repo.name != remote.name for remote in self.git.remotes]):
                logger.info(f"Add new remote: {repo}")
                self.git.add_remote(repo.name, new_url)

            current_url = self.git.remotes[repo.name].urls.__next__()
            if new_url != current_url:
                self.git.set_url(repo.name, new_url, current_url)

            yield self.git.fetch_remote(repo.name), repo.name


class SvnManager(BaseManager):
    def __init__(self, settings: Setting) -> None:
        super().__init__(settings)

    def iter_latest_commits(self) -> Iterator[SvnCommit]:
        """ Get all commits log that is committed by specific author for all repositories written
        in settings file

        Return
        ------
        SvnCommit: SvnCommit
            Commit log data is wrapped BaseCommit class
        """
        for repo in self.settings.svn_repositories:
            logger.info(f"Fetch to: {repo}")
            for log in self.iter_commits_from_last_updated(repo.url):
                if log.author == self.settings.svn_author:
                    yield SvnCommit(log, repo.name)

    def iter_commits_from_last_updated(self, url: str) -> Iterator[LogEntry]:
        """ Get all commit log from last time you accessed.

        Parameter
        ---------
        url: str
            The repository url to get commit log.

        Return
        ------
        SvnClient.iter_log(): Iterator[LogEntry]
            Commit log from svn client
        """
        client = SvnClient(url)
        args = {
            "timestamp_from_dt": self.settings.last_updated
        }

        return client.iter_log(**args)
