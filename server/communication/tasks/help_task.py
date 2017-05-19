from server.communication.tasks.task_base import TaskBase


class HelpTask(TaskBase):
    def __init__(self, task_list):
        self.task_list = task_list

    def trigger(self, msg):
        return msg.split(" ")[0] == "help"

    def callback(self, slack, channel):
        help_msg, _ = self.help()
        help_msg += "\n"
        help_msg += '{0:<20} {1:>30} : {2:<60}'.format("*Name*", "*Command*", "*Description*")
        for task in self.task_list:
            task_name = task.name()
            task_exemple, task_description = task.help()
            task_exemple = task_exemple.replace("\n", "")
            task_description = task_description.replace("\n", "")
            help_msg += "\n"
            help_msg += '{0:<20} {1:>30} : {2:<60}'.format(task_name, task_exemple, task_description)
        return help_msg

    def name(self):
        return "Help"

    def help(self):
        return "Help : ", ""
