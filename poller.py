"""
Most of the code in this file is taken from the following source:
https://stackoverflow.com/a/31736883/5049559

Modified to work with Python 3.6 and run asynchronously.
"""

import os
import time
from threading import Thread

IS_WINDOWS = os.name == "nt"

if IS_WINDOWS:
    from win32api import STD_INPUT_HANDLE
    from win32console import (
        GetStdHandle,
        KEY_EVENT,
        ENABLE_ECHO_INPUT,
        ENABLE_LINE_INPUT,
        ENABLE_PROCESSED_INPUT,
    )
else:
    import sys
    import select
    import termios


class KeyPoller(Thread):
    def __init__(self, on_press=None):
        super().__init__()

        self.on_press = on_press
        self.daemon = True

        if IS_WINDOWS:
            self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
            self.readHandle.SetConsoleMode(
                ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT | ENABLE_PROCESSED_INPUT
            )

            self.curEventLength = 0
            self.curKeysLength = 0

            self.capturedChars = []
        else:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

    def __exit__(self, type, value, traceback):
        if not IS_WINDOWS:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        if IS_WINDOWS:
            if len(self.capturedChars) != 0:
                return self.capturedChars.pop(0)

            eventsPeek = self.readHandle.PeekConsoleInput(10000)

            if len(eventsPeek) == 0:
                return None

            if len(eventsPeek) != self.curEventLength:
                for curEvent in eventsPeek[self.curEventLength :]:
                    if (
                        curEvent.EventType == KEY_EVENT
                        and ord(curEvent.Char) != 0
                        and curEvent.KeyDown
                    ):
                        curChar = str(curEvent.Char)
                        self.capturedChars.append(curChar)
                self.curEventLength = len(eventsPeek)

            if len(self.capturedChars) != 0:
                return self.capturedChars.pop(0)
            else:
                return None
        else:
            dr, dw, de = select.select([sys.stdin], [], [], 0)
            if dr != []:
                return sys.stdin.read(1)
            return None

    def run(self):
        while True:
            k = self.poll()
            if k is not None:
                self.on_press(k)
            time.sleep(0.01)

