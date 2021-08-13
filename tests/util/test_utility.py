import os

from git_svn_monitor.core.config import env_config
from git_svn_monitor.util import utility


def test_setup_proxy() -> None:
    utility.setup_proxy()
    assert os.environ.get("http_proxy") == env_config.proxy
    assert os.environ.get("https_proxy") == env_config.proxy


def test_remove_proxy() -> None:
    utility.remove_proxy()
    assert os.environ.get("http_proxy") == ""
    assert os.environ.get("https_proxy") == ""
