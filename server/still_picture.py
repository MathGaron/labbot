import sys
sys.path.append("/home/mathieu/source/labbot")
import json
import os
from server.logger import Logger

if __name__ == '__main__':
    config_file = sys.argv[1]

    with open(config_file) as data_file:
        configs = json.load(data_file)

    log_file_path = os.path.join(configs["data_folder"], "log.txt")
    logger = Logger(log_file_path)
    logger.add_line("line {}".format(len(logger)))
