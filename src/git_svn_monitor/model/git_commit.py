from git.objects import Commit

from git_svn_monitor.model.commit_parser import build_message_for_redmine, parse_ticket_number


class GitCommit(object):
    def __init__(self, commit: Commit) -> None:
        self.author = commit.author.name
        self.timestamp = commit.authored_datetime

        # convert to string if the type of member is bytes.
        self.message = commit.message
        if isinstance(self.message, bytes):
            self.message = self.message.decode("utf-8")

        self.summary = commit.summary
        if isinstance(self.summary, bytes):
            self.summary = self.summary.decode("utf-8")
