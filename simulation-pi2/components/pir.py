from simulators.pir import run_pir_simulator
import threading
import time
from components.lock import lock
from globals import *
from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

pir_batch = []
publish_data_counter = 0
publish_data_limit = 1
#counter_lock = threading.Lock()

def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        if not get_is_menu_opened():
            print(f'published {publish_data_limit} pir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def pir_callback(motion, pir_settings):
    global publish_data_counter, publish_data_limit
    character_payload = {
        "measurement": "Motion",
        "simulated": pir_settings['simulated'],
        "runs_on": pir_settings["runs_on"],
        "code": pir_settings["code"],
        "value": motion
    }

    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {pir_settings['code']}")
            if motion:
                print("Movement detected")
            else:
                print("No movement")
            print(f"Runs on: {pir_settings['runs_on']}")

        pir_batch.append(('Motion', json.dumps(character_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_pir(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event, settings))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.pir import PassiveInfraRed
        print("Starting " + code + " sensor")
        pir_sensor = PassiveInfraRed(settings['pin'], pir_callback, settings)
        thread = threading.Thread(target=pir_sensor.run, args=(2, ))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
