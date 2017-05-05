import picamera
from server.camera.camerabase import CameraBase
import numpy as np


class Picam(CameraBase):
    def __init__(self):
        self.device = picamera.PiCamera()
        self.device.vflip = True
        self.device.hflip = True
        self.h = 480
        self.w = 640
        self.device.resolution = (self.w, self.h)

    def get_frame(self):
        output = np.empty((self.h, self.w, 3), dtype=np.uint8)
        self.device.capture(output, 'rgb')
        return output
