import RPi.GPIO as GPIO
import time
from globals import *
from datetime import datetime


class DoorLight:
    def __init__(self, pin):
        self.led_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def turn_on(self):
        print("LED on")
        GPIO.output(self.led_pin, GPIO.HIGH)

    def turn_off(self):
        print("LED off")
        GPIO.output(self.led_pin, GPIO.LOW)


def run(dl, callback, settings,delay,stop_event):
    while True:
        current_time = datetime.now()
        dl_time = get_dl_should_turn_off()
        should_light_up = True
        if dl_time is None:
            should_light_up = False

        elif dl_time < current_time:
            should_light_up = False

        if should_light_up:
            dl.turn_on()
        else:
            dl.turn_off()

        time.sleep(delay)
        callback(settings, should_light_up)
        if stop_event.is_set():
            break
