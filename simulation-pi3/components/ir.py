from simulators.dht import run_dht_simulator
import threading
import time
from components.lock import lock
from globals import *

from broker_settings import HOSTNAME, PORT
import json
import paho.mqtt.publish as publish

from simulators.ir import run_ir_simulator

ir_batch = []
publish_data_counter = 0
publish_data_limit = 1
#counter_lock = threading.Lock()

def publisher_task(event, ir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with lock:
            local_dht_batch = ir_batch.copy()
            publish_data_counter = 0
            ir_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        if not get_is_menu_opened():
            print(f'published {publish_data_limit} ir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ir_callback(reading,ir_settings):
    global publish_data_counter, publish_data_limit

    code = ir_settings["code"]

    temp_payload = {
        "measurement": "IrReading",
        "simulated": ir_settings['simulated'],
        "runs_on": ir_settings["runs_on"],
        "code": ir_settings["code"],
        "value": reading
    }

    if reading == "1":
        current = get_rgb_colors()[0]
        opposite = not current
        set_rgb_colors_index(opposite,0)
        set_is_color_changed(True)
    elif reading == "2":
        current = get_rgb_colors()[1]
        opposite = not current
        set_rgb_colors_index(opposite, 1)
        set_is_color_changed(True)
    elif reading == "3":
        current = get_rgb_colors()[2]
        opposite = not current
        set_rgb_colors_index(opposite, 2)
        set_is_color_changed(True)

    #printuj merenja ako meni nije otvoren
    with lock:
        if not get_is_menu_opened():
            t = time.localtime()
            print("=" * 20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Reading: '{reading}'")
            print(f"Runs on: {ir_settings['runs_on']}")


        ir_batch.append(('IrReading', json.dumps(temp_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ir(settings, threads, stop_event):
    code = settings['code']
    if settings['simulated']:
        print("Starting " + code + " simulator")
        ir_thread = threading.Thread(target=run_ir_simulator, args=(2, ir_callback, stop_event,settings))
        ir_thread.start()
        threads.append(ir_thread)
        print(code + " simulator started")
    else:
        from sensors.ir import InfraRed, run_ir_loop
        print("Starting " + code + "loop")
        ir = InfraRed(settings['pin'])
        ir_thread = threading.Thread(target=run_ir_loop, args=(ir, 2, ir_callback, stop_event,settings))
        ir_thread.start()
        threads.append(ir_thread)
        print(code + " loop started")
