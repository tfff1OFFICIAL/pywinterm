"""
Screen utilities
"""
from pywinterm.display import util, style, style
from pywinterm.display.style import foreground, background
import os


class Label:
    def __init__(self, text, fore_colour=None, back_colour=None):
        self.text = text
        self.fore_colour = fore_colour
        self.back_colour = back_colour
        self.index = 0

    def _generate_colour_start_sequence(self):
        if self.fore_colour and self.back_colour:
            return style.ESCAPE_SEQUENCE + self.fore_colour + ";" + self.back_colour
        elif self.fore_colour:
            return style.ESCAPE_SEQUENCE + self.fore_colour
        elif self.back_colour:
            return style.ESCAPE_SEQUENCE + self.back_colour
        else:
            return style.END

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

    def __getitem__(self, item):
        if item == 0:
            return self._generate_colour_start_sequence() + self.text[0]
        elif item == len(self.text) - 1:
            return self.text[item] + style.END
        else:
            return self.text[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.text):
            raise StopIteration
        elif self.index == 0:
            result = self._generate_colour_start_sequence() + self.text[0]
        elif self.index == len(self.text) - 1:
            result = self.text[self.index] + style.END
        else:
            result = self.text[self.index]

        self.index += 1
        return result


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

    def add_display(self, obj):
        """
        Adds a label or display as a child
        :param obj: Label, Display
        :return: None
        """
        self.children.append(obj)

    def printline(self, text):
        """
        Prints text inside this Display
        :param text: String
        :return: None
        """
        self.text.append(text)

    def printlines(self, texts=None, *args):
        """
        Prints multiple rows of text inside this Display

        Fails silently if nothing is specified to print
        :param texts: iter<string>
        :return: None
        """
        if texts is not None:
            self.text.extend(texts)

        if args is not None:
            self.text.extend(args)

    def clear(self):
        """
        Clears the text
        :return: None
        """
        self.text = []

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
        util.resize_window(self.width, self.height)
        util.clear_window()

    def render(self):
        """
        Renders everything
        :return: None
        """
        util.clear_window()

        for row in util.flatten_root(self):
            print(''.join(row))


        """
        for row in util.flatten_root(self):
            for char in row:
                print(char, end="")
            print()
        """


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
    menu.printline("hi there!")
    l = Label("how are you?", fore_colour=style.foreground.RED)
    for x in l:
        print(x)
    menu.printline(l)

    #root.printline("aweroignarilgunairltuhmargl")
    #root.printline("aisuhtnalkrwtxmal,rugmixuas")

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

        l.fore_colour = cols[x]

        root.render()

        time.sleep(0.5)
