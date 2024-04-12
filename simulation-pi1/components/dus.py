from simulators.dus import run_dus_simulator
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
        if not get_is_menu_opened():
            print(f'published {publish_data_limit} ds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dus_callback(distance, dus_settings):
    global publish_data_counter, publish_data_limit
    code = dus_settings["code"]

    payload = {
        "measurement": "Distance",
        "simulated": dus_settings['simulated'],
        "runs_on": dus_settings["runs_on"],
        "code": dus_settings["code"],
        "value": distance
    }

    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Distance: " + str(distance) + " cm")
            print(f"Runs on: {dus_settings['runs_on']}")

        batch.append(('Distance', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dus(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_dus_simulator, args=(2, dus_callback, stop_event, settings))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.dus import DistanceSensor
        print("Starting " + code + " sensor")
        dus_sensor = DistanceSensor(settings['trig_pin'], settings['echo_pin'])
        thread = threading.Thread(target=dus_sensor.run, args=(2, dus_callback, stop_event, settings))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
