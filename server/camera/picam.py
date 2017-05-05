import picamera
from server.camera.camerabase import CameraBase


class Picam(CameraBase):
    def __init__(self):
        self.device = picamera.PiCamera()
        self.device.vflip = True

    def get_frame(self):
        pass

