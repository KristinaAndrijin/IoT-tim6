import json
import threading

from broker_settings import HOSTNAME, PORT
from components.gyro import run_gyro
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from components.dus import run_dus
from components.pir import run_pir
from components.lcd import run_lcd
import paho.mqtt.publish as publish
from globals import *
import time
import paho.mqtt.client as mqtt

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

is_menu_opened = False

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    client.subscribe("PI2")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: process_server_message(msg.topic, json.loads(msg.payload.decode('utf-8')))
pir_expiry_time = None

def process_server_message(topic,data):
    global pir_expiry_time
    global lcd_message
    global lcd_should_change
        # @TODO Vlada getter
    if data["for"] == "glcd":
        lcd_message = data["lcd_message"]
        lcd_should_change = True


def run_sensors(settings, threads, stop_event):
    # DHT
    dht1_settings = settings['RDHT3']
    run_dht(dht1_settings, threads, stop_event)

    dht1_settings = settings['GDHT']
    run_dht(dht1_settings, threads, stop_event)

    # DS
    ds1_settings = settings['DS2']
    run_ds(ds1_settings,threads,stop_event)

    # DUS
    dus1_settings = settings['DUS2']
    run_dus(dus1_settings, threads, stop_event)

    # DPIR
    dpir_settings = settings['DPIR2']
    run_pir(dpir_settings, threads, stop_event)

    # RPIR
    rpir_settings = settings['RPIR3']
    run_pir(rpir_settings, threads, stop_event)

    # LCD
    lcd_settings = settings['GLCD']
    run_lcd(lcd_settings, threads, stop_event)

    # GSG
    gsg_settings = settings['GSG']
    run_gyro(gsg_settings, threads, stop_event)

def send_setup_to_server():
    pi_name = "PI2"
    settings = load_settings()

    payload = {
        "pi_name": pi_name,
        "devices": settings
    }

    json_payload = json.dumps(payload)

    publish.single("setup", json_payload, hostname=HOSTNAME, port=PORT)



if __name__ == "__main__":
    print('Starting app')
    #mozda bi trebalo posle kreiranja threadova
    send_setup_to_server()
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        run_sensors(settings, threads, stop_event)
        while True:
            user_input = input("Enter 'm' to open the menu: ").lower()

            if user_input == 'm':
                set_is_menu_opened(True)
            else:
                time.sleep(2)

    except KeyboardInterrupt:
        print("=" * 20)
        print('Stopping app')
        for t in threads:
            stop_event.set()

        for t in threads:
            t.join()

        print("=" * 20)
        print("App successfully stopped")