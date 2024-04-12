from simulators.dht import run_dht_simulator
import threading
import time
from components.lock import lock
from globals import *

from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

from simulators.gyro import run_gyro_simulator

gyro_batch = []
publish_data_counter = 0
publish_data_limit = 5
#counter_lock = threading.Lock()

def publisher_task(event, gyro_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_dht_batch = gyro_batch.copy()
            publish_data_counter = 0
            gyro_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        if not get_is_menu_opened():
            print(f'published {publish_data_limit} dht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def gyro_callback(accel, gyro,gyro_settings):
    global publish_data_counter, publish_data_limit

    code = gyro_settings["code"]

    accel_payload = {
        "measurement": "Acceleration",
        "simulated": gyro_settings['simulated'],
        "runs_on": gyro_settings["runs_on"],
        "code": gyro_settings["code"],
        "value": accel
    }

    gyro_payload = {
        "measurement": "Gyro",
        "simulated": gyro_settings['simulated'],
        "runs_on": gyro_settings["runs_on"],
        "code": gyro_settings["code"],
        "value": gyro
    }


    #printuj merenja ako meni nije otvoren
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Acceleration: {accel}")
            print(f"Gyro: {gyro}")
            print(f"Runs on: {gyro_settings['runs_on']}")


        gyro_batch.append(('Acceleration', json.dumps(accel_payload), 0, True))
        gyro_batch.append(('Gyro', json.dumps(gyro_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gyro(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        gyro_thread = threading.Thread(target=run_gyro_simulator, args=(2, gyro_callback, stop_event,settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print(code + " sumilator started")
    else:
        from sensors.auxiliary import MPU6050
        from sensors.gyro import run_gyro_loop
        print("Starting " + code + "loop")
        mpu = MPU6050.MPU6050()
        gyro_thread = threading.Thread(target=run_gyro_loop, args=(mpu, 2, gyro_callback, stop_event,settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print(code + " loop started")
