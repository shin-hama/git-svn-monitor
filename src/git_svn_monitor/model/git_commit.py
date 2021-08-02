from git.objects import Commit


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
