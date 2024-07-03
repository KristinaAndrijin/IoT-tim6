import RPi.GPIO as GPIO
import time
from globals import *

class SegmentDisplay(object):

    def __init__(self,segments, digits):
        GPIO.setmode(GPIO.BCM)
        #originalno (11, 4, 23, 8, 7, 10, 18, 25)
        self.segments = segments
        #originalno (22, 27, 17, 24)
        self.digits = digits

        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        for digit in digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

        self.num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}


def run_4sd_loop(sd_device, delay, callback, stop_event,settings):
    try:
        if check_timer():
            if get_is_sd_working():
                n = time.ctime()[11:13] + time.ctime()[14:16]
            else:
                n = " "*4
            set_is_sd_working(not get_is_sd_working())

        else:
            n = time.ctime()[11:13] + time.ctime()[14:16]

        s = str(n).rjust(4)

        while True:
            for digit in range(4):
                for loop in range(0, 7):
                    GPIO.output(sd_device.segments[loop], sd_device.num[s[digit]][loop])
                    if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                        # GPIO.output(25, 1)
                        GPIO.output(sd_device.segments[7],1)
                    else:
                        #GPIO.output(25, 0)
                        GPIO.output(sd_device.segments[7], 0)
                GPIO.output(sd_device.digits[digit], 0)
                time.sleep(0.001)
                GPIO.output(sd_device.digits[digit], 1)

            callback(settings, "working_4real")
            if stop_event.is_set():
                break
            time.sleep(delay)
    finally:
        GPIO.cleanup()

