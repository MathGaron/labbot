import abc


class CameraBase(abc.ABC):
    @abstractmethod
    def get_frame(self):
        pass