import re

import git


class GitCommit:
    ticket_pattern = re.compile("refs #[0-9]*")

    def __init__(self, commit: git.base.Commit) -> None:
        self.commit = commit

    def parse_tickets(self) -> list[str]:
        """ Get list of all ticket number written in commit message.
        We can find to match the pattern of `refs #****`.
        """
        _message = self.commit.message
        results = self.ticket_pattern.findall(_message)
        return results

    def build_message_for_redmine(self) -> str:
        """ Build message for upload redmine.
        """
        # title for the collapsed message
        _title = f"{self.commit.summary.strip()}: {self.commit.author.name}".strip()
        # Main containts is able to show when open the collapsed message.
        _timestamp = f"Datetime: {self.commit.authored_datetime.isoformat()}"
        _containts = f"{_timestamp}\n\n{self.commit.message.strip()}"

        # need new line at the both start and end of message to define collect collapsed sentence.
        message = f"{{{{collapse({_title})\n{_containts}\n}}}}"

        return message
