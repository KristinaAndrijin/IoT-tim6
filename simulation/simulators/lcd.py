import time
import random

def generate_values():
      while True:
            yield "working"

def run_lcd_simulator(delay, callback, stop_event,settings):
        for v in generate_values():
            time.sleep(delay)
            callback(settings,v)
            if stop_event.is_set():
                  break
              