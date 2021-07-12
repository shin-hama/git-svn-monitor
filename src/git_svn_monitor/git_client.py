import os
from pathlib import Path
from typing import Optional, Union

import git


PathLike = Union[str, 'os.PathLike[str]']


class Client():
    def __init__(self, path: PathLike):
        if Path(path).exists():
            self.repo = git.Repo(path)
        else:
            self.repo = git.Repo.init(path, mkdir=True)

    def _add_remote(self, name: str, url: str):
        try:
            self.repo.create_remote(name, url=url)
        except git.GitError:
            pass

    @property
    def remotes(self):
        return self.repo.remotes


target = Path(r"D:\workspace\hamada\test_python")

remote_path = r"\\mnemosyne\EMSYS\Users\Hamada\git\lamella_image_builder.git"
remote_path = remote_path.replace("\\", "/")
git_cli = Client(target)

name = "origin"
if name not in git_cli.remotes:
    print("no remote")
    git_cli._add_remote(name, remote_path)
for remote in git_cli.remotes:
    print(remote)
    for b in remote.fetch():
        print(b)
