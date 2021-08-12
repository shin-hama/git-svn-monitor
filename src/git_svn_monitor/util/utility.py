import os

from git_svn_monitor.core.config import env_config


def remove_proxy() -> None:
    os.environ.update({"http_proxy": ""})
    os.environ.update({"https_proxy": ""})


def setup_proxy() -> None:
    if env_config.proxy is not None:
        os.environ.update({"http_proxy": env_config.proxy})
        os.environ.update({"https_proxy": env_config.proxy})
