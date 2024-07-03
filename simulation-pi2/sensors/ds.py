import RPi.GPIO as GPIO
import time

class DoorSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_door_state(self):
        return GPIO.input(self.pin)

    def run(self, delay, callback, stop_event,settings):
        while True:
            state = self.read_door_state()
            callback(state,settings)
            if stop_event.is_set():
                break
            time.sleep(delay)
