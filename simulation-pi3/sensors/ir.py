
import RPi.GPIO as GPIO
import time

# -----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
# ------------------------------------------------------------#
# Imports modules
import RPi.GPIO as GPIO
from datetime import datetime
import time

class InfraRed(object):
	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.IN)

		self.buttons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897,
				   0x300ff02fd,
				   0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd,
				   0x300ff4ab5,
				   0x300ff52ad]  # HEX code list
		self.buttonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
						"#"]  # String list in same order as HEX list

	def getBinary(self):
		# Internal vars
		num1s = 0  # Number of consecutive 1s read
		binary = 1  # The binary value
		command = []  # The list to store pulse times in
		previousValue = 0  # The last value
		value = GPIO.input(self.pin)  # The current value

		# Waits for the sensor to pull pin low
		while value:
			time.sleep(0.0001)  # This sleep decreases CPU utilization immensely
			value = GPIO.input(self.pin)

		# Records start time
		startTime = datetime.now()

		while True:
			# If change detected in value
			if previousValue != value:
				now = datetime.now()
				pulseTime = now - startTime  # Calculate the time of pulse
				startTime = now  # Reset start time
				command.append((previousValue, pulseTime.microseconds))  # Store recorded data

			# Updates consecutive 1s variable
			if value:
				num1s += 1
			else:
				num1s = 0

			# Breaks program when the amount of 1s surpasses 10000
			if num1s > 10000:
				break

			# Re-reads pin
			previousValue = value
			value = GPIO.input(self.pin)

		# Converts times to binary
		for (typ, tme) in command:
			if typ == 1:  # If looking at rest period
				if tme > 1000:  # If pulse greater than 1000us
					binary = binary * 10 + 1  # Must be 1
				else:
					binary *= 10  # Must be 0

		if len(str(binary)) > 34:  # Sometimes, there is some stray characters
			binary = int(str(binary)[:34])

		return binary

	# Convert value to hex
	def convertHex(self,binaryValue):
		tmpB2 = int(str(binaryValue), 2)  # Temporarely propper base 2
		return hex(tmpB2)

def run_ir_loop(ir, delay, callback, stop_event, settings):
	while True:
		inData = ir.convertHex(ir.getBinary())
		for button in range(len(ir.buttons)):
			if hex(ir.buttons[button]) == inData:
				callback(ir.buttonsNames[button], settings)
		if stop_event.is_set():
			break
		time.sleep(delay)