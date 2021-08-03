from collections import defaultdict
from datetime import datetime
from logging import getLogger
from typing import Dict, List

from git_svn_monitor.core.config import env_config
from git_svn_monitor.core.settings import save_settings, Settings
from git_svn_monitor.model.redmine_client import RedmineClient
from git_svn_monitor.model.manager import BaseManager, GitManager, SvnManager


logger = getLogger(__name__)


def main() -> None:
    commits = get_latest_commits()

    if env_config.debug is False:
        Settings.last_updated = datetime.now()
    save_settings()

    update_redmine(commits)


def get_latest_commits() -> Dict[int, List[str]]:
    targets: List[BaseManager] = [GitManager(), SvnManager()]
    commits_for_ticket: Dict[int, List[str]] = defaultdict(list)
    for mgr in targets:
        logger.info(f"Start parsing to {type(mgr)}")
        for commit in mgr.iter_latest_commits():
            id = commit.parse_ticket_number()
            if id is None:
                continue
            message = commit.build_message_for_redmine()
            commits_for_ticket[id].append(message)

    logger.debug(f"The number of commits: {len(commits_for_ticket)}")
    logger.debug(f"The kind of tickets: {commits_for_ticket.keys()}")
    return commits_for_ticket


def update_redmine(commits: Dict[int, List[str]]) -> None:
    redmine = RedmineClient()

    for _id, _commits in commits.items():
        summary = f"{len(_commits)} commits added from last updated"
        note = "\n\n".join([summary, *_commits])
        if env_config.debug:
            logger.debug(f"=====ticket id: {_id}=====")
            logger.debug(note)
        else:
            redmine.update_issue(_id, notes=note)


if __name__ == "__main__":
    main()
