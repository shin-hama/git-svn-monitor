from collections import defaultdict
from typing import Dict, List

from git_svn_monitor.core.config import env_config
from git_svn_monitor.model.git_manager import GitManager
from git_svn_monitor.model.redmine_client import RedmineClient


def main() -> None:
    git = GitManager()
    commits = git.get_latest_commits()

    commits_for_ticket: Dict[str, List[str]] = defaultdict(list)
    for commit in commits:
        id = commit.parse_ticket_number()
        if id is None:
            continue
        message = commit.build_message_for_redmine()
        commits_for_ticket[id].append(message)

    redmine = RedmineClient()

    for _id, _commits in commits_for_ticket.items():
        summary = f"{len(_commits)} commits added from last updated"
        note = "\n\n".join([summary, *_commits])
        if env_config.debug:
            print(f"=====ticket id: {_id}=====")
            print(note)
        else:
            redmine.update_issue(_id, notes=note)


if __name__ == "__main__":
    main()
