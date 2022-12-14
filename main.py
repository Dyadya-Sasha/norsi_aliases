import re
import os
from time import sleep
import subprocess
import sys
import socket
import argparse

pattern_name = r'\b[A-Z].*(?==)'
pattern_command = r'\bssh\s.*(?=\")'
pattern_ip = r'[\d]{,3}(?:[.][\d]{,3}){3}'
pattern_port = r'\d{4}'
unicode_status = "\u25C9"
united_dict = {}


class RGB:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


def color_text(text, rgb):
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def finder(pat, text):
    try:
        match_ = re.search(pat, str(text))
        str_match = format(match_.group(0))
        return str_match
    except AttributeError:
        print("Something is wrong with reference file")
        sys.exit()


def parser():
    order = []
    names = []
    cmd = []
    ip_list = []
    port_list = []
    port_avail = []
    global united_dict
    with open('norsi_aliases', 'r') as f:
        test = f.readlines()
        i = 0
        for line in test:
            if line == "\n":
                continue
            else:
                order.append(i)
                names.append(finder(pattern_name, line))
                cmd.append(finder(pattern_command, line))
                ip_list.append(finder(pattern_ip, line))
                port_list.append(finder(pattern_port, line))
                port_avail.append(port_test(finder(pattern_ip, line), finder(pattern_port, line)))
                i = i + 1
    f.close()
    united_dict = {z[0]: list(z[1:]) for z in zip(order, names, cmd, ip_list, port_list, port_avail)}
    names.clear()
    cmd.clear()
    ip_list.clear()
    port_list.clear()
    order.clear()


def ssh_connect(name, command):
    print(f"\nConnecting to {name} {command}")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        sleep(0.8)


def port_test(address, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(0.2)
    try:
        result_of_check = a_socket.connect_ex((address, int(port)))
        if result_of_check == 0:
            # print("Port is open")
            a_socket.close()
            # print(f"{address}:{port} is online")
            return RGB.GREEN
        else:
            # print("Port is not open")
            a_socket.close()
            # print(f"{address}:{port} is offline")
            return RGB.RED
    except socket.error:
        return


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="You can use this script in 2 ways - either direct SSH connection or grab information about nodes."
                                                     "To grab info about nodes, you have to specify -t option")
    arg_parser.add_argument("-t",
                            type=str,
                            help="Grab info about nodes")
    option_keys = arg_parser.parse_args()
    print(option_keys.t)
    if option_keys.t == "-t":
        sys.exit("-t option is enabled")

    os.chdir(sys.path[0])
    counter = 0
    while True:
        x = 0
        parser()
        try:
            subprocess.call('clear')
            for key, val in united_dict.items():
                x += 1
                print(f"{x :<2}) {color_text(unicode_status, val[4])} {color_text(val[0], RGB.RED)}")
                print(f"      {color_text(val[1], RGB.GREEN)}")
            # for key, val in united_dict.items():
            # print(f"{key:}\n {val}")
            try:
                inp = input("\nChoose your destiny (any other key to exit):  ")
                if inp.isdigit():
                    inp = int(inp)
                else:
                    sys.exit('Exit')
            except ValueError:
                sys.exit("Exit")

            if 1 <= inp <= len(united_dict):
                ssh_connect(united_dict.get((inp - 1))[0], {united_dict.get((inp - 1))[1]})
                # sleep(10)
            else:
                print("Your choice is out range")
                sleep(1)
        except KeyboardInterrupt:
            pass
