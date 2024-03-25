import os
from config import pswd


def add_to_ubuntu(name):
    os.system("useradd -p " + pswd + " " + name)


def delete_user(name):
    os.system("deluser " + name)
