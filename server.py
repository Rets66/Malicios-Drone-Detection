#!/use/bin/env python3
# coding:utf-8

from glob import glob
import os
from paramiko import SSHClient, AutoAddPolicy
import subprocess
import shutil

# Save prediction image to Prediction Folder
def save_predictions(file):
    target_dir = '/home/iplab/Predictions'
    src = '/home/iplab/darknet/predictions.jpg'
    file_name = os.path.basename(file)

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    dst = '{}/pre_{}'.format(target_dir,file_name)
    shutil.copyfile(src, dst)

target = ''
def load_file():
    path = "/home/iplab/Projects/PBLDrone/detected/"
    file_list = [i for i in os.listdir(path) if "jpg" in i]
    target = sorted(file_list)[-1]
    return target

accuracy = ''
def get_accuracy(target):
    result = subprocess.run(["/home/iplab/darknet/darknet", "detector",\
                            "test", "/home/iplab/darknet/cfg/pbldrone.data",\
                            "/home/iplab/darknet/cfg/yolo-pbldrone.cfg",\
                            "/home/iplab/darknet/yolo-pbldrone_1200.backup",\
                            target], stdout=subprocess.PIPE)

	# Save prediction image to Prediction Folder
    # save_predictions(target)

    # Classifing Drone
    decode_lines = result.stdout.decode('utf-8')
    lines = decode_lines.split('\n')
    if 'drone' in lines:
        accuracy = int(lines[-3].split(': ')[-1].strip('%'))
        return accuracy
		#    if 'drone' not in lines:
		#    	continue
		#    else:
		#        accuracy = int(lines[-3].split(': ')[-1].strip('%'))
		#        return accuracy


# @Raspberrypi
def connect_pi():
    """
    Connecting RaspberryPi if the accuracy is more than 80%.
    80% is a temporary proportion.
    """

    Host = '163.221.52.134'
    Port = 22
    User = 'pi'
    Pass = 'raspberry'

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
        print(accuracy)
        if accuracy < 60:
            continue
        else:
            connect_pi()

if __name__ == "__main__":
    main()
