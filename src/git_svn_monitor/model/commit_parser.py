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
