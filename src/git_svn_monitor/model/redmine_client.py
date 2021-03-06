from datetime import datetime
from logging import getLogger
from typing import Any, Iterator, Optional, Union

from redminelib import Redmine, resources

from git_svn_monitor.core.config import env_config, DateLike


logger = getLogger(__name__)


class RedmineClient:
    def __init__(self) -> None:
        self.redmine = Redmine(
            url=env_config.redmine_url,
            key=env_config.redmine_api_key,
        )

    def update_issue(self, ticket_id: Union[int, str], **kwargs: Any) -> resources.Issue:
        """ Update issue for specified ticket.

        Parameters
        ----------
        The parameter name of kwargs as below.
        - subject (string): Issue subject
        - description (string): Issue description
        - notes (string): journal note that is called as history
        - parent_issue_id (int): Parent issue id.
        - done_ratio (int): Issue done ratio.

        Return
        ------
        issue: redminelib.resources.Issue
            The updated issue
        """
        if env_config.debug:
            logger.debug(f"Update: #{ticket_id}, kwargs: {kwargs}")
        else:
            self.redmine.issue.update(ticket_id, **kwargs)

        issue = self.redmine.issue.get(ticket_id)

        return issue

    def iter_issues_filtered_by_updated_date(
        self,
        start: DateLike = None,
        end: DateLike = None,
        **kwargs: Any,
    ) -> Iterator[resources.Issue]:
        """ Get the issues that were updated in the specified period for current session user.

        Parameters
        ----------
        start: str, date or None default is None
            start date to filter. If this is None, you can get all issues.
        end: str, date or None default is None
            end date to filter. If this is None, you can get up to today.

        Return
        ------
        issues:  Iterator of redminelib.resources.Issue
            The iterator of issues between start and end.
        """
        logger.info("Get issues")
        filter = kwargs

        updated_on = self._build_date_range(start, end)
        # updated_on will be not set when timestamp condition is empty
        if updated_on:
            filter["updated_on"] = updated_on

        u = self.redmine.user.get("current")
        logger.debug(f"user_id: {u.id}, fileter: {filter}")

        iterator = self.redmine.issue.filter(assigned_to_id=u.id, **filter)
        for issue in iterator:
            yield issue

    def _build_date_range(self, start: DateLike = None, end: DateLike = None) -> Optional[str]:
        condition = None
        if start is not None:
            if end is None:
                end = datetime.today().date()
            condition = f"><{start}|{end}"

        return condition
