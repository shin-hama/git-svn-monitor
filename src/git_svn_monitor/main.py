from git_svn_monitor.git.git_manager import GitManager


def main() -> None:
    git = GitManager()
    test = git.parse_latest_commit()
    print(test)


if __name__ == "__main__":
    main()
