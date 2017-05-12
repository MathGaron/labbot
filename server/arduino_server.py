import sys
sys.path.append("../")
from server.communication.usb_serial import UsbSerial
from server.communication.slack import Slack
import time
import os

SLACK_TOKEN = os.environ["LVSN_SLACK_TOKEN"]


if __name__ == '__main__':

    # Setup Arduino communication
    sending_struct = "BB"
    receiving_stuct = "BB"
    stream = UsbSerial(sending_struct, receiving_stuct)

    # Setup Slack communication
    channel = "#" + sys.argv[1]
    #todo check if channel exits
    slack = Slack(SLACK_TOKEN)

    print("USB Serial server started")
    while 1:
        messages = stream.read_data()
        for message in messages:
            if message[0]:
                slack.post_msg(channel, "Coffee is Ready! :coffee:")
            if message[1]:
                print("Button 2 Press")
        time.sleep(1)

    stream.release()
