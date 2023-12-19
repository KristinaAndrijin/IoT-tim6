import RPi.GPIO as GPIO
import time
class DoorMembraneSwitch:

    def __init__(self, settings):
    # these GPIO pins are connected to the keypad
    # change these according to your connections!
        self.R1 = int(settings['R1'])
        self.R2 = int(settings['R2'])
        self.R3 = int(settings['R3'])
        self.R4 = int(settings['R4'])

        self.C1 = int(settings['C1'])
        self.C2 = int(settings['C2'])
        self.C3 = int(settings['C3'])
        self.C4 = int(settings['C4'])

        # Initialize the GPIO pins

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        # Make sure to configure the input pins to use the internal pull-down resistors

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # The readLine function implements the procedure discussed in the article
    # It sends out a single pulse to one of the rows of the keypad
    # and then checks each column for changes
    # If it detects a change, the user pressed the button that connects the given line
    # to the detected column

    def readLine(self, line, characters, callback,settings):
        GPIO.output(line, GPIO.HIGH)
        if (GPIO.input(self.C1) == 1):
            callback(characters[0],settings)
        if (GPIO.input(self.C2) == 1):
            callback(characters[1],settings)
        if (GPIO.input(self.C3) == 1):
            callback(characters[2],settings)
        if (GPIO.input(self.C4) == 1):
            callback(characters[3],settings)
        GPIO.output(line, GPIO.LOW)

    def run(self, delay, callback, stop_event, settings):
        while True:
            # call the readLine function for each row of the keypad
            self.readLine(self.R1, ["1", "2", "3", "A"], callback,settings)
            self.readLine(self.R2, ["4", "5", "6", "B"], callback,settings)
            self.readLine(self.R3, ["7", "8", "9", "C"], callback,settings)
            self.readLine(self.R4, ["*", "0", "#", "D"], callback,settings)
            if stop_event.is_set():
                break
            time.sleep(delay)
