# This is a sample Python script.

from __future__ import with_statement
import re
import os
import subprocess


names = []
cmd = []
fin_dict = {}
pattern_name = r'\b[A-Z].*(?==)'
pattern_command = r'\bssh\s.*(?=\")'
global_iterator = 0


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


def print_list(listik):
    for i in range(len(listik)):
        print(listik[i])


if __name__ == "__main__":
    os.system('clear')
    parser()
#    print_list(names)
#    print_list(cmd)
    global_iterator = 1
    for x in range(len(names)):
        print("{}) {}".format(global_iterator, color_text(names[x], RGB.RED)))
        print("         {}  ".format(color_text(cmd[x], RGB.GREEN)))
        global_iterator += 1
    inp = int(input("\nChoose your destiny (q for quit):  "))
    if 1 <= inp < 24:
        print(f"you have chosen {inp}")
        print(names[inp - 1])
        print(cmd[inp - 1])
    else:
        print("ты идёшь в хуй")


