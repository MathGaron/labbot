from server.communication.tasks.task_base import TaskBase


class TestTask(TaskBase):
    def trigger(self, msg):
        # simply check if the first " " separated word is test
        return msg.split(" ")[0] == "test"

    def callback(self, slack, channel):
        print("Test Callback trigged")

    def name(self):
        return "Test"

    def help(self):
        return "test [...]", "Print to the server console"