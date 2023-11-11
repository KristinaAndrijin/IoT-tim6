from simulators.dht import run_dht_simulator
import threading
import time
from components.lock import lock


def dht_callback(humidity, temperature, code=""):
    with lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, code))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(code + " sumilator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        print("Starting " + code + "loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(code + " loop started")
