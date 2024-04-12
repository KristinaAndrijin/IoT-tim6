import json
import threading

from broker_settings import HOSTNAME, PORT
from components.gyro import run_gyro
from components.ir import run_ir
from components.rgb import run_rgb
from components.sd import run_sd
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from components.dus import run_dus
from components.dms import run_dms
from components.pir import run_pir
from components.db import run_db
from components.dl import run_dl
from components.lock import actuator_lock
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
    client.subscribe("PI1")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: process_server_message(msg.topic, json.loads(msg.payload.decode('utf-8')))

def process_server_message(topic,data):
    print("aaaaaaaaaaaaaaa",topic,data)

def run_sensors(settings, threads, stop_event):
    # DHT
    dht1_settings = settings['RDHT1']
    run_dht(dht1_settings, threads, stop_event)
    dht2_settings = settings['RDHT2']
    run_dht(dht2_settings, threads, stop_event)

    # DS
    ds1_settings = settings['DS1']
    run_ds(ds1_settings,threads,stop_event)

    # DUS
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event)

    # DMS
    dms_settings = settings['DMS']
    run_dms(dms_settings, threads, stop_event)

    # DPIR
    dpir_settings = settings['DPIR1']
    run_pir(dpir_settings, threads, stop_event)

    # RPIR
    rpir_settings = settings['RPIR1']
    run_pir(rpir_settings, threads, stop_event)
    rpir_settings = settings['RPIR2']
    run_pir(rpir_settings, threads, stop_event)

    # LCD
    lcd_settings = settings['LCD']
    run_lcd(lcd_settings, threads, stop_event)

    # SD
    sd_settings = settings['B4SD']
    run_sd(sd_settings, threads, stop_event)

    # BIR
    bir_settings = settings['BIR']
    run_ir(bir_settings, threads, stop_event)

    # GSG
    gsg_settings = settings['GSG']
    run_gyro(gsg_settings, threads, stop_event)

def open_menu():
    global is_menu_opened
    with actuator_lock:
        print("Menu contents:")
        print("1. Start buzzing")
        print("2. Switch led state")
        print("3. Switch RGB state")
        # print("3. Option 3")
        print("Enter 'x' to close the menu.")

        user_input = input(" >> ").lower()

        if user_input == 'x':
            set_is_menu_opened(False)
        elif user_input == '1':
            db_settings = settings['DB']
            run_db(db_settings, threads, stop_event)
            wait_for_threads()
        elif user_input == '2':
            dl_settings = settings['DL']
            run_dl(dl_settings, threads, stop_event)
            wait_for_threads()
        elif user_input == '3':
            brgb_settings = settings['BRGB']
            run_rgb(brgb_settings, threads, stop_event)
            wait_for_threads()
        else:
            print("Invalid input. Try again.")

def send_setup_to_server():
    pi_name = "PI1"
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
            if not get_is_menu_opened():
                user_input = input("Enter 'm' to open the menu: ").lower()

                if user_input == 'm':
                    set_is_menu_opened(True)
                else:
                    time.sleep(2)
            else:
                open_menu()

    except KeyboardInterrupt:
        print("=" * 20)
        print('Stopping app')
        for t in threads:
            stop_event.set()

        for t in threads:
            t.join()

        print("=" * 20)
        print("App successfully stopped")