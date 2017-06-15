"""
Screen utilities
"""
import os


def clear():
    """
    Clears the screen
    :return: None
    """
    os.system("cls")


def render_chars(arr):
    """
    Prints every character to the terminal window
    :param arr: iter<String>, each String is a line in the terminal
    :return: None
    """
    for row in arr:
        print(arr)


def set_title(title):
    """
    Set the window title
    :param title: String
    :return: None
    """
    os.system("TITLE {}".format(title))


def resize(width, height):
    """
    Resize the terminal window
    :param width: width of the terminal (chars)
    :param height: height of the terminal (rows)
    :return: None
    """
    os.system("mode con: cols={} lines={}".format(width, height))
