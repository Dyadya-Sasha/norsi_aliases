# This is a sample Python script.
import os
import re
from time import sleep
import subprocess
import sys

names = []
cmd = []
fin_dict = {}
pattern_name = r'\b[A-Z].*(?==)'
pattern_command = r'\bssh\s.*(?=\")'
global_iterator = 0
pattern_ip = r'[\d{}]{,3}(?:[.][\d{}]{,3}){3}'
pattern_port = r'\d{4}'


class RGB:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


def color_text(text, rgb):
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def finder(pat, text):
    match = re.search(pat, str(text))
    str_match = format(match.group(0))
    return str_match


def parser():
    with open('norsi_aliases', 'r') as f:
        test = f.readlines()
        i = 0
        for line in test:
            #            print(color_text(finder(pattern_name, line), RGB.RED))
            #            print(color_text(finder(pattern_command, line), RGB.GREEN))
            names.append(finder(pattern_name, line))
            cmd.append(finder(pattern_command, line))
            i = i + 1
    f.close()


# def print_list(listik):
#     for i in range(len(listik)):
#         print(listik[i])


def ssh_connect(name, command):
    # hostname = "192.168.122.248"
    # username = "root"
    # password = "qwedsa"
    # s = paramiko.SSHClient()
    # s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    # s.connect(hostname="192.168.122.248", username="root", password="qwedsa")
    # while True:
    #     try:
    #         cmd = input("root>")
    #         if cmd == "exit": break
    #         stdin, stdout, stderr = s.exec_command(cmd)
    #         print(stdout.read().decode())
    #     except KeyboardInterrupt:
    #         break
    # s.close()
    # subprocess.call('clear')
    print(f"\nConnecting to {name} {command}")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        sleep(3)


if __name__ == "__main__":
    os.chdir(sys.path[0])
    parser()
    while True:
        try:
            subprocess.call('clear')
            #    print_list(names)
            #    print_list(cmd)
            global_iterator = 1
            for x, item in enumerate(names):
                print(f"{x +1}) {color_text(names[x], RGB.RED)}")
                print(f"    {format(color_text(cmd[x], RGB.GREEN))}")
                global_iterator += 1
            try:
                inp = int(input("\nChoose your destiny (any other key to exit):  "))
            except ValueError:
                sys.exit("Exit")

            if 1 <= inp < 25:
                ssh_connect(names[inp - 1], cmd[inp - 1])
            else:
                print("Your choice is out range")
                sleep(1)
        except KeyboardInterrupt:
            print("\nInterrupted from keyboard")
