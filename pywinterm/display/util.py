"""
Display utilities
"""
import os


def clear_window():
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


def set_window_title(title):
    """
    Set the window title
    :param title: String
    :return: None
    """
    os.system("TITLE {}".format(title))


def resize_window(width, height):
    """
    Resize the terminal window
    :param width: width of the terminal (chars)
    :param height: height of the terminal (rows)
    :return: None
    """
    os.system("mode con: cols={} lines={}".format(width, height))


# For merging content from many displays onto one plane

NON_PREFERABLE_CHARACTERS = (' ', '\t', '\n', '\r')
"""
# Modified from: https://stackoverflow.com/questions/8427330/merging-a-list-of-lists-such-that-unique-values-overwrite-nonunique-ones
def non_white_if_possible(items):
    try:
        return set(items).difference(NON_PREFERABLE_CHARACTERS).pop()
    except KeyError:
        return '*'


def merge(lists):
    t = [non_white_if_possible(items) for items in zip(*lists)]
    print(t)
    return t


def merge_all(data):
    print(data)
    for lists in zip(*data):
        print(lists)
        m = merge(lists)
        print(m)
        return m
"""


def flatten_root(root):
    """
    Merges displays into one list of strings for outputting
    :param root: Display, the root display
    :return: list<list<char>>
    """
    screen = [[" " for i in range(root.width)] for x in range(root.height)]  # pre-generate the matrix

    """
    for l in range(len(root.text)):  # render the text
        line = list(root.text[l])
        for i in range(len(line)):
            screen[l].insert(i, line[i])
    """

    def flatten_display(display, x=0, y=0):
        """
        Merges displays into one list of strings for outputting
        :param display: Display, the display we're merging
        :param x: int, total x indent of parent
        :param y: int, total y indent of parent
        :return: None
        """
        y_total = display.y + y
        x_total = display.x + x

        for l in range(len(display.text)):  # render the text
            for i in range(len(display.text[l])):
                print("screen[{}][{}] = {}".format(l + y_total, i + x_total, display.text[l][i]))
                screen[l + y_total][i + x_total] = display.text[l][i]

        for disp in display.children:  # repeat for all of the children, and the children's children etc.
            flatten_display(disp, x_total, y_total)

    flatten_display(root)  # begin the flattening of displays

    return screen
