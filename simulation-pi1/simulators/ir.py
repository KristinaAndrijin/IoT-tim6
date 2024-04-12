import time
import random

def generate_values():
    buttonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]
    while True:
        yield random.choice(buttonsNames)

def run_ir_simulator(delay, callback, stop_event,settings):
        for v in generate_values():
            time.sleep(delay)
            callback(v,settings)
            if stop_event.is_set():
                  break
              