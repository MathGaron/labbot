from server.communication.tasks.task_base import TaskBase
from server.indexer import Indexer
import os


class ShowTask(TaskBase):
    def __init__(self, image_name, folder_path):
        self.image_name = image_name
        self.path = folder_path

    def trigger(self, msg):
        tokens = msg.split(" ")
        return tokens[0] == "show" and tokens[1] == self.image_name

    def callback(self, slack, channel):
        last = Indexer.get_last_tag_from_folder(self.path)
        last_date = Indexer.tag_to_date(last)
        slack.post_attachment(channel=channel, filename=os.path.join(self.path, last + ".jpg"), title=str(last_date))

    def name(self):
        return "Show {}".format(self.image_name)

    def help(self):
        return "show {} [...]".format(self.image_name), "Send {} picture to slack".format(self.image_name)