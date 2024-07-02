import json
import threading
from datetime import datetime

from broker_settings import HOSTNAME, PORT
from components.ir import run_ir
from components.rgb import run_rgb
from components.sd import run_sd
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.db import run_db
from components.lock import actuator_lock
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
    client.subscribe("PI3")
    client.subscribe("rgb")
    client.subscribe("set_timer")
    client.subscribe("timer_off")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: process_server_message(msg.topic, json.loads(msg.payload.decode('utf-8')))

def process_server_message(topic,data):
    if topic == "rgb":
        if data["rgb"]:
            set_rgb_colors(data["rgb"])
            print("rgb vrednosti sa weba",get_rgb_colors())
            set_is_color_changed(True)

    if topic == "set_timer":
        if data["time"]:
            str_datetime = data["time"]
            parsed_datetime = datetime.fromisoformat(str_datetime.replace('Z', '+00:00'))
            set_is_timer_on(True)
            set_timer_time(parsed_datetime)
            print("timer je postavljen: ",get_timer_time())

    if topic == "timer_off":
        if data["state"]:
            set_is_timer_on(False)
            set_timer_time(None)
            print("timer je isključen")



def run_sensors(settings, threads, stop_event):
    # DHT
    dht1_settings = settings['RDHT4']
    run_dht(dht1_settings, threads, stop_event)

    # RPIR
    rpir_settings = settings['RPIR4']
    run_pir(rpir_settings, threads, stop_event)

    # SD
    sd_settings = settings['B4SD']
    run_sd(sd_settings, threads, stop_event)

    # BIR
    bir_settings = settings['BIR']
    run_ir(bir_settings, threads, stop_event)

    rgb_settings = settings['BRGB']
    run_rgb(rgb_settings, threads, stop_event)

def open_menu():
    global is_menu_opened
    with actuator_lock:
        print("Menu contents:")
        print("1. Start buzzing")
        print("2. Switch RGB state")
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