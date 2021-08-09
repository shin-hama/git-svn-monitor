from datetime import date
import pytest

from git_svn_monitor.core.config import env_config
from git_svn_monitor.model.redmine_client import RedmineClient


@pytest.fixture(scope="session")
def client() -> RedmineClient:
    yield RedmineClient()


@pytest.mark.internal
def test_iter_issues_is_runable(client: RedmineClient) -> None:
    for issue in client.iter_issues_filtered_by_updated_date():
        assert issue.url.startswith(env_config.redmine_url)
        break


def test__build_timestamp_condition_with_none(client: RedmineClient) -> None:
    condition = client._build_date_range()
    assert condition is None


def test__build_timestamp_condition_only_start(client: RedmineClient) -> None:
    _start = "2000-01-01"
    start = date.fromisoformat(_start)
    condition = client._build_date_range(start)
    end = date.today().isoformat()
    assert condition == f"><{_start}|{end}"
