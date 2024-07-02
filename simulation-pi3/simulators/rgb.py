import time
import random
from globals import *

def generate_values():
    while True:
        yield get_rgb_colors()


def run_rgb_simulator(delay, callback, stop_event, settings):
    for v in generate_values():
        time.sleep(delay)
        callback(settings, v)
        if stop_event.is_set():
            break
