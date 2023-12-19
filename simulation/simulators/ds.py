import time
import random

def generate_values(initial_opened = False):
      opened = initial_opened
      while True:
            random_val = random.randint(0, 10)
            if random_val < 2:
                opened = not opened
            yield opened

      

def run_ds_simulator(delay, callback, stop_event,settings):
        for value in generate_values():
            time.sleep(delay)
            callback(value,settings)
            if stop_event.is_set():
                  break
              