import os
import re
from time import sleep
import subprocess
import sys
import socket


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
    match_ = re.search(pat, str(text))
    str_match = format(match_.group(0))
    return str_match


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
            #            print(color_text(finder(pattern_name, line), RGB.RED))
            #            print(color_text(finder(pattern_command, line), RGB.GREEN))
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


def ssh_connect(name, command):
    print(f"\nConnecting to {name} {command}")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        sleep(2)


def port_test(address, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = (address, port)
    result_of_check = a_socket.connect_ex((address, int(port)))

    if result_of_check == 0:
        # print("Port is open")
        a_socket.close()
        return RGB.GREEN
    else:
        # print("Port is not open")
        a_socket.close()
        return RGB.RED


if __name__ == "__main__":
    os.chdir(sys.path[0])
    parser()
    while True:
        x = 0
        try:
            subprocess.call('clear')
            for key, val in united_dict.items():
                x += 1
                print(f"{x :<2}) {color_text(val[0], RGB.RED)} {color_text(unicode_status, val[4])}")
                print(f"      {color_text(val[1], RGB.GREEN)}")
            # for x, item in enumerate(names):
            #     print(f"{x + 1:<2}) {color_text(names[x], RGB.RED):<10}  {color_text(unicode_status, RGB.GREEN)}")
            #     print(f"      {color_text(cmd[x], RGB.GREEN)}")
            #     print(f"address: {ip_list[x]}    port: {port_list[x]}")
            # for key, val in united_dict.items():
            #     print(f"{key:}\n {val}")
            try:
                inp = input("\nChoose your destiny (any other key to exit):  ")
                if inp.isdigit():
                    inp = int(inp)
                else:
                    sys.exit('Exit')
            except ValueError:
                sys.exit("Exit")

            if 1 <= inp < 25:
                ssh_connect(united_dict.get((inp - 1))[0], {united_dict.get((inp - 1))[1]})
                # sleep(10)
            else:
                print("Your choice is out range")
                sleep(1)
        except KeyboardInterrupt:
            print("\nInterrupted from keyboard")