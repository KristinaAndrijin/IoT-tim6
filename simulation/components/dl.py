import threading
import time
from components.lock import lock
from globals import *


def dl_callback(code=""):
    with lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        if led_is_on():
            print("LED turned OFF")
            set_led_state(False)
        else:
            print("LED turned ON")
            set_led_state(True)
        print("=" * 20)
        time.sleep(1)


def run_dl(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        dl_thread = threading.Thread(target=dl_callback, args=(code,))
        dl_thread.start()
        threads.append(dl_thread)
    else:
        from actuators.dl import DoorLight, run
        dl = DoorLight(int(settings['pin']))
        dl_thread = threading.Thread(target=run, args=(dl,))
        dl_thread.start()
        threads.append(dl_thread)
