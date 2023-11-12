import RPi.GPIO as GPIO
import time


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


def run(db):
    pitch = 440
    duration = 0.1
    db.buzz(pitch, duration)
    time.sleep(1)
