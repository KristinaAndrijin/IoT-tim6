from simulators.dms import run_dms_simulator
import threading
import time
from components.lock import lock
from globals import *
from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

dms_batch = []
publish_data_counter = 0
publish_data_limit = 5
#counter_lock = threading.Lock()

def publisher_task(event, dms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_dms_batch = dms_batch.copy()
            publish_data_counter = 0
            dms_batch.clear()
        publish.multiple(local_dms_batch, hostname=HOSTNAME, port=PORT)
        if not get_is_menu_opened():
            print(f'published {publish_data_limit} dms values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dms_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dms_callback(character, dms_settings):
    global publish_data_counter, publish_data_limit
    character_payload = {
        "measurement": "Character",
        "simulated": dms_settings['simulated'],
        "runs_on": dms_settings["runs_on"],
        "code": dms_settings["code"],
        "value": character
    }
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {dms_settings['code']}")
            print(f"Character: " + str(character))
            print(f"Runs on: {dms_settings['runs_on']}")

        dms_batch.append(('Character', json.dumps(character_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dms(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_dms_simulator, args=(2, dms_callback, stop_event, settings))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.dms import DoorMembraneSwitch
        print("Starting " + code + " sensor")
        dms_sensor = DoorMembraneSwitch(settings)
        thread = threading.Thread(target=dms_sensor.run, args=(2, dms_callback, stop_event,settings))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
