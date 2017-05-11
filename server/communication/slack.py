"""
DOC
http://www.codingtricks.biz/slack-python-client-to-send-messages/
http://pfertyk.me/2016/11/automatically-respond-to-slack-messages-containing-specific-text/
http://stackoverflow.com/questions/37283111/cannot-post-images-to-slack-channel-via-web-hooks-utilizing-python-requests
"""

from slackclient import SlackClient


class Slack(object):
    def __init__(self, slack_token):
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
