import os
import sys
import subprocess


def shell(command):
    """
    Executes command in shell

    :param command: command string
    """
    return subprocess.run(command, shell=True)


def raise_error(command):
    """
    Executes command in shell and raises an error if the command outputs non-zero exit code

    :param command: command string
    """
    return subprocess.check_output(command, shell=True)


def bckgr(command):
    """
    Run shell command as background process

    :param command: command string
    """
    return subprocess.Popen(command, shell=True)


def error():
    """
    :return: subprocess.CalledProcessError
    """
    return subprocess.CalledProcessError
