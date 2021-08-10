from logging import getLogger

from slack_sdk import WebhookClient

from git_svn_monitor.core.config import env_config


logger = getLogger(__name__)


def send_to_slack(text: str) -> None:
    if env_config.slack_webhook_url is None:
        return
    client = WebhookClient(
        url=env_config.slack_webhook_url,
        proxy=env_config.proxy
    )

    head = "*Automatic posting from git_svn_progress_monitor*"
    _text = f"{head}\n\n{text}"

    res = client.send(text=_text)
    if (200 <= res.status_code < 300) is False:
        logger.error("Fail to post slack")
        logger.error(res.body)
