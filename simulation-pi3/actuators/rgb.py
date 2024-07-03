import RPi.GPIO as GPIO
import time
from globals import *


class RGBLight:
    def __init__(self, red_pin,green_pin,blue_pin):
        GPIO.setmode(GPIO.BCM)

        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        # set pins as outputs
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def turnOff(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)

    def setColor(self,red,blue,green):
        if (red):
            gpio_red = GPIO.HIGH
        else:
            gpio_red = GPIO.LOW

        if (blue):
            gpio_blue = GPIO.HIGH
        else:
            gpio_blue = GPIO.LOW

        if (green):
            gpio_green = GPIO.HIGH
        else:
            gpio_green = GPIO.LOW

        GPIO.output(self.red_pin, gpio_red)
        GPIO.output(self.blue_pin, gpio_blue)
        GPIO.output(self.green_pin, gpio_green)


def run(delay,rgb, callback, settings,stop_event):

    while True:
        colors = get_rgb_colors()
        rgb.setColor(colors[0], colors[1], colors[2])
        callback(settings, colors)
        set_threads_done()

        if stop_event.is_set():
            break
        time.sleep(delay)

