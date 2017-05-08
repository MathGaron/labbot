"""
DOC
http://www.codingtricks.biz/slack-python-client-to-send-messages/
http://pfertyk.me/2016/11/automatically-respond-to-slack-messages-containing-specific-text/
http://stackoverflow.com/questions/37283111/cannot-post-images-to-slack-channel-via-web-hooks-utilizing-python-requests
"""

from slackclient import SlackClient
import os

SLACK_CLIENT_ID = os.environ["LVSN_CLIENT_ID"]
SLACK_CLIENT_SECRET = os.environ["LVSN_CLIENT_SECRET"]
SLACK_BOT_SCOPE = 'slackbot'
SLACK_BOT_TOKEN = os.environ["LVSN_SLACK_TOKEN"]

slack_token = SLACK_BOT_TOKEN
sc = SlackClient(slack_token)

sc.api_call(
    "chat.postMessage",
    channel="#labbot",
    text="Hello from Python! :tada:"
)