import RPi.GPIO as GPIO
import time


class DoorLight:
    def __init__(self, pin):
        self.led_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def switch(self):
        print("LED on")
        GPIO.output(self.led_pin, GPIO.HIGH)
        time.sleep(1)
        print("LED off")
        GPIO.output(self.led_pin, GPIO.LOW)


def run(dl):
    dl.switch()
    time.sleep(1)
