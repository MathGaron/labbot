import sys
sys.path.append("../")
from server.communication.slack import Slack
from server.indexer import Indexer
import os
import json

SLACK_TOKEN = os.environ["LVSN_SLACK_TOKEN"]


def get_configurations():
    """
    Load config json from first command line argument
    :return:
    """
    config_file = sys.argv[1]
    with open(config_file) as data_file:
        configs = json.load(data_file)
    return configs

if __name__ == '__main__':
    configs = get_configurations()
    path = configs["data_folder"]
    last = Indexer.get_last_tag_from_folder(path)
    last_date = Indexer.tag_to_date(last)
    channel = "#labbot"

    slack = Slack(SLACK_TOKEN)
    slack.post_attachment(channel=channel, filename=os.path.join(path, last + ".jpg"), title=str(last_date))