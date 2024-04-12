import threading
import time
from components.lock import lock
from globals import *
from simulators.sd import run_sd_simulator

from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

# batch = []
# publish_data_counter = 0
# publish_data_limit = 1

# def publisher_task(event, batch):
#     global publish_data_counter, publish_data_limit
#     while True:
#         event.wait()
#         with lock:
#             local_batch = batch.copy()
#             publish_data_counter = 0
#             batch.clear()
#         publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
#         #print(f'published {publish_data_limit} db values')
#         event.clear()


# publish_event = threading.Event()
# publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
# publisher_thread.daemon = True
# publisher_thread.start()

def sd_callback(sd_settings, value):

    #global publish_data_counter, publish_data_limit
    code = sd_settings["code"]

    # payload = {
    #     "measurement": "LCD",
    #     "simulated": lcd_settings['simulated'],
    #     "runs_on": lcd_settings["runs_on"],
    #     "code": lcd_settings["code"],
    #     "value": True
    # }

    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Runs on: {sd_settings['runs_on']}")
            print(f"Displaying.")
            print("=" * 20)
            # time.sleep(1)

            # batch.append(('LCD', json.dumps(payload), 0, True))
            # publish_data_counter += 1
            #
            # if publish_data_counter >= publish_data_limit:
            #     publish_event.set()

            set_threads_done()

def run_sd(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        sd_thread = threading.Thread(target=run_sd_simulator, args=(2, sd_callback, stop_event, settings))
        sd_thread.start()
        threads.append(sd_thread)
    else:
        from sensors.sd import run_4sd_loop, SegmentDisplay
        print("Starting " + code + "loop")
        sd = SegmentDisplay(settings['segments'],settings['digits'])
        sd_thread = threading.Thread(target=run_4sd_loop, args=(sd, 2, sd_callback, stop_event, settings))
        sd_thread.start()
        threads.append(sd_thread)
        print(code + " loop started")
