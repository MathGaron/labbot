from server.communication.usb_serial import UsbSerial


if __name__ == '__main__':
    sending_struct = "if"
    receiving_stuct = "if"
    stream = UsbSerial(sending_struct, receiving_stuct)
    print("USB Serial server started")
    while 1:
        print(stream.read_data())
        time.sleep(1)

    stream.release()
