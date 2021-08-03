import logging
import logging.handlers

from git_svn_monitor.core.config import env_config, LOG_FILE


def setup_logger(name: str) -> None:
    """ Setup logging config

    Parameter
    ---------
    name: str
        The logger name, expected root package name.
        ex) Call from __init__.py at the root of this package as `setup_logger(__name__)`.
    """
    logger = logging.getLogger(name)
    if env_config.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    # set limits to 1MB
    max_bytes = 1024*1024
    fh = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=max_bytes, backupCount=5, encoding="utf-8"
    )
    sh = logging.StreamHandler()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
