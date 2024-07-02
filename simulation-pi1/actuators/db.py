import RPi.GPIO as GPIO
import time
from globals import *

class DoorBuzzer:
    def __init__(self, pin):
        self.buzzer_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

    def buzz(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.buzzer_pin, True)
            time.sleep(delay)
            GPIO.output(self.buzzer_pin, False)
            time.sleep(delay)

def run(db,callback,settings,delay,stop_event):

    while True:
        should_buzz = False
        if get_is_alarm_on() or get_is_ds_alarm_on() or is_dms_alarm_on() or is_rpir_alarm_on():
            should_buzz = True

        pitch = 440
        duration = 1.5
        db.buzz(pitch, duration)
        callback(should_buzz,settings)
        set_threads_done()

        if stop_event.is_set():
            break
        time.sleep(delay)



