from collections import defaultdict
from datetime import datetime
from logging import getLogger
from typing import Dict, List

from redminelib.resources import Issue

from git_svn_monitor.client.post_slack import send_to_slack
from git_svn_monitor.client.spread_seat import upload_commit
from git_svn_monitor.core.config import env_config
from git_svn_monitor.core.settings import save_settings, Settings
from git_svn_monitor.model.commit_parser import BaseCommit
from git_svn_monitor.model.redmine_client import RedmineClient
from git_svn_monitor.model.manager import BaseManager, GitManager, SvnManager
from git_svn_monitor.util import utility

logger = getLogger(__name__)


def main() -> None:
    commits = get_latest_commits()

    if env_config.debug is False:
        Settings.last_updated = datetime.now()
    save_settings()

    # Redmine is internal server, that means no need to use proxy
    utility.remove_proxy()
    updated_issues = update_redmine_issues(commits)
    utility.setup_proxy()

    # Upload to spread sheet
    if env_config.spread_sheet_key:
        for commit in commits:
            ws_url = upload_commit(commit)

    # Send updated info when setting up a slack webhook.
    if env_config.slack_webhook_url:
        if len(commits) > 0:
            sheet_result = f"Spread sheet is updated: {ws_url}"
            redmine_result = parse_redmine_result(updated_issues)
            message = f"{sheet_result}\n\n{redmine_result}"
        else:
            message = "There are no commits from last time"
        send_to_slack(message)


def get_latest_commits() -> List[BaseCommit]:
    """ Get all commits log from last executed time
    """
    targets: List[BaseManager] = [GitManager(), SvnManager()]
    commits = []
    for mgr in targets:
        logger.info(f"Start parsing to {type(mgr)}")
        for commit in mgr.iter_latest_commits():
            commits.append(commit)

    logger.debug(f"The number of commits: {len(commits)}")
    return commits


def update_redmine_issues(commits: List[BaseCommit]) -> List[Issue]:
    """ Update issues is added commits
    """
    redmine = RedmineClient()

    issues = []
    commits_per_ticket = classify_commits_by_ticket(commits)
    for _id, _commits in commits_per_ticket.items():
        summary = f"{len(_commits)} commits added from last updated"
        note = "\n\n".join([summary, *_commits])

        issue = redmine.update_issue(_id, notes=note)
        issues.append(issue)

    return issues


def classify_commits_by_ticket(commits: List[BaseCommit]) -> Dict[int, List[str]]:
    """ Classify commits by ticket id.

    Return
    ------
    commits_per_ticket: dict[int, list[str]]
        Mapping ticket id to messages committed to them
    """
    commits_per_ticket: Dict[int, List[str]] = defaultdict(list)
    for commit in commits:
        id = commit.ticket_id
        if id is None:
            continue
        message = commit.build_message_for_redmine()
        commits_per_ticket[id].append(message)

    logger.debug(f"The kind of tickets: {commits_per_ticket.keys()}")

    return commits_per_ticket


def parse_redmine_result(issues: List[Issue]) -> str:
    """ Build message to notify result of execution.
    """
    if issues == []:
        return ""
    tickets = [i.url for i in issues]

    head = "Progress on the following Issue has been described.\n"
    foot = f"\nCompleted at {datetime.now().isoformat(timespec='seconds')}"

    message = "\n".join([head, *tickets, foot])
    return message


if __name__ == "__main__":
    main()
