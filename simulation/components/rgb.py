import threading
import time
from components.lock import lock
from globals import *
from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

rgb_batch = []
publish_data_counter = 0
publish_data_limit = 1
#counter_lock = threading.Lock()

def publisher_task(event, dl_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_dl_batch = dl_batch.copy()
            publish_data_counter = 0
            dl_batch.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        #print(f'published {publish_data_limit} dl values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_callback(rgb_settings):
    global publish_data_counter, publish_data_limit
    with lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {rgb_settings['code']}")

        colors = get_rgb_colors()
        if (not colors):
            set_rgb_colors([True,False,False])
        print("Colors:")
        print(f"Red: {colors[0]}")
        print(f"Green: {colors[1]}")
        print(f"Blue: {colors[2]}")

        print(f"Runs on: {rgb_settings['runs_on']}")
        print("=" * 20)

        light_state_payload = {
            "measurement": "RGBState",
            "simulated": rgb_settings['simulated'],
            "runs_on": rgb_settings["runs_on"],
            "code": rgb_settings["code"],
            "value": colors
        }

        rgb_batch.append(('RGBState', json.dumps(light_state_payload), 0, True))
        publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()
        # time.sleep(1)
        set_threads_done()


def run_rgb(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        rgb_thread = threading.Thread(target=rgb_callback, args=(settings,))
        rgb_thread.start()
        threads.append(rgb_thread)
    else:
        from actuators.rgb import RGBLight, run
        rgb = RGBLight(int(settings['red_pin']),int(settings['green_pin']),int(settings['blue_pin']))
        #ovo true false true na kraju su samo dummy, ovde će se upravljati sa rgb
        rgb_thread = threading.Thread(target=run, args=(rgb, rgb_callback, settings,True,False,True))
        rgb_thread.start()
        threads.append(rgb_thread)
