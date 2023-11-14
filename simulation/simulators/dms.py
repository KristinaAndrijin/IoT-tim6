import time
import random


def generate_values():
    while True:
        character_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', '*', '#']
        random_character = random.choice(character_list)
        yield random_character


def run_dms_simulator(delay, callback, stop_event, code):
    for value in generate_values():
        time.sleep(delay)
        callback(value, code)
        if stop_event.is_set():
            break
