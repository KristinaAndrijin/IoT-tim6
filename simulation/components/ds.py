from simulators.ds import run_ds_simulator
import threading
import time
from components.lock import lock
from globals import *

from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

batch = []
publish_data_counter = 0
publish_data_limit = 5

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ds_callback(opened,ds_settings):
    global publish_data_counter, publish_data_limit
    code = ds_settings["code"]

    temp_payload = {
        "measurement": "Door opened",
        "simulated": ds_settings['simulated'],
        "runs_on": ds_settings["runs_on"],
        "code": ds_settings["code"],
        "value": opened
    }

    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Runs on: {ds_settings['runs_on']}")
            if opened:
                print("Door is opened")
            else:
                print("Door is closed")

            batch.append(('Door opened', json.dumps(temp_payload), 0, True))
            publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()



def run_ds(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_ds_simulator, args=(2, ds_callback, stop_event,settings))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.ds import DoorSensor
        print("Starting " + code + " sensor")
        door_sensor = DoorSensor(settings['pin'])  # Adjust this based on your hardware setup
        thread = threading.Thread(target=door_sensor.run, args=(2, ds_callback, stop_event,settings))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
