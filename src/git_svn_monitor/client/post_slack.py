from logging import getLogger

from slack_sdk import WebhookClient

from git_svn_monitor.core.config import env_config


logger = getLogger(__name__)


def send_to_slack(text: str) -> None:
    client = WebhookClient(
        url=env_config.slack_webhook_url,
        proxy=env_config.proxy
    )

    res = client.send(text=text)
    if (200 <= res.status_code < 300) is False:
        logger.error("Fail to post slack")
        logger.error(res.body)
