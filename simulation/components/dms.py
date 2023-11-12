from simulators.dms import run_dms_simulator
import threading
import time
from components.lock import lock
from globals import *
def dms_callback(character, code=""):
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Character: " + str(character))


def run_dms(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_dms_simulator, args=(2, dms_callback, stop_event, code))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.dms import DoorMembraneSwitch
        print("Starting " + code + " sensor")
        dms_sensor = DoorMembraneSwitch(settings)
        thread = threading.Thread(target=dms_sensor.run, args=(2, dms_callback, stop_event))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
