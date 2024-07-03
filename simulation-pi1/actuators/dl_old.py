import RPi.GPIO as GPIO
import time
from globals import *


class DoorLight:
    def __init__(self, pin):
        self.led_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def switch(self):
        print("LED on")
        GPIO.output(self.led_pin, GPIO.HIGH)
        time.sleep(10)
        print("LED off")
        GPIO.output(self.led_pin, GPIO.LOW)


def run(dl, callback, settings):
    dl.switch()
    # time.sleep(1)
    callback(settings)
    set_threads_done()
