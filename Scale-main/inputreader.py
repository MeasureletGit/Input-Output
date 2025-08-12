import os
import subprocess as sp
from pynput.keyboard import Key, Listener

global buffer, mypath
buffer = ''
mypath =  os.path.dirname(os.path.realpath(__file__))+os.sep

def on_press(c):
    global buffer, mypath
    if not c is None:
        c = str(c)
        if len(c) == 3:
            c = c[1]  # fx 'a' -> a
        if c == 'Key.enter':
            with open(mypath + "measurelet.ID", 'w') as f:
                if len(buffer) > 1 and buffer[1] == '#':
                    with open(mypath + "scanner.txt", 'w') as s:
                        s.write(buffer[0])
                    buffer = buffer[2:]
                f.write(buffer)
            buffer = ""
        elif c == 'Key.left':
            sp.call(["sudo", "killall", "-9", "python"])
            sp.call(["sudo", "killall", "-9", "python3"])
        elif len(c) == 1 and (c.isalnum() or c in ('#', ',')):
            buffer += c


def on_release(key):
    pass

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
