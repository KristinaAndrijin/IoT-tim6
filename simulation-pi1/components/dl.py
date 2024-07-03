import threading
import time
from components.lock import lock
from globals import *
from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

from simulators.dl import run_dl_simulator

dl_batch = []
publish_data_counter = 0
publish_data_limit = 2
#counter_lock = threading.Lock()

def publisher_task(event, dl_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_dl_batch = dl_batch.copy()
            publish_data_counter = 0
            dl_batch.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        #print(f'published {publish_data_limit} dl values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dl_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dl_callback(dl_settings,value):
    global publish_data_counter, publish_data_limit
    with lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {dl_settings['code']}")
        if value is True:
            print("LED turned ON")
        else:
            print("LED turned OFF")
        set_led_state(value)

        light_state_payload = {
            "measurement": "LightState",
            "simulated": dl_settings['simulated'],
            "runs_on": dl_settings["runs_on"],
            "code": dl_settings["code"],
            "value": value
        }

        dl_batch.append(('LightState', json.dumps(light_state_payload), 0, True))
        publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()

        set_threads_done()


def run_dl(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        dl_thread = threading.Thread(target=run_dl_simulator, args=(2, dl_callback, stop_event, settings))
        dl_thread.start()
        threads.append(dl_thread)
    else:
        from actuators.dl import DoorLight, run
        dl = DoorLight(int(settings['pin']))
        dl_thread = threading.Thread(target=run, args=(dl, dl_callback, settings,2,stop_event))
        dl_thread.start()
        threads.append(dl_thread)
