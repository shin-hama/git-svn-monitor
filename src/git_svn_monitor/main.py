from collections import defaultdict

from git_svn_monitor.model.git_manager import GitManager
from git_svn_monitor.model.commit_parser import build_message_for_redmine, parse_ticket_number


def main() -> None:
    git = GitManager()
    commits = git.get_latest_commits()

    commits_for_ticket: dict[str, list[str]] = defaultdict(list)
    for commit in commits:
        id = parse_ticket_number(commit.message)
        if id is None:
            continue
        commits_for_ticket[id].append(build_message_for_redmine(commit))

    for _id, _commits in commits_for_ticket.items():
        summary = f"{len(_commits)} commits added from last updated"
        result = "\n\n".join([summary, *_commits])
        print(f"=====ticket id: {_id}=====")
        print(result)


if __name__ == "__main__":
    main()
