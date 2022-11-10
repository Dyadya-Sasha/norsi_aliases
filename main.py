

import os
import re
from time import sleep
import subprocess
import sys

names = []
cmd = []
ip_list = []
port_list = []
pattern_name = r'\b[A-Z].*(?==)'
pattern_command = r'\bssh\s.*(?=\")'
pattern_ip = r'[\d]{,3}(?:[.][\d]{,3}){3}'
pattern_port = r'\d{4}'
uni_status = "\u25C9"


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
            ip_list.append(finder(pattern_ip, line))
            port_list.append(finder(pattern_port, line))
            i = i + 1
    f.close()


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
        sleep(2)


if __name__ == "__main__":
    os.chdir(sys.path[0])
    parser()
    while True:
        try:
            subprocess.call('clear')
            #    print_list(names)
            #    print_list(cmd)
            for x, item in enumerate(names):
                print(f"{x + 1:<2}) {color_text(names[x], RGB.RED):<10}  {color_text(uni_status, RGB.GREEN)}")
                print(f"      {color_text(cmd[x], RGB.GREEN)}")
                # print(f"address: {ip_list[x]}    port: {port_list[x]}")
            try:
                inp = input("\nChoose your destiny (any other key to exit):  ")
                if inp.isdigit():
                    inp = int(inp)
                else:
                    sys.exit('Exit')
            except ValueError:
                sys.exit("Exit")

            if 1 <= inp < 25:
                ssh_connect(names[inp - 1], cmd[inp - 1])
            else:
                print("Your choice is out range")
                sleep(1)
        except KeyboardInterrupt:
            print("\nInterrupted from keyboard")
