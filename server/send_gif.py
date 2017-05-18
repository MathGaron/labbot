import sys
import warnings
if sys.version_info < (3,0):
    warnings.warn("this code can only run with python3 or higher!")
sys.path.append("../")

from server.communication.slack import Slack
from server.indexer import Indexer
from subprocess import call
import os
import json


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

    begin_interval="**13***"
    end_interval="**15***"
    get_interval = Indexer.get_dates_between_interval(path,begin_interval,end_interval)
    
    call_command = 'convert '
    for item in get_interval:
        call_command += path+'/'+item+'.jpg'+' '

    call_command += 'gif.gif'
        
    call(call_command.split(' '))

    channel = "#labbot"
    slack = Slack(SLACK_TOKEN)
    slack.post_attachment(channel=channel, filename=os.path.join("gif.gif"), title=str(begin_interval+end_interval))

    call("rm", "gif.gif")

