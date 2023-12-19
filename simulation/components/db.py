import threading
import time
from components.lock import lock
from globals import *

from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

batch = []
publish_data_counter = 0
publish_data_limit = 1

#TODO: NIKO NE ŠALJE AKTUATORE KAO BATCH OD 1
def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
        #print(f'published {publish_data_limit} db values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
publisher_thread.daemon = True
publisher_thread.start()

def db_callback(db_settings):

    global publish_data_counter, publish_data_limit
    code = db_settings["code"]

    payload = {
        "measurement": "Door Buzzer",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "code": db_settings["code"],
        "value": True
    }

    with lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Runs on: {db_settings['runs_on']}")
        print("Buzz")
        print("=" * 20)
        # time.sleep(1)

        batch.append(('Door Buzzer', json.dumps(payload), 0, True))
        publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()

        set_threads_done()




def run_db(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        db_thread = threading.Thread(target=db_callback, args=(settings,))
        db_thread.start()
        threads.append(db_thread)
    else:
        from actuators.db import DoorBuzzer, run
        db = DoorBuzzer(int(settings['pin']))
        db_thread = threading.Thread(target=run, args=(db,db_callback,settings ))
        db_thread.start()
        threads.append(db_thread)
