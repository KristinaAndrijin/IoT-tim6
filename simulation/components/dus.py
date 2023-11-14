from simulators.dus import run_dus_simulator
import threading
import time
from components.lock import lock
from globals import *
def dus_callback(distance, code="Sensor is on"):
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Distance: " + str(distance) + " cm")


def run_dus(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        thread = threading.Thread(target=run_dus_simulator, args=(2, dus_callback, stop_event, code))
        thread.start()
        threads.append(thread)
        print(code + " simulator started")
    else:
        from sensors.dus import DistanceSensor
        print("Starting " + code + " sensor")
        dus_sensor = DistanceSensor(settings['trig_pin'], settings['echo_pin'])
        thread = threading.Thread(target=dus_sensor.run, args=(2, dus_callback, stop_event))
        thread.start()
        threads.append(thread)
        print(code + " sensor started")
