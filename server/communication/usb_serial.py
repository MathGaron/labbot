import serial
import glob
import sys
import struct
import time
import threading


class UsbSerial:
    def __init__(self, send_payload_type, receive_payload_type, port='', baud=115200, async=True):
        self.send_payload_type = send_payload_type
        self.send_payload_size = struct.calcsize(self.send_payload_type)
        self.receive_payload_type = receive_payload_type
        self.receive_payload_size = struct.calcsize(self.receive_payload_type)
        self.shadow_buffer = ""
        available_ports = UsbSerial.list_ports()
        if len(available_ports) == 0:
            raise IOError('No available serial port found.')
        if port == '':
            port = available_ports[0]
        if port not in available_ports:
            raise IOError('Selected port : ' + port + " is not available.")
        self.serial_stream = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        if not self.serial_stream.isOpen():
            raise IOError("Unable to open port " + port)
        time.sleep(2)  # Here we wait for the arduino to boot properly

        self.receive_buffer = []
        self.mutex = threading.Lock()
        self.is_active = async
        self.io_thread = threading.Thread(target=self.receive_data_thread_)
        if async:
            self.io_thread.start()

    def receive_data_thread_(self):
        while self.is_active:
            msg = self.receive_data_()
            if msg:
                with self.mutex:
                    self.receive_buffer.append(msg)

    def receive_data_(self):
        ret = None
        val = self.read_data_(1)
        if hex(ord(val)) == hex(0x06):
            val = self.read_data_(1)
            if hex(ord(val)) == hex(0x85):
                size = ord(self.read_data_(1))
                payload = self.read_data_(size)
                CS = ord(self.read_data_(1))
                if self.packet_sanity_check(payload, CS, self.receive_payload_size):
                    ret = struct.unpack(self.receive_payload_type, payload)
        return ret

    def read_data(self):
        """
        Will read from the async buffer and return a list of messages
        """
        with self.mutex:
            copy = list(self.receive_buffer)
            self.receive_buffer = []
        return copy

    def send_data(self, data_tuple):
        if len(data_tuple) != len(self.send_payload_type):
            raise TypeError("Input data tuple must have lenght " + str(len(self.send_payload_type)))

        self.serial_stream.write(chr(0x06))
        self.serial_stream.write(chr(0x85))
        payload = struct.pack(self.send_payload_type, *data_tuple)
        self.serial_stream.write(chr(len(payload)))
        CS = len(payload)
        for value in payload:
            self.serial_stream.write(value)
            CS ^= ord(value)
        self.serial_stream.write(chr(CS))

    def packet_sanity_check(self, payload, truth_CS, truth_size):
        # Todo Handle error gracefully
        if len(payload) != truth_size:
            print("Payload size (" + str(len(payload)) + ") != structure lenght (" + str(truth_size) + ").")
            return False
        if truth_CS != UsbSerial.compute_CS(payload):
            print("Bad checksum")
            return False
        return True

    def flush_shadow_buffer(self):
        self.shadow_buffer = ""

    def read_data_(self, size):
        val = self.serial_stream.read(size)
        #We do not keep the shadow buffer in async mode
        if not self.is_active:
            self.shadow_buffer += val
        return val

    def release(self):
        self.is_active = False
        self.io_thread.join()

    @staticmethod
    def print_details(buffer, separator="\n"):
        msg = ""
        msg += "Header : " + str(hex(ord(buffer[0]))) + " - " + str(hex(ord(buffer[1]))) + separator
        msg += "Size : " + str(ord(buffer[2])) + separator
        msg += "Check Sum : " + str(ord(buffer[-1]))
        return msg

    @staticmethod
    def list_ports():
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    @staticmethod
    def compute_CS(payload):
        checksum = len(payload)
        for value in payload:
            checksum ^= value
        return checksum