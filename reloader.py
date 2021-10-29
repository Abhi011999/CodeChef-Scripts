import os
import sys
import time
import hashlib
import logging
import importlib
import subprocess
import coloredlogs
from threading import Thread
from pynput import keyboard

LOGGER = logging.getLogger("hot_reload")
# coloredlogs.install(level="DEBUG", logger=LOGGER)
get_time = lambda: time.time()


class Monitor(Thread):
    """
    Monitors for changes in both the script and input file and
    notifies the loader if hash change is detected.
    """

    def __init__(self, loader, frequency):
        super().__init__()

        self.frequency = frequency
        self.loader = loader

        self.daemon = True

    def run(self):
        while True:
            with open(self.loader.source) as file:
                fingerprint = hashlib.sha1(file.read().encode("utf-8")).hexdigest()

            with open(self.loader.input_file) as file:
                fingerprint_input_file = hashlib.sha1(
                    file.read().encode("utf-8")
                ).hexdigest()

            if fingerprint != self.loader.fingerprint:
                self.loader.notify(fingerprint)

            if fingerprint_input_file != self.loader.fingerprint_input_file:
                self.loader.notify_input_file(fingerprint_input_file)

            time.sleep(self.frequency)


class Loader:
    def __init__(self, source, input_file, frequency=1):
        """
        Handles the reloading of the script.

        Args:
            source (str): Script file name
            input_file (str): Input file name
            frequency (int, optional): Frequency of polling. Defaults to 1.
        """
        
        self.source = source
        self.input_file = input_file
        self.__name = os.path.splitext(self.source)[0]
        self.module = importlib.import_module(self.__name)
        self.__process = None
        self.fingerprint = None
        self.fingerprint_input_file = None

        self.changed = False

        monitor = Monitor(self, frequency)
        monitor.start()

        listener = keyboard.Listener(on_press=self.notify_key_press)
        listener.start()

    def notify_key_press(self, key):
        try:
            if key.char == "r":
                LOGGER.info("Reload key pressed, reloading...")
                self.changed = True
        except:
            pass

    def notify(self, fp):
        self.fingerprint = fp
        LOGGER.info(
            f"Script change detected, fingerprint changed to {fp[:7]}, reloading..."
        )
        self.changed = True

    def notify_input_file(self, fp):
        self.fingerprint_input_file = fp
        LOGGER.info(
            f"Input file change detected, fingerprint changed to {fp[:7]}, reloading..."
        )
        self.changed = True

    def has_changed(self):
        if self.changed:
            self.changed = False
            return True
        else:
            return False

    def start(self):
        try:
            reload_time_start = get_time()
            # if self.__process != None and self.__process.poll() is None:
            #     LOGGER.info("Identical process already running, restarting...")
            #     self.__process.kill()
            #     self.__process.wait()
            self.__process = subprocess.call([sys.executable, self.source])
            reload_time_stop = get_time()
            reload_time_elapsed = reload_time_stop - reload_time_start
            LOGGER.info(f"Reload complete in {reload_time_elapsed:.3f} secs.")
        except Exception as e:
            LOGGER.error(f"Reload failed. {e}")

    def __getattr__(self, attr):
        return getattr(self.module, attr)
