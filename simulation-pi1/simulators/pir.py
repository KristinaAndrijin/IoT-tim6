import time
import random


def generate_values():
    while True:
        yield True if random.randint(0, 100) > 70 else False


def run_pir_simulator(delay, callback, stop_event, settings):
    for motion in generate_values():
        time.sleep(delay)
        callback(motion, settings)
        if stop_event.is_set():
            break
