

class Logger:
    def __init__(self, file_path):
        self.path = file_path
        self.log_file = open(file_path, "a")

    def __del__(self):
        self.log_file.close()

    def add_line(self, msg):
        # make sure the user will not write on more than one line
        msg.replace("\n", "")
        self.log_file.write(msg + "\n")

    def __len__(self):
        i = -1
        with open(self.path) as f:
            for i, l in enumerate(f):
                pass
        return i + 1