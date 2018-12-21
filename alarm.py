#!/use/bin/env python3
# coding:utf-8

import glob
import os
from paramiko import SSHClient, AutoAddPolicy
import sys

# Execution darknet
def darknet():
    target_file = glob.glob("/home/iplab/Projects/PBLDrone/detected/*.jpg")
    for file in target_file:
        result = subprocess.run(["/home/darknet/darknet", "detect", "cfg/yolo-pbldrone.cfg",".weights", file], capture_output=True)

        # Classifing Drone
        decode_lines = result.stdout.decode('utf-8')
        lines = decode_lines.split('\n')
        accuracy = int(lines[-2].split(': ')[-1].strip('%'))
        return accuracy
                   
# Alarm @Raspberrypi
def request():

    Host = '<address>'
    Port = 22
    User = '<name>'
    Pass = '<your-pass>'

    # Connecting
    with SSHClient() as c:
        c.load_system_host_keys()
        c.connect(Host, Port, User, Pass)

        # Execution
        stdin, stdout, stderr = c.exec_command('speaker-test -t sine -f 600')
        print("Alarming")

def main():
    darknet()
    if accuracy > 80:
        request()
    else:
        pass

if __name__ == "__main__":
    main()
