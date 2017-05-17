"""
DOC
http://www.codingtricks.biz/slack-python-client-to-send-messages/
http://pfertyk.me/2016/11/automatically-respond-to-slack-messages-containing-specific-text/
http://stackoverflow.com/questions/37283111/cannot-post-images-to-slack-channel-via-web-hooks-utilizing-python-requests
"""

from slackclient import SlackClient
from chatterbot import ChatBot
import time
import threading


class Slack(object):

    def __init__(self, slack_token, chatbot=True):
        self.sc = SlackClient(slack_token)
        self.BOT_ID = self.get_user_id('pibot')

        # Create a new chat bot named labbot
        if chatbot:
            self.chatbot = ChatBot('labbot',
                                   trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
                                   storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
                                   silence_performance_warning=True,  # MongoDatabaseAdapter might be faster
                                   logic_adapters=[
                                       "chatterbot.logic.MathematicalEvaluation",
                                       "chatterbot.logic.TimeLogicAdapter",
                                       "chatterbot.logic.BestMatch"],
                                   database="../chatbot_database.db")  # gender: AI
            self.chatbot.train("chatterbot.corpus.english")
        else:
            self.chatbot = None

    def post_attachment(self, channel, filename, title):
        '''
        Push #file to #channel or @user
        usage: post_attachement('#labbot', 'abc.txt', 'test')
        '''
        msg = self.sc.api_call(
            "files.upload",
            file=open(filename, 'rb'),
            filename=filename,
            title=title,
            channels=channel
        )
        return msg['ok']

    def post_msg(self, channel, text):
        '''
        Send message to #channel or @user
        usage: post_msg('@slackbot', 'hello')
        '''
        msg = self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=text
        )
        return msg['ok']

    def get_user_id(self, name):
        api_call = self.sc.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == name:
                    user_id = user.get('id')
                    print("ID for '" + user['name'] + "' is " + user_id)
                    return user_id
        else:
            print("could not find user with the name " + name)
            return None

    def chat(self, msg='who are you?'):
        # Get a response to the input text 'How are you?'
        if self.chatbot:
            response = self.chatbot.get_response(msg)
        else:
            response = 'I do not know what you are talking about.'
        return str(response)

    def handle_command(self, channel, command):
        """
        Receives commands directed at the bot and determines if they are valid commands.
        If so, then acts on the commands. Else, forward the command to the chatbot.
        Add more commands in the Instruction dict
        """
        Instructions = {'do': "I am lazy! Ask @mathieu. :p",
                        'hello': "Hello again.",
                        'chatoff': 'I am pibot, give me command.',
                        'lovemathieu': "I love you too.",
                        'loveherique': "I love you too.",
                        'nice': "You too.",
                        'help': 'Get this help msg.'}

        help_msg = "Not sure what you mean. Use the following commands *%s*, delimited by spaces." % (' '.join(Instructions))

        cmds = []
        for key, value in Instructions.items():
            cmds.append(key)

        cmd_instruction = [Instructions[cmd] for cmd in cmds if command.startswith(cmd)]

        if cmd_instruction:
            if cmd_instruction[0] == 'help':
                response = help_msg
            else:
                response = cmd_instruction[0]
        else:
            msg = command  # msg = ' '.join(command.split(' ')[0:])  # parameters without cmd
            response = self.chat(msg)

        self.post_msg(channel, response)

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        # constants
        AT_BOT = "<@" + self.BOT_ID + ">"
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                        output['channel']
        return None, None

    def start_monitor(self):
        '''
        Listen the messaging channel via the RTM api
        '''
        READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading

        def _auto(me):
            while True:
                command, channel = self.parse_slack_output(self.sc.rtm_read())
                if command and channel:
                    self.handle_command(channel, command)
                time.sleep(READ_WEBSOCKET_DELAY)

        if self.sc.rtm_connect():
            print("Bot connected and running!")
            thread = threading.Thread(target=_auto, args=(self,))
            thread.start()
        else:
            print("Connection failed. Invalid Slack token or bot ID?")


def tester():
    import os
    SLACK_TOKEN = os.environ["LVSN_SLACK_TOKEN"]
    channel = "#labbot"
    slack = Slack(SLACK_TOKEN)
    slack.start_monitor()
    # slack.chat()
    # slack.chat('Good morning! How are you doing?')

    # slack.post_attachment(channel=channel, filename='', title=str(last_date))


if __name__ == '__main__':
    tester()
