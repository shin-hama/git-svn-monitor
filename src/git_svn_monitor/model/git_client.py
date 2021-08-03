from typing import Any, Iterator

import git
from git.objects import Commit
from git.util import IterableList

from git_svn_monitor.core.config import PathLike


class GitClient():
    def __init__(self, path: PathLike) -> None:
        try:
            self.repo = git.Repo(path)
            if self.repo.bare is False:
                raise Exception(f"{path} is not bare repository, please set other")
        except git.GitError:
            self.repo = git.Repo.init(path, mkdir=True, bare=True)

    def add_remote(self, name: str, url: str) -> None:
        """ Add remote repository. Skip to process if already exists same name
        """
        try:
            self.repo.create_remote(name, url=url)
        except git.GitError:
            pass

    def fetch_remote(self, remote: str = "origin") -> IterableList[git.FetchInfo]:
        """ Fetch the latest changes for all branch of specified remote.

        Parameter
        ---------
        remote: str default is "origin"
            The name of remote repository specified with git.

        Return
        ------
        fetch_info: IterableList[git.FetchInfo]
            The latest changes for all branches.
        """
        return self.repo.remotes[remote].fetch(prune=True)

    def iter_commits_(self, rev: Any, **kwargs: Any) -> Iterator[Commit]:
        """ Get all commits, merge commit is ignored by default.

        Parameters
        ----------
        rev : Any
            Revision info to get commits
        """
        kwargs.setdefault("no_merges", True)
        return self.repo.iter_commits(rev, **kwargs)

    @property
    def remotes(self) -> IterableList[git.FetchInfo]:
        return self.repo.remotes
