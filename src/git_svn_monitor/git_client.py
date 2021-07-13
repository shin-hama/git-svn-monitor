from typing import Any

import git

from git_svn_monitor.core.config import PathLike


class GitClient():
    def __init__(self, path: PathLike):
        self.repo = git.Repo(path)
        # self.repo = git.Repo.init(path, mkdir=True, bare=True)

    def add_remote(self, name: str, url: str):
        try:
            self.repo.create_remote(name, url=url)
        except git.GitError:
            pass

    def iter_commits_from_branches(self, branches: Any, **kwargs):
        kwargs.setdefault("no_merges", True)
        return self.repo.iter_commits(branches, **kwargs)

    @property
    def remotes(self):
        return self.repo.remotes
