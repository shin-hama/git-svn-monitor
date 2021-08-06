from datetime import date, datetime
import pytest

from git_svn_monitor.core.config import TIMESTAMP_FORMAT, env_config
from git_svn_monitor.model.redmine_client import RedmineClient


@pytest.fixture(scope="session")
def client() -> RedmineClient:
    yield RedmineClient()


def test_iter_issues_is_runable(client: RedmineClient) -> None:
    for issue in client.iter_issues_filtered_by_updated_date():
        assert issue.url.startswith(env_config.redmine_url)
        break


def test__build_timestamp_condition_with_none(client: RedmineClient) -> None:
    condition = client._build_timestamp_condition()
    assert condition == ""


def test__build_timestamp_condition_only_start(client: RedmineClient) -> None:
    _start = "2000-01-01"
    start = date(_start, "%Y-%m-%d")
    condition = client._build_timestamp_condition(start)
    end = datetime.today().date().strftime("%Y-%m-%d")
    assert condition == f"><{_start}|{end}"
