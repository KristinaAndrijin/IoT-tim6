import json
import threading

from broker_settings import HOSTNAME, PORT
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from components.dus import run_dus
from components.dms import run_dms
from components.pir import run_pir
from components.db import run_db
from components.dl import run_dl
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
    client.subscribe("n_people")
    client.subscribe("raise_alarm_ds_pi1")
    client.subscribe("turn_alarm_off_ds_pi1")
    client.subscribe("raise_alarm_dms_ds_pi1")
    client.subscribe("turn_off_alarm_dms_ds_pi1")
    client.subscribe("raise_alarm_rpir_pi1")
    client.subscribe("turn_alarm_off_rpir_pi1")
    client.subscribe("raise_alarm_gyro_pi1")
    client.subscribe("turn_alarm_off_gsg_pi1")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: process_server_message(msg.topic, json.loads(msg.payload.decode('utf-8')))

def process_server_message(topic,data):
    if topic == "n_people":
        if data["n_people"]:
            set_num_of_people(data["n_people"])
            print("skrapapa",get_num_of_people())
    if topic == "raise_alarm_ds_pi1":
        which_ds = data["ds"]
        print("ALARM DS" + str(which_ds))
        set_is_ds_alarm_on(True)
        set_ds_trigger(which_ds)
    if topic == "turn_alarm_off_ds_pi1":
        which_ds = data["ds"]
        if get_ds_trigger() == which_ds:
            print("ALARM DS" + str(which_ds) + " TURNED OFF")
            set_is_ds_alarm_on(False)
    if topic == "raise_alarm_dms_ds_pi1":
        print("DMS ALARM")
        set_dms_alarm_on(True)
    if topic == "turn_off_alarm_dms_ds_pi1":
        print("DMS ALARM IS TURNED OFF")
        set_dms_alarm_on(False)
    if topic == "raise_alarm_rpir_pi1":
        print("RPIR ALARM")
        set_rpir_alarm_on(True)
    if topic == "turn_alarm_off_rpir_pi1":
        print("RPIR ALARM TURNED OFF")
        set_rpir_alarm_on(False)
    if topic == "raise_alarm_gyro_pi1":
        print("GYYRO ALARM")
        set_gyro_alarm_on(True)
    if topic == "turn_alarm_off_gsg_pi1":
        print("GYYRO ALARM TURNED OFF")
        set_gyro_alarm_on(False)



def switch_dl():
    dl_settings = settings['DL']
    run_dl(dl_settings, threads, stop_event)
    wait_for_threads()
    # stop_event.set()
    # time.sleep(duration)
    # stop_event.clear()
    # run_dl(dl_settings, threads, stop_event)
    # wait_for_threads()


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

    # DB
    db_settings = settings['DB']
    run_db(db_settings, threads, stop_event)

    # DL
    dl_settings = settings['DL']
    run_dl(dl_settings, threads, stop_event)

def open_menu():
    global is_menu_opened
    global is_alarm_on
    with actuator_lock:
        print("Menu contents:")
        print("1. Start buzzing")
        print("2. Switch led state")
        # print("3. Option 3")
        print("Enter 'x' to close the menu.")

        user_input = input(" >> ").lower()

        if user_input == 'x':
            pass
            set_is_menu_opened(False)
        elif user_input == '1':
            pass
            #db_settings = settings['DB']
            #run_db(db_settings, threads, stop_event)
            #wait_for_threads()
        elif user_input == '2':
            pass
            #dl_settings = settings['DL']
            #run_dl(dl_settings, threads, stop_event)
            #wait_for_threads()
        elif user_input == '3':
            iao = get_is_alarm_on()
            xd = True
            if iao:
                xd = False
            print("aaaaaaaa")
            print(iao,xd)
            set_is_alarm_on(xd)
            print(get_is_alarm_on(),xd)
            print("bbbbbbbb")
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