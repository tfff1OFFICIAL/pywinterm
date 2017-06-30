class DisplayError(Exception):
    """
    A general error with displays
    """


class DisplaySizeError(DisplayError):
    """
    For when there is a problem with a display's size
    """


class LabelTooLongError(DisplayError):
    """
    For when a label is too long to fit in it's designated display
    """