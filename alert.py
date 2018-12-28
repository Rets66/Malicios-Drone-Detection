#!/use/bin/env python3
# coding:utf-8

import glob
import os
from paramiko import SSHClient, AutoAddPolicy
import subprocess

accuracy = 0
# Execution darknet
def darknet():
	target_file = glob.glob("/home/iplab/test_images/*.jpg")
	for file in target_file:
		result = subprocess.run(["/home/iplab/darknet/darknet", "detector", "test","/home/iplab/darknet/cfg/pbldrone.data",\
								"/home/iplab/darknet/cfg/yolo-pbldrone.cfg","/home/iplab/yolo-pbldrone_1200.backup", file],\
								stdout=subprocess.PIPE)

		# Classifing Drone
		decode_lines = result.stdout.decode('utf-8')
		lines = decode_lines.split('\n')
		target = lines[-2].split(': ')
		if 'drone' in  target:
			accuracy = int(target[-1].strip('%'))
			continue
		else:
			continue
		return accuracy

# Alart @Raspberrypi
def request():

    Host = '163.221.52.134'
    Port = 22
    User = 'pi'
    Pass = 'raspberry'

    # Connecting
    with SSHClient() as c:
        c.load_system_host_keys()
        c.connect(Host, Port, User, Pass)

        # Execution
        stdin, stdout, stderr = c.exec_command('speaker-test -t sine -f 600 ',timeout=5)
        print("Alarming")
        c.close()

def main():
    accuracy = darknet()
    if accuracy > 60:
        request()
    else:
        pass

if __name__ == "__main__":
    main()
