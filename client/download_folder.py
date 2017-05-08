import sys
import json
import os
import sys
sys.path.append("../")
from client.ssh_connection import SshConnection

if __name__ == '__main__':
    config_file = sys.argv[1]

    with open(config_file) as data_file:
        data = json.load(data_file)

    server = data["server"]
    user = data["user"]
    remote_path = data["remote_path"]
    host_path = data["host_path"]

    if not os.path.exists(host_path):
        os.mkdir(host_path)

    ssh = SshConnection(server, user, verbose=True)
    ssh.download_dir(remote_path, host_path)