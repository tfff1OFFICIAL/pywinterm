"""
Keyboard related stuff
"""
import msvcrt
import time


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
        return '{}{}'.format(chr(self.id), "(special)" if self.is_special_key else "")


def kbfunc():
    """
    !!DEPRECATED!!
    gets the currently pressed key.
    From: https://stackoverflow.com/questions/5044073/python-cross-platform-listening-for-keypresses
    :return: String or None
    """
    print("WARNING: lu.sys.keyboard.kbfunc() is deprecated, used lu.sys.keyboard.pressed() instead")
    #this is boolean for whether the keyboard has bene hit
    x = msvcrt.kbhit()
    if x:
        #getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = None
    return ret


pressed_keys = []  # a list of pressed keys for this frame, so that different keys can be checked in the same frame


def listen_pressed():
    """
    Gets the currently pressed key
    :return: None
    """
    global pressed_keys
    if msvcrt.kbhit():  # if the keyboard has been hit
        key = ord(msvcrt.getch())
        if key == 224 or key == 0:  # 224 always comes before a special key, 0 appears to come before an F key
            key_2 = ord(msvcrt.getch())
            pressed_keys.append(Key(key_2, True))
        else:
            pressed_keys.append(Key(key))


def key_down(key):
    """
    Checks if key is currently pressed
    :param key: String, Int, Key - the requested key in either form.
    :return: Bool
    """
    listen_pressed()
    global pressed_keys
    return key in pressed_keys


def clear_keypresses():
    """
    To be called at the end of every frame
    :return: None
    """
    global pressed_keys
    pressed_keys = []


def wait_for_keypress(sleep_time=0.01):
    """
    Blocks until a keypress event occurs
    :return: None
    """
    while not msvcrt.kbhit():
        time.sleep(sleep_time)


if __name__ == "__main__":
    import time

    while True:
        k = listen_pressed()
        if k:
            print(k.__repr__())
        time.sleep(0.01)
