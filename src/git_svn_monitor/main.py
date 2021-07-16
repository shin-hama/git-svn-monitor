from git_svn_monitor.model.git_manager import GitManager


def main() -> None:
    git = GitManager()
    commits = git.parse_latest_commit()

    comment = f"{len(commits)} commits added from {git.settings.last_updated}"
    commit_messages = [c.build_message_for_redmine() for c in commits]

    result = "\n\n".join([comment, *commit_messages])
    print(result)


if __name__ == "__main__":
    main()
