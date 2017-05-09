"""
    The indexer controls image database : how to write images and how to read them
"""
from time import localtime, strftime
import datetime
import os

class Indexer:
    def __init__(self):
        pass

    @staticmethod
    def generate_time_tag():
        """
        file tags : YYYYMMDDHHMMSS
        exemple 11 May 1918 14h 49m 52s  => 19180511144952
        :return:
        """
        tag = strftime("%Y%m%d%H%M%S", localtime())
        return tag

    @staticmethod
    def tag_to_date(tag):
        date = datetime.datetime.strptime(str(tag), "%Y%m%d%H%M%S").date()
        return date

    @staticmethod
    def get_last_tag_from_folder(path):
        files = [int(f[:-4]) for f in os.listdir(path) if ".jpg" in f]
        files.sort()
        return str(files[-1])
