"""
DOC
http://www.codingtricks.biz/slack-python-client-to-send-messages/
http://pfertyk.me/2016/11/automatically-respond-to-slack-messages-containing-specific-text/
http://stackoverflow.com/questions/37283111/cannot-post-images-to-slack-channel-via-web-hooks-utilizing-python-requests
"""

from slackclient import SlackClient
import os
import requests

filename = '~/envmap.jpg'

title = 'title'
channel = "#labbot"
text = "Hello from Python! :tada:"


class LVSN_SLACK(object):

    def __init__(self):
        SLACK_CLIENT_ID = os.environ["LVSN_CLIENT_ID"]
        SLACK_CLIENT_SECRET = os.environ["LVSN_CLIENT_SECRET"]
        SLACK_BOT_SCOPE = 'slackbot'

        SLACK_BOT_TOKEN = os.environ["LVSN_SLACK_TOKEN"]
        slack_token = SLACK_BOT_TOKEN
        self.sc = SlackClient(slack_token)

    def post_attachment(self, channel, filename, title):
        msg = self.sc.api_call(
            "files.upload",
            file=open(filename, 'rb'),
            filename=filename,
            title=title,
            channels=channel
        )
        return msg['ok']

    def post_msg(self, channel, text):
        msg = self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=text
        )
        return msg['ok']


slack = LVSN_SLACK()
slack.post_msg(channel=channel, text=text)
slack.post_attachment(channel=channel, filename=filename, title='LABBOT TEST')
