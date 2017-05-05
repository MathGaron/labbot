import abc


class CameraBase(abc.ABC):
    @abc.abstractmethod
    def get_frame(self):
        pass