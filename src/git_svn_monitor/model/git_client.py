from logging import getLogger
from typing import Any, Iterator, Optional

import git
from git.objects import Commit
from git.util import IterableList

from git_svn_monitor.core.config import PathLike


logger = getLogger(__name__)


class GitClient():
    def __init__(self, path: PathLike) -> None:
        try:
            self.repo = git.Repo(path)
            if self.repo.bare is False:
                msg = f"{path} is not bare repository, please use other repository"
                logger.error(msg)
                raise Exception(msg)
        except git.GitError:
            logger.info(f"{path} is not git repository, create new one.")
            self.repo = git.Repo.init(path, mkdir=True, bare=True)
        logger.info(f"Git client: {path}")

    def add_remote(self, name: str, url: str) -> None:
        """ Add remote repository. Skip to process if already exists same name
        """
        try:
            self.repo.create_remote(name, url=url)
            logger.info("Add new remote repository")
            logger.info(f"name: {name}, url: {url}")
        except git.GitError as e:
            logger.warning(e)
            logger.warning(f"Fail to add remote for {name}.")
            pass

    def delete_remote(self, remote: git.Remote) -> None:
        """
        """
        try:
            self.repo.delete_remote(remote)
        except git.GitError as e:
            logger.warning(e)
            logger.warning(f"Fail to delete remote for {remote}.")
            pass

    def set_url(self, remote_name: str, new: str, old: Optional[str] = None) -> None:
        """ Set url to specified remote. Remove old url when set old.
        """
        self.remotes[remote_name].set_url(new, old)

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
        logger.info("Get commits")
        logger.debug(f"revision: {[r.ref for r in rev]}, kwargs: {kwargs}")
        kwargs.setdefault("no_merges", True)
        return self.repo.iter_commits(rev, **kwargs)

    @property
    def remotes(self) -> IterableList[git.Remote]:
        return self.repo.remotes
