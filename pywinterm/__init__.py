"""
System functions
"""
import os
import sys


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