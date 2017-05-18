"""
    The indexer controls image database : how to write images and how to read them
"""
from time import localtime, strftime
import numpy as np
import datetime
import os
import re

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
        dateYmd = datetime.datetime.strptime(str(tag), "%Y%m%d%H%M%S").date()
        return dateYmd

    @staticmethod
    def tag_to_datetime(tag):
        dateYmdHMS = datetime.datetime.strptime(str(tag), "%Y%m%d%H%M%S")
        return dateYmdHMS

    @staticmethod
    def get_last_tag_from_folder(path):
        files = [int(f[:-4]) for f in os.listdir(path) if ".jpg" in f]
        files.sort()
        return str(files[-1])

    @staticmethod
    def get_dates_between_interval(path,begin_interval,end_interval):
        """
        begin_interval and end_interval
        Format:  * where the date is not important and <number> otherwise
        Example:
        begin_interval="**14***"
        end_interval="**15***"
        :return: all dates between day 14 and 15 (inclusive)
        """
        files = [int(f[:-4]) for f in os.listdir(path) if ".jpg" in f]
        files.sort()
        dates = []
        
        # split intervals into a list
        begin_interval = begin_interval.split("*")
        end_interval = end_interval.split("*")
        
        for i in range(len(files)):
            date = Indexer.tag_to_datetime(files[i])
            # split date into a list of [Y,m,d,H,M,S]
            date = re.split('-| |:',str(date))

            # check if a given date is inside the intervals
            inside_interval = False
            for j in range(6):
                if begin_interval[j] != '':
                    if(date[j] >= begin_interval[j]):
                        inside_interval = True
                    else:
                        inside_interval = False
                if inside_interval:
                    if end_interval[j] != '':
                        if(date[j] <= end_interval[j]):
                            inside_interval = True
                        else:
                            inside_interval = False
            if inside_interval:
                dates.append(''.join(date))

        return dates
        

