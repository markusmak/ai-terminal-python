# timer.py

from argparse import ArgumentParser
from time import sleep
import platform


def init_shell():
    print("initializing shell")
    system = platform.system()
    print(f"{system} detected")

init_shell()
