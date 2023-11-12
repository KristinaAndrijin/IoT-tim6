from simulators.ds import run_ds_simulator
import threading
import time
from components.lock import lock
from globals import *

def ds_callback(opened, code=""):
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            if opened:
                print("Door is opened")
            else:
                print("Door is closed")


def run_ds(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_ds_simulator, args=(2, ds_callback, stop_event, code))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.ds import DoorSensor
        print("Starting " + code + " sensor")
        door_sensor = DoorSensor(settings['pin'])  # Adjust this based on your hardware setup
        thread = threading.Thread(target=door_sensor.run, args=(2, ds_callback, stop_event))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
