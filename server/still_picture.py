import sys
sys.path.append("/home/pi/labbot")
#sys.path.append("/home/pi/Debug_labbot_MG")
import json
import os
from PIL import Image
from time import gmtime, strftime


def get_configurations():
    """
    Load config json from first command line argument
    :return:
    """
    config_file = sys.argv[1]
    with open(config_file) as data_file:
        configs = json.load(data_file)
    if "data_folder" not in configs:
        print("[Config Missing] : data_folder")
        sys.exit(-1)
    if "camera" not in configs:
        print("[Config Missing] : camera")
        sys.exit(-1)
    return configs


def get_camera(camera_config):
    """
    Take a string and return a Camera instance
    :param camera_config:
    :return:
    """
    if camera_config == "webcam":
        from server.camera.webcam import Webcam
        camera = Webcam()
    elif camera_config == "picam":
        from server.camera.picam import Picam
        camera = Picam()
    else:
        print("Error : camera type {} is not supported".format(configs["camera"]))
        sys.exit(-1)
    return camera


def save_data(frame, folder):
    """
    Save a frame and a logger entry to folder
    :param frame:
    :param logger:
    :return:
    """
    time = strftime("%Y%m%d%H%M%S", gmtime())
    frame = Image.fromarray(frame)
    frame.save(os.path.join(folder, "{}.jpg".format(time)))

if __name__ == '__main__':

    configs = get_configurations()
    camera = get_camera(configs["camera"])
    frame = camera.get_frame()
    save_data(frame, configs["data_folder"])
