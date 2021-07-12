from pathlib import Path

import git

from git_svn_monitor.core.config import PathLike


class GitClient():
    def __init__(self, path: PathLike):
        if Path(path).joinpath(".git").exists():
            self.repo = git.Repo(path)
        else:
            self.repo = git.Repo.init(path, mkdir=True)

    def add_remote(self, name: str, url: str):
        try:
            self.repo.create_remote(name, url=url)
        except git.GitError:
            pass

    @property
    def remotes(self):
        return self.repo.remotes
