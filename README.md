# pywinterm
[Windows Only] A tiny library for doing some basic terminal control and keyhandling in Python

## Installation

1. Download or clone this repo.
2. In the containing folder of the containing directory, open an elevated terminal and enter:
```
pip install git+https://github.com/tfff1OFFICIAL/pywinterm.git@master
```

## Quickstart

A basic application to count the number of times 'x' was pressed could be made like:

```python
import time
from pywinterm import key
from pywinterm.display import RootDisplay

root = RootDisplay("key counter")

def run():
  root.print("x pressed: 0 times so far")
  
  key.clear_keypresses()
  
  counter = 0
  
  while True:
    root.render()
    key.wait_for_keypress()
    if key.key_down("x"):
      root.clear()
      counter += 1
      root.print("x pressed: {} times so far".format(counter))

if __name__ == "__main__":
  run()
```
