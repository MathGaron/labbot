from slackclient import SlackClient
from chatterbot import ChatBot
import sys
sys.path.append("../..")
from server.communication.tasks.test_task import TestTask
from server.communication.tasks.help_task import HelpTask
from server.communication.tasks.show_last_image import ShowTask
import time
import threading
import json


def get_configurations(config_file):
    """
    Load config json from first command line argument
    :return:
    """
    with open(config_file) as data_file:
        configs = json.load(data_file)
    return configs


class Slack(object):

    def __init__(self, slack_token, config_file='configs/slack.json'):
        self.sc = SlackClient(slack_token)
        self.BOT_ID = self.get_user_id('pibot')
        config = get_configurations(config_file)
        chatbot = config['chatbot']
        #todo It should not be the Slack object that handle tasks!!!
        self.tasks = []
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

    def load_tasks(self, tasks):
        for task in tasks:
            self.tasks.append(task)

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

    def handle_command(self, channel, msg):
        """
        Receives commands directed at the bot and determines if they are valid commands.
        If so, then acts on the commands. Else, forward the command to the chatbot.
        Add more commands in the Instruction dict
        """
        return_message = None
        for task in self.tasks:
            if task.trigger(msg):
                return_message = task.callback(self, channel)
                break
        if not return_message:
            return_message = self.chat(msg)

        self.post_msg(channel, return_message)


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
    slack = Slack(SLACK_TOKEN, config_file='../configs/slack.json')

    # Setup tasks
    test_task = TestTask()
    still_plant_task = ShowTask("plant", "/home/pi/timelaps_plant_2017")
    help_task = HelpTask([test_task, still_plant_task])
    slack.load_tasks([test_task, help_task, still_plant_task])

    slack.start_monitor()


if __name__ == '__main__':
    tester()
