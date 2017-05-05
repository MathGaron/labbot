from server.camera.camerabase import CameraBase
import cv2


class Webcam(CameraBase):
    def __init__(self):
        self.device = cv2.VideoCapture(0)

    def __del__(self):
        self.device.release()

    def get_frame(self):
        ret, frame = self.device.read()
        return frame