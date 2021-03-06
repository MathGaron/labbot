import sys
sys.path.append("../")
from server.communication.usb_serial import UsbSerial
from server.communication.slack import Slack
import time
import os

SLACK_TOKEN = os.environ["LVSN_SLACK_TOKEN"]


if __name__ == '__main__':

    # Setup Arduino communication
    # struct : {uint8, uint8, uint16} : button0, button1, moisture sensor
    sending_struct = "BBH"
    receiving_stuct = "BBH"
    stream = UsbSerial(sending_struct, receiving_stuct)

    # Setup Slack communication
    channel = "#" + sys.argv[1]
    print("Will send to channel : {}".format(channel))
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
            print("moisture : {}".format(message[2]))
        time.sleep(1)

    stream.release()
