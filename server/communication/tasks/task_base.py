from abc import ABCMeta, abstractmethod


class TaskBase(object):
    __metaclass__ = ABCMeta

    def callback(self, slack, channel):
        """
        Can define a callback that will be executed when the task is received, if return string, send to slack
        :return:
        """
        pass

    @abstractmethod
    def trigger(self, msg):
        """
        Parse the input msg, if return True, will call the callback.
        :return:
        """
        pass

    @abstractmethod
    def help(self):
        """
        Return a tuple (stringA, stringB)
            -stringA : how to call the task
            -stringB : one line short description of what it does
        :return:
        """
        pass

    @abstractmethod
    def name(self):
        """
        return a string with the task name
        :return:
        """
        pass