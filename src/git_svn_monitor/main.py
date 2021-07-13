from git_svn_monitor.git_manager import GitManager


def main() -> None:
    git = GitManager()
    git.parse_latest_commit()


if __name__ == "__main__":
    main()
