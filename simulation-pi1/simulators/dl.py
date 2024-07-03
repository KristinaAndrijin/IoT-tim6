import time
import random
from globals import *
from datetime import datetime

def run_dl_simulator(delay, callback, stop_event,settings):
        while True:
            current_time = datetime.now()
            dl_time = get_dl_should_turn_off()
            should_light_up = True
            if dl_time is None:
                should_light_up = False

            elif dl_time < current_time:
                should_light_up = False

            time.sleep(delay)
            callback(settings,should_light_up)
            if stop_event.is_set():
                  break
              