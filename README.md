# git-svn-monitor

Monitor git and svn log to make progress report

## PySvn

PySvn is wrapper module of svn cli.
You have to install cli before use it.
If you haven't installed it yet, you can do so automatically by selecting the additional installation of the CLI when you install `TortoiseSVN`.
If you have already installed, you can get manually by below steps.

1. Go to [https://www.visualsvn.com/downloads/]
2. Download Apache Subversion command line tools
3. Extract zip file
4. Add the path for bin directory in extracted file to `PATH`.

## Slack sdk

The python sdk for slack api.
This package use [slack webhook](https://slack.com/intl/ja-jp/help/articles/115005265063-Slack-%E3%81%A7%E3%81%AE-Incoming-Webhook-%E3%81%AE%E5%88%A9%E7%94%A8) to post result of execution.

### How to use

1. Slack app settings ページを開く.
   * Open [here](https://api.slack.com/apps)
2. `Create New App` ボタンをクリック
   1. From scratch を選択
   2. 名前とワークスペースを選択して作成
3. 初期設定画面で `Add features and functionality` の `Incoming Webhooks` を選択
4. `Activate` を ON にして下の方にある `Add New Webhook to Workspace` をクリック
5. 自動投稿を行いたいチャンネルを選択
6. 生成された URL をコピーしておく
7. `Python` 用の Slack SDK をインストール
   1. `> pip install slack-sdk`
8. コピーした URL を使って Client インスタンスを立ち上げメッセージを送信する

``` Python
client = WebhookClient(
    url="https://your-slack-webhook-url",
)

response= client.send(text=text)
```

The variant of slack webhook url is defined in `.env` file.
You can send the running result of this package when you set url in `.env`.
