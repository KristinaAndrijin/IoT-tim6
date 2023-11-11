import threading
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from components.dus import run_dus
from components.dms import run_dms
import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_sensors(settings, threads, stop_event):
    # DHT
    dht1_settings = settings['RDHT1']
    run_dht(dht1_settings, threads, stop_event)
    dht2_settings = settings['RDHT2']
    run_dht(dht2_settings, threads, stop_event)

    #DS
    ds1_settings = settings['DS1']
    run_ds(ds1_settings,threads,stop_event)

    #DUS
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event)

    # DMS
    dms_settings = settings['DMS']
    run_dms(dms_settings, threads, stop_event)


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        run_sensors(settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
