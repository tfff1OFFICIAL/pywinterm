class DisplayException(Exception):
    """
    A general error with displays
    """


class DisplaySizeException(DisplayException):
    """
    For when there is a problem with a display's size
    """


class LabelTooLongException(DisplayException):
    """
    For when a label is too long to fit in it's designated display
    """