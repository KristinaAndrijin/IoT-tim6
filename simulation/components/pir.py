from simulators.pir import run_pir_simulator
import threading
import time
from components.lock import lock
from globals import *
def pir_callback(motion, code=""):
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            if motion:
                print("You moved")
            else:
                print("You stopped moving")


def run_pir(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event, code))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.pir import PassiveInfraRed
        print("Starting " + code + " sensor")
        pir_sensor = PassiveInfraRed(settings['pin'], pir_callback)
        thread = threading.Thread(target=pir_sensor.run, args=(2, ))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
