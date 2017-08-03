"""
Widgets for some nifty new features
"""
import platform
import threading
import itertools
from pywinterm.display import style
from pywinterm.key.key import TAB, RETURN, ESCAPE, BACKSPACE
from pywinterm import key


class Widget:
    """
    A Generic widget, extend this to easily create a custom widget with styling
    """
    index = 0

    def __init__(self, style=style.Style(), alignment=0):
        self.alignment = alignment
        self.style = style

    def __len__(self):
        return 0

    def __str__(self):
        return self.style.start_sequence + '' + self.style.end_sequence

    def __repr__(self):
        return '<Widget alignment: %r>' % self.alignment

    def __getitem__(self, item):
        raise NotImplementedError()
        '''
        Implement your own, something like this:
        
        if item == 0:
            return self.style.start_sequence + self.text[0]
        elif item == len(self) - 1:
            return self.text[item] + self.style.end_sequence
        else:
            return self.text)[item]
        '''
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= self.__len__():
            raise StopIteration
        elif self.index == 0:
            result = self.style.start_sequence + self[0]
        elif self.index == self.__len__() - 1:
            result = self[self.index] + self.style.end_sequence
        else:
            result = self[self.index]

        self.index += 1
        return result


class Row(Widget):
    """
    Allows for multiple widgets to be on the same line.

    NOTE: sub-widgets' alignment is ignored, they are always put one next to the other.
    """
    def __init__(self, widgets=(), *args, **kwargs):
        self.widgets = widgets
        super(self.__class__, self).__init__(*args, **kwargs)

    def __len__(self):
        l = 0
        for widget in self.widgets:
            l += len(widget)

        return l

    def __str__(self):
        return ''.join([str(widget) for widget in self.widgets])

    def __getitem__(self, item):
        return self.__str__()[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= self.__len__():
            raise StopIteration

        result = self.__str__()[self.index]
        self.index += 1

        return result

    def __repr__(self):
        return '<Row widgets: %r>' % self.widgets

DEFAULT_VALID_CHARS = (
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '0',
    '-',
    '=',
    '!',
    '@',
    '#',
    '$',
    '%',
    '^',
    '&',
    '*',
    '(',
    ')',
    '_',
    '+',
    '~',
    '`',
    'q',
    'w',
    'e',
    'r',
    't',
    'y',
    'u',
    'i',
    'o',
    'p',
    '[',
    ']',
    'Q',
    'W',
    'E',
    'R',
    'T',
    'Y',
    'U',
    'I',
    'O',
    'P',
    '{',
    '}',
    'a',
    's',
    'd',
    'f',
    'g',
    'h',
    'j',
    'k',
    'l',
    ';',
    "'",
    'A',
    'S',
    'D',
    'F',
    'G',
    'H',
    'J',
    'K',
    'L',
    ':',
    '"',
    'z',
    'x',
    'c',
    'v',
    'b',
    'n',
    'm',
    ',',
    '.',
    '/',
    'Z',
    'X',
    'C',
    'V',
    'B',
    'N',
    'M',
    ',',
    '<',
    '>',
    '?',
    ' ',
    # '\t' - no because Tab should be used to change focus by default
)


class TextInput(Widget):
    """
    An input widget to input text of unlimited length
    """
    def __init__(
            self,
            length,
            valid_chars=DEFAULT_VALID_CHARS,
            unfocus_keys=(ESCAPE, RETURN, TAB),
            unfocus_handler=lambda k: None,
            backspace_key=BACKSPACE,
            style=style.Style(),
            *args,
            **kwargs
    ):
        self.length = length
        self.valid_chars = valid_chars

        self.style = style

        self.unfocus_keys = unfocus_keys

        self.backspace_key = backspace_key

        self.text = ""
        self.text_lock = threading.Lock()

        self.unfocus_handler = unfocus_handler

        self._keylistener_stop_event = threading.Event()
        self._keylistener_stop_event.set()

        super(self.__class__, self).__init__(*args, **kwargs)

    def keypress_handler(self, k, rerender_event):
        """
        Handles every keypress for the ThreadedKeyListener
        :param k: Key
        :param rerender_event: threading.Event
        :return: None
        """
        if k in self.valid_chars:
            with self.text_lock:
                self.text += str(k)
            rerender_event.set()
        elif k in self.unfocus_keys:
            self._unfocus(k)  # call the internal unfocus which was designed for this purpose
        elif k == self.backspace_key:
            with self.text_lock:
                self.text = self.text[:-1]
            rerender_event.set()

    @property
    def is_focused(self):
        return not self._keylistener_stop_event.is_set()

    def focus(self, sleep_time=0.1, blocking=False, rerender_event=threading.Event()):
        """
        Hijack keylistening until one of the unfocus keys is hit
        :param rerender_event: threading.Event, set on update time
        :return: None
        """
        if not self.is_focused:
            self._keylistener_stop_event.clear()

            keylistener = key.ThreadedKeyListener(
                self._keylistener_stop_event,
                self.keypress_handler,
                sleep_time,
                rerender_event=rerender_event
            )

            keylistener.start()

            if blocking:
                keylistener.join()
        else:
            raise RuntimeError('You cannot call focus more than once without unfocusing first')

    def unfocus(self):
        """
        Unfocus ourselves, kill the ThreadedKeyListener
        :return: None
        """
        self._keylistener_stop_event.set()

    def _unfocus(self, k=None):
        """
        For internal use by the ThreadedKeyListener. unfocuses and executes the unfocus handler
        :param k: Key/None, the key that was pressed to cause the exit.
        :return: None
        """
        self.unfocus()
        self.unfocus_handler(k)

    @property
    def _unstyled_text(self):
        with self.text_lock:
            if len(self.text) >= self.length:
                return self.text[-self.length:]
            else:
                return self.text + '_' * (self.length - len(self.text))

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        if item == 0:
            return self.style.start_sequence + self._unstyled_text[0]
        elif item == len(self) - 1:
            return self._unstyled_text[item] + self.style.end_sequence
        else:
            return self._unstyled_text[item]

    def __str__(self):
        return self.style.start_sequence + self._unstyled_text + self.style.end_sequence

    def __repr__(self):
        with self.text_lock:
            return '<TextInput length: %r, text: %r>' % (self.length, self.text)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self._unstyled_text):
            raise StopIteration
        elif self.index == 0:
            result = self.style.start_sequence + self._unstyled_text[0]
        elif self.index == len(self) - 1:
            result = self._unstyled_text[self.index] + self.style.end_sequence
        else:
            result = self._unstyled_text[self.index]

        self.index += 1
        return result


class Label(Widget):
    """
    A coloured string of text (any length)
    """
    def __init__(self, text, style=style.Style(), *args, **kwargs):
        self.text = text
        self.style = style
        self.index = 0

        super(self.__class__, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Label text: %r, style: %r, alignment: %r>' % (
            self.text,
            self.style,
            self.alignment
        )

    def __len__(self):
        return len(self.text)

    def __getitem__(self, item):
        if item == 0:
            return self.style.start_sequence + self.text[0]
        elif item == len(self.text) - 1:
            return self.text[item] + self.style.end_sequence
        else:
            return self.text[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.text):
            raise StopIteration
        elif self.index == 0:
            result = self.style.start_sequence + self.text[0]
        elif self.index == len(self.text) - 1:
            result = self.text[self.index] + self.style.end_sequence
        else:
            result = self.text[self.index]

        self.index += 1
        return result

if __name__ == '__main__':
    import time
    from pywinterm.display.util import clear_window
    '''
    row = Row(
        widgets=(
            Label('1234'),
            "56",
            Label('7891')
        )
    )

    print(row)
    print(len(row))

    for char in row:
        print(char)

    for i in range(len(row)):
        print(row[i])
    '''

    tin = TextInput(
        20,
        unfocus_handler=lambda k: print('EXITED WITH KEY:', repr(k)),
        style=style.Style(
            fore=style.foreground.BLUE,
            back=style.background.WHITE#,
            #style=style.BOLD
        )
    )

    print('pre-run')

    print(tin)
    tin.text = 'test'
    #print(tin)

    tin.focus()

    print("Main loop starting...")

    while True:
        #clear_window()

        print(tin)
        print(tin[2:5])

        time.sleep(1)
