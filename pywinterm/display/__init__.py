"""
Screen utilities
"""
from pywinterm.display import util, style, style, widget
from pywinterm.display.exceptions import *
from pywinterm.display.style import foreground, background
import platform


def Label(text, fore_colour=None, back_colour=None, text_alignment=0):
    """
    Generator for a Label for back compatibility
    :return: Label
    """
    s = style.Style(fore=fore_colour, back=back_colour)
    return widget.Label(
        text,
        s,
        alignment=text_alignment
    )


class Display:
    """
    Represents a Window object. Stuff can be drawn on to the window using it's functions.
    """
    def __init__(self, parent=None, width=100, height=30, x=0, y=0, children=()):
        """
        Initialise a Display
        :param parent: Display, the parent of this Display
        :param width: int, the number of characters to fit along the x axis in this display
        :param height: int, the number of rows of characters to find along the y axis in this display
        :param x: int, characters to the right of the Parent Display to position this Display
        :param y: int, characters below the top of the Parent Display to position this Display
        :param children: tuple, Child Displays
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.children = list(children)
        self.text = []

        self.parent = parent

    def add_display(self, disp):
        """
        Adds a label or display as a child
        :param disp: Label, Display
        :return: None
        """
        # Issue checking:
        if disp.width > self.width:
            raise DisplaySizeError("Display is too wide to fit here")
        if disp.height > self.height:
            raise DisplaySizeError("Display is too tall to fit here")

        self.children.append(disp)

    def print(self, *args):
        """
        Prints text inside this Display
        :return: None
        """
        if args is not None:
            self.text.extend(args)

    def clear(self):
        """
        Clears the text and the children
        :return: None
        """
        self.text.clear()
        self.children.clear()

    def centre_on_parent(self):
        """
        Centres this on the parent as much as is possible using integer division
        :return: None
        """
        self.x = (self.parent.width // 2) - (self.width // 2)
        self.y = (self.parent.height // 2) - (self.height // 2)

    def __repr__(self):
        return '<Display x: %r, y: %r, height: %r, width: %r>' % (self.x, self.y, self.height, self.width)


class RootDisplay(Display):
    """
    A Display object for the root
    """
    def __init__(self, title="", *args, **kwargs):
        self.title = title

        super(RootDisplay, self).__init__(*args, **kwargs)

        self.x = 0
        self.y = 0

        util.set_window_title(self.title)
        self.resize_window(self.width, self.height)
        util.clear_window()

    def update_title(self, title):
        """
        Change the Window title
        :param title: string
        :return: None
        """
        self.title = title
        util.set_window_title(self.title)

    def resize_window(self, x, y):
        """
        Resizes the window
        :param x: int
        :param y: int
        :return: None
        """
        if platform.uname().version == "10":
            util.resize_window(self.width, self.height + 1)  # +1 because we need to leave room for the cursor in the terminal
        else:
            util.resize_window(self.width+5, self.height + 5)  # in order to make the default font fit correctly, based on some testing

    def flatten(self):
        """
        Merges displays and then renders them
        :return: list<list<char>>, a matrix representing the screen, rows first, then columns
        """
        screen = [[" " for i in range(self.width)] for x in range(self.height)]  # pre-generate the screen matrix

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
                # decide on how many spaces to leave before the text (to handle alignment)
                indent = 0
                if issubclass(type(display.text[l]), widget.Widget):
                    # if display.text[l].text_alignment == 0:
                    # left alignment
                    if display.text[l].alignment == style.alignment.CENTRE:
                        # centre alignment
                        indent = (display.width // 2) - (len(display.text[l]) // 2)
                    elif display.text[l].alignment == style.alignment.RIGHT:
                        # right alignment
                        indent = display.width - len(display.text[l])

                for i in range(len(display.text[l])):
                    # print("screen[{}][{}] = {}".format(l + y_total, i + x_total + indent, display.text[l][i]))
                    try:
                        screen[l + y_total][i + x_total + indent] = str(display.text[l][i])
                    except IndexError:
                        raise DisplayError("Either the Label is too long, or the Display is too large.")

            for disp in display.children:  # repeat for all of the children, and the children's children etc.
                flatten_display(disp, x_total, y_total)

        flatten_display(self)

        return screen

    def render(self):
        """
        Renders everything
        :return: None
        """
        util.clear_window()

        for row in self.flatten():
            print(''.join(row))

if __name__ == "__main__":
    import time
    # unit testing

    # init the displays
    root = RootDisplay(
        title="Test"
    )

    menu = Display(
        root,
        width=11,
        height=2
    )
    menu.centre_on_parent()

    # link displays
    root.add_display(menu)

    # print things to the displays
    menu.print("hi there!")
    l = widget.Label("how are you?")
    #for x in l:
    #    print(x)
    menu.print(l)

    root.print(widget.Label("Left", alignment=0))
    root.print(widget.Label("Centre", alignment=1))
    root.print(widget.Label("Right", alignment=2))

    x = 0

    cols = (
        style.foreground.WHITE,
        style.foreground.RED,
        style.foreground.BLUE,
        style.foreground.CYAN,
        style.background.GREEN,
        style.background.MAGENTA
    )

    while True:
        if x < 5:
            x += 1
        else:
            x = 0

        l.style.fore = cols[x]

        root.render()

        time.sleep(0.5)
