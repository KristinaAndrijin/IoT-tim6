import RPi.GPIO as GPIO
import time

class PassiveInfraRed:
    def __init__(self, pin, callback):
        self.pir_pin = pin
        self.callback = callback
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pir_pin, GPIO.IN)
    def motion_detected(self):
        self.callback(True)
        # print("You moved")
    def no_motion(self):
        self.callback(False)
        # print("You stopped moving")

    def run(self, delay):
        GPIO.add_event_detect(self.pir_pin, GPIO.RISING, callback=self.motion_detected)
        GPIO.add_event_detect(self.pir_pin, GPIO.FALLING, callback=self.no_motion)
        # input("Press any key to exit...")
        time.sleep(delay)