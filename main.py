import re
import os
from time import sleep
import subprocess
import sys
import socket
import argparse
import paramiko
import json
from rich import print_json

pattern_name = r'\b[A-Z].*(?==)'
pattern_command = r'\bssh\s.*(?=\")'
pattern_ip = r'[\d]{,3}(?:[.][\d]{,3}){3}'
pattern_port = r'\d{4}'
unicode_status = "\u25C9"
united_dict = {}
node_option = False
json_out = ""


class RGB:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


def color_text(text, rgb):
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def opt_parser():
    arg_parser = argparse.ArgumentParser(
        description="You can use this script in 2 ways - either direct SSH connection or to grab information about nodes."
                    "To grab info about nodes, you have to specify -t option. <prog_name -t>")
    arg_parser.add_argument('-t', action="store_true",
                            help="Grab info about nodes")
    option_keys = arg_parser.parse_args()
    if option_keys.t:
        global node_option
        node_option = True
        # sys.exit("-t option is enabled")


def finder(pat, text):
    try:
        match_ = re.search(pat, str(text))
        str_match = format(match_.group(0))
        return str_match
    except AttributeError:
        print("Something is wrong with reference file")
        sys.exit()


def parser():
    global united_dict
    _list = []
    with open("norsi.json", "r") as file:
        json_data = json.load(file)
        # # print(type(json_data))
        # print("\n")
        counter = 0
        for item in enumerate(json_data):
            _list.append(item[1].get("name"))
            _list.append(item[1].get("command"))
            _list.append(item[1].get("password"))
            _list.append(item[1].get("segments")[0].get("name"))
            _list.append(item[1].get("segments")[0].get("ip"))
            _list.append(item[1].get("segments")[1].get("name"))
            _list.append(item[1].get("segments")[1].get("ip"))
            _list.append(port_test(finder(pattern_ip, item[1].get("command")), finder(pattern_port, item[1].get("command"))))
            united_dict[counter + 1] = _list
            # print(united_dict)
            _list = []
            counter += 1


def ssh_connect(choice, segment=0, complexity=False):
    print(f"\nConnecting to {color_text(united_dict[choice][0:2], RGB.YELLOW)}")
    if node_option:
        print(f" Grabbing info from {finder(pattern_ip, united_dict[choice][1])}, {finder(pattern_port, united_dict[choice][1])}, {united_dict[choice][3]}, {united_dict[choice][4]}")
        if segment == 1:
            segment = 3
        else:
            segment = 5
        try:
            base_client = paramiko.SSHClient()
            base_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            base_client.connect(finder(pattern_ip, united_dict[choice][1]), port=int(finder(pattern_port, united_dict[choice][1])), username="root", password="[eqdjqyt")
            base_transport = base_client.get_transport()
            if segment == 3:
                base_channel = base_transport.open_channel("direct-tcpip", (united_dict[choice][4], 22), (finder(pattern_ip, united_dict[choice][1]), int(finder(pattern_port, united_dict[choice][1]))))
            else:
                base_channel = base_transport.open_channel("direct-tcpip", (united_dict[choice][6], 22), (finder(pattern_ip, united_dict[choice][1]), int(finder(pattern_port, united_dict[choice][1]))))
            # base_channel = base_transport.open_channel("direct-tcpip", ("192.168.100.1", 22), ("192.168.103.250", 22))
            jump_host = paramiko.SSHClient()
            jump_host.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if segment == 3:
                jump_host.connect(united_dict[choice][4], username="root", password="[eqdjqyt", sock=base_channel)
                stdin, stdout, stderr = jump_host.exec_command("curl -s http://127.0.0.1:8080/sorm@127.0.0.1/interfaces/1/exec_mgr")
            else:
                jump_host.connect(united_dict[choice][6], username="root", password="[eqdjqyt", sock=base_channel)
                stdin, stdout, stderr = jump_host.exec_command("curl -s http://127.0.0.1:8080/sormgw@127.0.0.1/interfaces/1/exec_mgr")
            # jump_host.connect("192.168.100.1", username="root", password="[eqdjqyt", sock=base_channel)
            # client.connect("192.168.122.80", port=22, username="user", password="12345")
            # for line in iter(stdout.readline, ""):
            #     print(line, end="")
            # inputt = input("PAUSE")
            global json_out
            json_out = stdout.read()
            test_dict = json.loads(json_out)
            print_json(data=test_dict, sort_keys=True)
            # print(json.dumps(test_dict, indent=4, sort_keys=True))
            input("PAUSE")
            # mid_result = subprocess.run("jq", input=json_out, capture_output=True)
            # subprocess.run(["less", "-R"], input=mid_result.stdout, check=True)
            jump_host.close()
            base_client.close()
        except paramiko.ssh_exception.AuthenticationException as e:
            print(e)
            sleep(2)
        except paramiko.ssh_exception.SSHException as e:
            print(e)
            sleep(2)
        finally:
            return
    else:
        try:
            subprocess.call(united_dict[choice][1], shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output)
            sleep(2)
        finally:
            return


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


def decorator(func):
    def wrapper():
        subprocess.call('clear')
        if node_option:
            print(color_text("INFO ABOUT NODES\n", RGB.RED))
            return func()
        else:
            print(color_text("DIRECT SSH CONNECTION\n", RGB.RED))
            return func()

    return wrapper


@decorator
def print_list():
    x = 1
    for key, val in united_dict.items():
        print(f"{x :<2}) {color_text(unicode_status, val[7])} {color_text(val[0], RGB.RED)}")
        print(f"      {color_text(val[1], RGB.GREEN)}")
        x += 1
        # print(united_dict)
    # for key, val in united_dict.items():
    #     print(f"{key:}\n {val}")


def print_submenu(choice):
    y = 1
    for x in range(3, 7):
        if not x % 2:
            print(f"{y :<2})  {color_text(united_dict[choice][x], RGB.RED)}")
            # t = united_dict[choice][x]
            y += 1
        else:
            print(f"   {color_text(united_dict[choice][x], RGB.GREEN)}")


if __name__ == "__main__":
    opt_parser()
    os.chdir(sys.path[0])
    while True:
        parser()
        try:
            print_list()
            try:
                inp = int(input("\nChoose your destiny (any other key to exit):  "))
            except ValueError:
                sys.exit("Exit")

            if 1 <= inp <= len(united_dict) and node_option:
                # print("SUBMENU")
                print_submenu(inp)
                try:
                    inp_sub = int(input("\nChoose desired segment:  "))
                    if inp_sub > 2:
                        continue
                    else:
                        ssh_connect(inp, inp_sub)
                        # data = json.loads(json_out)
                        # data1 = json.dumps(json.loads(data), indent=4, sort_keys=True)
                        # print(json_out)
                        # plug = input("PAUSE")
                        continue
                except ValueError:
                    sys.exit("Not a digit")
            if 1 <= inp <= len(united_dict):
                # ssh_connect(united_dict.get((inp - 1))[0], {united_dict.get((inp - 1))[1]}, {united_dict.get((inp - 1))[2]}, {united_dict.get((inp - 1))[3]})
                ssh_connect(inp)
                # sleep(10)
            else:
                print("Your choice is out range")
                sleep(1)
        except KeyboardInterrupt:
            pass
