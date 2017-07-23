"""
Styles for text
"""
import platform
from . import background, foreground, alignment

# Special
ESCAPE_SEQUENCE = "\033["
END = "\033[0m"  # end the style

# Styles
RESET = "0"
BOLD = "1"
UNDERLINE = "4"
INVERSE = "7"


class Style:
    def __init__(self, fore=None, back=None, style=None):
        self.fore = fore
        self.back = back
        self.style = style

    @property
    def start_sequence(self):
        """
        :return: String, the starting sequence for the Style
        """
        if platform.uname().release == "10":  # colours only work on Windows 10
            if self.fore and self.back and self.style:
                return ESCAPE_SEQUENCE + self.fore + ";" + self.back + ';' + self.style + 'm'
            elif self.fore and self.back:
                return ESCAPE_SEQUENCE + self.fore + ";" + self.back + 'm'
            elif self.fore and self.style:
                return ESCAPE_SEQUENCE + self.fore + ";" + self.style + 'm'
            elif self.back and self.style:
                return ESCAPE_SEQUENCE + self.back + ";" + self.style + 'm'
            elif self.style:
                return ESCAPE_SEQUENCE + self.style + 'm'
            elif self.fore:
                return ESCAPE_SEQUENCE + self.fore + 'm'
            elif self.back:
                return ESCAPE_SEQUENCE + self.back + 'm'
            else:
                return END
        else:
            return ''

    @property
    def end_sequence(self):
        if platform.uname().release == "10":  # colours only work on Windows 10
            return END
        else:
            return ''

    def __repr__(self):
        return '<Style (fore: %r, back: %r, style: %r)>' % (self.fore, self.back, self.style)