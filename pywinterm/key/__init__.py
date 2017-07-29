"""
Keyboard related stuff
"""
import msvcrt
import time
import threading
import types


class Key:
    def __init__(self, id, is_special_key=False):
        self.id = id
        self.is_special_key = is_special_key

    def __repr__(self):
        return '<Key id: %r, special: %r>' % (self.id, self.is_special_key)

    def __eq__(self, other):
        if isinstance(other, Key):  # both objects are of Key type, nothing special here...
            return self.id == other.id and self.is_special_key == other.is_special_key

        elif isinstance(other, str) and len(other) == 1:  # if the other key is a string, and this isn't a special key
            if not self.is_special_key:
                return ord(other) == self.id  # see if they represent the same character

        elif isinstance(other, int):
            if not self.is_special_key:  # if the other key is an ord value for a character
                return other == self.id  # see if they represent the same character

    def __str__(self):
        return chr(self.id)


def kbfunc():
    """
    !!DEPRECATED!!
    gets the currently pressed key.
    From: https://stackoverflow.com/questions/5044073/python-cross-platform-listening-for-keypresses
    :return: String or None
    """
    print("WARNING: lu.sys.key.kbfunc() is deprecated, used lu.sys.key.pressed() instead")
    #this is boolean for whether the key has bene hit
    x = msvcrt.kbhit()
    if x:
        #getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = None
    return ret


def pressed():
    """
    Gets the currently pressed key and returns it
    :return: Key
    """
    if msvcrt.kbhit():  # if the key has been hit
        key = ord(msvcrt.getch())
        if key == 224 or key == 0:  # 224 always comes before a special key, 0 appears to come before an F key
            key_2 = ord(msvcrt.getch())
            return Key(key_2, True)
        else:
            return Key(key)


pressed_key = None  # a list of pressed keys for this frame, so that different keys can be checked in the same frame


def get_pressed():
    """
    Gets the currently pressed key and assigns it to a variable for later reference
    :return: None
    """
    global pressed_key
    if pressed_key is None:  # if there is no key already being handled
        pressed_key = pressed()


def key_down(key):
    """
    Checks if key is currently pressed
    :param key: String, Int, Key - the requested key in either form.
    :return: Bool
    """
    get_pressed()
    global pressed_key

    return key == pressed_key


def clear_keypresses():
    """
    To be called at the end of every frame
    :return: None
    """
    global pressed_key
    pressed_key = None


def wait_for_keypress(sleep_time=0.01):
    """
    Blocks until a keypress event occurs
    :return: None
    """
    while not msvcrt.kbhit():
        time.sleep(sleep_time)


class ThreadedKeyListener(threading.Thread):
    """
    A threaded Key Listener which executes a function every time a specific key is pressed
    """
    def __init__(self, stop_event, key_handler=lambda k: None, sleep_time=0.1, *args, **kwargs):
        self.stop_event = stop_event  # threading.Event
        self.key_handler = key_handler  # Executed every time a key is hit with the Key object as it's parameter
        self.sleep_time = sleep_time

        super(ThreadedKeyListener, self).__init__(*args, **kwargs)

    @property
    def do_run(self):
        return not self.stop_event.is_set()  # if it's set, then we have to stop

    def run(self):
        """
        Listen for keys and add them to the Queue when they're pressed.

        Will run until key is pressed, before determining whether to continue execution
        """
        while self.do_run:
            wait_for_keypress(self.sleep_time)
            k = pressed()

            if self.do_run:
                self.key_handler(k)  # execute the key handler


if __name__ == "__main__":
    import time

    X = None

    while X != "H":
        get_pressed()
        if pressed_key:
            print(pressed_key.__repr__())

        X = pressed_key

        clear_keypresses()
        time.sleep(0.01)

    while True:
        get_pressed()

        if key_down("a"):
            print("a")

        if key_down("b"):
            print("b")

        if key_down("c"):
            print("c")

        clear_keypresses()
        time.sleep(0.01)
