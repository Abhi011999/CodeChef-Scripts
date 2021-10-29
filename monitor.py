import sys
import time
import logging
import coloredlogs
from reloader import Loader

INIT_MSG = """
Reloader starting...

Save your changes on your editor to automatically reload.

Script will be restarted if you -
1. press `r` key
2. save your script file on your editor
3. save your input file on your editor
"""


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    logging.info(INIT_MSG)
    # coloredlogs.install(level="DEBUG")
    script = Loader(sys.argv[1], "in.txt", frequency=0.05)

    while True:
        # Check if script has been modified since last poll.
        if script.has_changed():
            # Execute start function from script if it has been modified.
            script.start()
        time.sleep(0.05)
