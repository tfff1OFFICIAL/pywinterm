"""
System functions
"""
import os
import sys
import platform

if platform.system() != 'Windows':  # this module supports windows only for the time being
    raise OSError("This operation is not currently supported. Please only use this library on Windows machines.")


def pause():
    """
    Does a pause
    :return: None
    """
    os.system("pause")


def exit(status=0):
    """
    Exits the terminal
    :return: None
    """
    sys.exit(status)
