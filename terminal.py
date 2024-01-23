import os


def add_to_ubuntu(name):
    pswd = "123"
    os.system("useradd -p " + pswd + " " + name)


def delete_user(name):
    os.system("deluser" + name)
