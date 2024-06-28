#!/usr/bin/env python3

from sensors.auxiliary.PCF8574 import PCF8574_GPIO
from sensors.auxiliary.Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep
from datetime import datetime
from globals import *
import time

class LCD(object):

    def __init__(self,pin_rs,pin_e,pins_db):
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db
        PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        # Create PCF8574 GPIO adapter.
        try:
            mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                print('I2C Address Error !')
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs=self.pin_rs, pin_e=self.pin_e, pins_db=self.pins_db, GPIO=mcp)

    def get_cpu_temp(self):  # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
        tmp = open('/sys/class/thermal/thermal_zone0/temp')
        cpu = tmp.read()
        tmp.close()
        return '{:.2f}'.format(float(cpu) / 1000) + ' C'

    def get_time_now(self):  # get system time
        return datetime.now().strftime('    %H:%M:%S')

    def destroy(self):
        self.lcd.clear()

def run_lcd_loop(lcd_device, delay, callback, stop_event,settings):

    lcd_device.mcp.output(3, 1)  # turn on LCD backlight
    lcd_device.lcd.begin(16, 2)  # set number of LCD lines and columns
    while (True):
        #lcd_device.lcd.clear()
        lcd_device.lcd.setCursor(0, 0)  # set cursor position
        #lcd_device.lcd.message('CPU: ' + lcd_device.get_cpu_temp() + '\n')  # display CPU temperature
        #lcd_device.lcd.message(lcd_device.get_time_now())  # display the time
        message = "hum: " + str(get_gdht_humidity()) + "temp: " + str(get_gdht_temperature())
        lcd_device.lcd.message(message)
        callback(settings, "working_4real")
        if stop_event.is_set():
            lcd_device.destroy()
            break
        sleep(delay)

# if __name__ == '__main__':
#     print ('Program is starting ... ')
#     try:
#         loop()
#     except KeyboardInterrupt:
#         destroy()

