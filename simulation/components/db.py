import threading
import time
from components.lock import lock
from globals import *

def db_callback(code=""):
    with lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print("Buzz")
        print("=" * 20)
        time.sleep(1)


def run_db(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        db_thread = threading.Thread(target=db_callback, args=(code, ))
        db_thread.start()
        threads.append(db_thread)
    else:
        from actuators.db import DoorBuzzer, run
        db = DoorBuzzer(int(settings['pin']))
        db_thread = threading.Thread(target=run, args=(db, ))
        db_thread.start()
        threads.append(db_thread)
