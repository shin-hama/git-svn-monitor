from pathlib import Path

from git_svn_monitor.core.config import TARGET_DIR
from git_svn_monitor.core.settings import load_settings
from git_svn_monitor.git_client import GitClient


def main():
    git_cli = GitClient(TARGET_DIR)

    setting_file = Path(TARGET_DIR) / "settings.json"
    settings = load_settings(setting_file)
    print(settings)
    for repo in settings.get("repositories", []):
        if repo["name"] not in git_cli.remotes:
            git_cli.add_remote(repo["name"], repo["url"].replace("\\", "/"))
        for f in git_cli.remotes[repo["name"]].fetch():
            print(f)


if __name__ == "__main__":
    main()
