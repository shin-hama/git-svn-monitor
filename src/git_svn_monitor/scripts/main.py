from collections import defaultdict
from datetime import datetime
import logging
from typing import Dict, List

from git_svn_monitor.core.config import env_config
from git_svn_monitor.core.settings import save_settings, Settings
from git_svn_monitor.model.redmine_client import RedmineClient
from git_svn_monitor.model.manager import BaseManager, GitManager, SvnManager


logger = logging.getLogger(__name__)


def main() -> None:
    targets: List[BaseManager] = [GitManager(), SvnManager()]
    commits_for_ticket: Dict[int, List[str]] = defaultdict(list)
    for mgr in targets:
        for commit in mgr.iter_latest_commits():
            id = commit.parse_ticket_number()
            if id is None:
                continue
            message = commit.build_message_for_redmine()
            commits_for_ticket[id].append(message)

    if env_config.debug is False:
        Settings.last_updated = datetime.now()
    save_settings()

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
