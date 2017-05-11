import sys
sys.path.append("../")
from server.communication.usb_serial import UsbSerial
import time

if __name__ == '__main__':
    sending_struct = "BB"
    receiving_stuct = "BB"
    stream = UsbSerial(sending_struct, receiving_stuct)
    print("USB Serial server started")
    while 1:
        messages = stream.read_data()
        for message in messages:
            if message[0]:
                print("Button 1 Press")
            if message[1]:
                print("Button 2 Press")
        time.sleep(1)

    stream.release()
