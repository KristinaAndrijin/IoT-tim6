import threading
import time
from components.lock import lock
from globals import *
from simulators.lcd import run_lcd_simulator

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

def lcd_callback(lcd_settings,value):

    #global publish_data_counter, publish_data_limit
    code = lcd_settings["code"]

    # payload = {
    #     "measurement": "LCD",
    #     "simulated": lcd_settings['simulated'],
    #     "runs_on": lcd_settings["runs_on"],
    #     "code": lcd_settings["code"],
    #     "value": True
    # }

    with lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Runs on: {lcd_settings['runs_on']}")
        print(f"Displaying.")
        print("=" * 20)
        # time.sleep(1)

        # batch.append(('LCD', json.dumps(payload), 0, True))
        # publish_data_counter += 1
        #
        # if publish_data_counter >= publish_data_limit:
        #     publish_event.set()

        set_threads_done()

def run_lcd(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        lcd_thread = threading.Thread(target=run_lcd_simulator, args=(2, lcd_callback, stop_event,settings))
        lcd_thread.start()
        threads.append(lcd_thread)
    else:
        from sensors.lcd import run_lcd_loop, LCD
        print("Starting " + code + "loop")
        lcd = LCD(settings['pin'])
        lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd, 2, lcd_callback, stop_event, settings))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(code + " loop started")
