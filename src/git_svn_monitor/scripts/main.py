from collections import defaultdict
from datetime import datetime
from logging import getLogger
from typing import Dict, List

from redminelib.resources import Issue

from git_svn_monitor.client.post_slack import send_to_slack
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

    updated_issues = update_redmine(commits)

    # Send updated info when setting slack webhook.
    if env_config.slack_webhook_url and len(updated_issues) > 0:
        message = build_message(updated_issues)
        send_to_slack(message)


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


def update_redmine(commits: Dict[int, List[str]]) -> List[Issue]:
    redmine = RedmineClient()

    issues = []
    for _id, _commits in commits.items():
        summary = f"{len(_commits)} commits added from last updated"
        note = "\n\n".join([summary, *_commits])

        issue = redmine.update_issue(_id, notes=note)
        issues.append(issue)

    return issues


def build_message(issues: List[Issue]) -> str:
    tickets = [i.url for i in issues]

    head = "Progress on the following Issue has been described.\n"
    foot = f"\nCompleted at {datetime.now().isoformat(timespec='seconds')}"

    message = "\n".join([head, *tickets, foot])
    return message


if __name__ == "__main__":
    main()
