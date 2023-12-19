from simulators.dht import run_dht_simulator
import threading
import time
from components.lock import lock
from globals import *

from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
#counter_lock = threading.Lock()

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        if not get_is_menu_opened():
            print(f'published {publish_data_limit} dht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dht_callback(humidity, temperature,dht_settings):
    global publish_data_counter, publish_data_limit

    code = dht_settings["code"]

    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "code": dht_settings["code"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "code": dht_settings["code"],
        "value": humidity
    }


    #printuj merenja ako meni nije otvoren
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Humidity: {humidity}%")
            print(f"Temperature: {temperature}°C")
            print(f"Runs on: {dht_settings['runs_on']}")


        dht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event,settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(code + " sumilator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        print("Starting " + code + "loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event,settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(code + " loop started")
