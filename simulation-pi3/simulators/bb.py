import time
import random
from globals import *


def run_bb_simulator(delay, callback, stop_event,settings):
        while True:
            should_buzz = False
            if get_is_alarm_on() or get_is_ds_alarm_on() or is_dms_alarm_on() or is_rpir_alarm_on():
                should_buzz = True
            time.sleep(delay)
            callback(should_buzz,settings)
            if stop_event.is_set():
                  break
              