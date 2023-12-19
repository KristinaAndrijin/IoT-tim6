import RPi.GPIO as GPIO
import time
from globals import *


class DoorLight:
    def __init__(self, pin):
        self.led_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def switch(self):
        if led_is_on():
            print("LED on")
            GPIO.output(self.led_pin, GPIO.HIGH)
            set_led_state(True)
        else:
            print("LED off")
            GPIO.output(self.led_pin, GPIO.LOW)
            set_led_state(False)


def run(dl, callback, settings):
    dl.switch()
    # time.sleep(1)
    callback(settings)
    set_threads_done()
