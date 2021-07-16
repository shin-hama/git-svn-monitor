from git_svn_monitor.model.git_manager import GitManager


def main() -> None:
    git = GitManager()
    test = git.parse_latest_commit()
    for t in test:
        t.parse_tickets()


if __name__ == "__main__":
    main()
