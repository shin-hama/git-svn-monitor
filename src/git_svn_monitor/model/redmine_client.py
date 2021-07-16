from redminelib import Redmine

from git_svn_monitor.core.config import REDMINE_API_KEY


redmine = Redmine(
    "http://redmine.jeol.co.jp/",
    key=REDMINE_API_KEY,
)
project = redmine.project.get("AutomationTEM")
issue = redmine.issue.get("127163")
print(issue.url)
for j in issue.journals:
    print(j.notes)

redmine.issue.update("127163", notes="test api")
