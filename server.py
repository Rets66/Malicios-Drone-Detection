#!/use/bin/env python3
# coding:utf-8

from glob import glob
from os import path
from paramiko import SSHClient, AutoAddPolicy
import subprocess

target = ''
def load_file():
    path = "/home/iplab/Projects/PBLDrone/detected/"
    target = sort([i for i in os.listdir(path) if "jpg" in  i], key=os.path.getmtime)[0]
    return target

accuracy = ''
def get_accuracy(target):
    result = subprocess.run(["/home/darknet/darknet", "detector", "test",\
                            "cfg/pbldrone.data", "cfg/yolo-pbldrone.cfg",\
                            "yolo-pbldrone_1200.backup", file], capture_output=True)

    # Classifing Drone
    decode_lines = result.stdout.decode('utf-8')
    lines = decode_lines.split('\n')
    if 'drone' in lines:
        accuracy = int(lines[-3].split(': ')[-1].strip('%'))
        return accuracy
    else:
        print("Can't find drones")
                       
# @Raspberrypi
def connect_pi():
    """
    Connecting RaspberryPi if the accuracy is more than 80%.
    80% is a temporary proportion.
    """

    Host = '<address>'
    Port = 22
    User = '<name>'
    Pass = '<your-pass>'

    # Connect
    with SSHClient() as c:
        c.load_system_host_keys()
        c.connect(Host, Port, User, Pass)

        # Alart
        stdin, stdout, stderr = c.exec_command('speaker-test -t sine -f 600',\
                                                timeout=5)
        print("Alarming")

def main():
    while True:
        target = load_file()
        accuracy = get_accuracy(target)
        if accuracy > 60:
            connect_pi()
        else:
            pass

if __name__ == "__main__":
    main()
