from redminelib import Redmine

from git_svn_monitor.core.config import REDMINE_API_KEY


redmine = Redmine(
    "http://redmine.jeol.co.jp/",
    key=REDMINE_API_KEY,
)
project = redmine.project.get("AutomationTEM")

print(project.url)
