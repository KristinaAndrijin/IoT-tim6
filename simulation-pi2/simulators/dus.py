import time
import random

def generate_values():
    while True:
        motion = random.randint(0, 10)
        if motion > 3:
            distance = random.randint(1, 100)
            yield distance

      

def run_dus_simulator(delay, callback, stop_event,settings):
        for value in generate_values():
            time.sleep(delay)
            callback(value,settings)
            if stop_event.is_set():
                  break
              