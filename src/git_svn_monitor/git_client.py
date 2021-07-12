from pathlib import Path

import git

target = Path(r"D:\workspace\hamada\test_python")
repo = git.Repo.init(target, mkdir=True)

print([r for r in repo.remotes])
if repo.remotes:
    origin = repo.remotes.origin
else:
    remote_path = r"https://github.com/shin-hama/git-svn-monitor.git"
    origin = repo.create_remote("origin", url=remote_path)
fetch = origin.fetch()
for i in fetch:
    print(i)
