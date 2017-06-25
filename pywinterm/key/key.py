"""
Constants for the characters returned by special keys.
"""
from pywinterm.key import Key

sKey = lambda x: Key(x, True)  # shorthand for a special key

# General Keys
ESCAPE  = Key(27)
RETURN  = Key(13)
TAB     = Key(9)

# Arrow Keys
UP      = sKey(72)
DOWN    = sKey(80)
LEFT    = sKey(75)
RIGHT   = sKey(77)

# Utility keys
DELETE    = sKey(83)
INSERT    = sKey(82)
HOME      = sKey(71)
PAGE_UP   = sKey(73)
PAGE_DOWN = sKey(81)
END       = sKey(79)

# F keys
F1  = sKey(59)
F2  = sKey(60)
F3  = sKey(61)
F4  = sKey(62)
F5  = sKey(63)
F6  = sKey(64)
F7  = sKey(65)
F8  = sKey(66)
F9  = sKey(67)
F10 = sKey(68)
F12 = sKey(134)
