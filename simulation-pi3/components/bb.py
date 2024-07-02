import threading
import time
from components.lock import lock
from globals import *

from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

from simulators.bb import run_bb_simulator

batch = []
publish_data_counter = 0
publish_data_limit = 1


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

def bb_callback(buzz, bb_settings):

    global publish_data_counter, publish_data_limit
    code = bb_settings["code"]
    should_publish = False
    value_to_publish = False
    is_bb_buzzing = get_is_bb_on()

    if (buzz is True and is_bb_buzzing is False):
        should_publish = True
        value_to_publish = True
        set_is_bb_on(True)

    if (buzz is False and is_bb_buzzing is True):
        should_publish = True
        value_to_publish = False
        set_is_bb_on(False)

    with lock:

        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Runs on: {bb_settings['runs_on']}")
        if buzz:
            print("Buzzing")
        else:
            print("Not buzzing")
        print("=" * 20)
        # time.sleep(1)

        if should_publish:

            payload = {
                "measurement": "Bedroom Buzzer",
                "simulated": bb_settings['simulated'],
                "runs_on": bb_settings["runs_on"],
                "code": bb_settings["code"],
                "value": value_to_publish
            }

            batch.append(('Bedroom Buzzer', json.dumps(payload), 0, True))
            publish_data_counter += 1

            if publish_data_counter >= publish_data_limit:
                publish_event.set()

        set_threads_done()




def run_bb(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        db_thread = threading.Thread(target=run_bb_simulator, args=(2, bb_callback, stop_event, settings))
        db_thread.start()
        threads.append(db_thread)
        print(code + " simulator started")
    else:
        from actuators.bb import BedroomBuzzer, run
        bb = BedroomBuzzer(int(settings['pin']))
        bb_thread = threading.Thread(target=run, args=(bb,bb_callback,settings,2,stop_event ))
        bb_thread.start()
        threads.append(bb_thread)