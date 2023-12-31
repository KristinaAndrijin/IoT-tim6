import threading
from settings import load_settings
from components.dht import run_dht
from components.ds import run_ds
from components.dus import run_dus
from components.dms import run_dms
from components.pir import run_pir
from components.db import run_db
from components.dl import run_dl
from components.lock import actuator_lock
from globals import *
import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

is_menu_opened = False

def run_sensors(settings, threads, stop_event):
    # DHT
    dht1_settings = settings['RDHT1']
    run_dht(dht1_settings, threads, stop_event)
    dht2_settings = settings['RDHT2']
    run_dht(dht2_settings, threads, stop_event)

    # DS
    ds1_settings = settings['DS1']
    run_ds(ds1_settings,threads,stop_event)

    # DUS
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event)

    # DMS
    dms_settings = settings['DMS']
    run_dms(dms_settings, threads, stop_event)

    # DPIR
    dpir_settings = settings['DPIR1']
    run_pir(dpir_settings, threads, stop_event)

    # RPIR
    rpir_settings = settings['RPIR1']
    run_pir(rpir_settings, threads, stop_event)
    rpir_settings = settings['RPIR2']
    run_pir(rpir_settings, threads, stop_event)

def open_menu():
    global is_menu_opened
    with actuator_lock:
        print("Menu contents:")
        print("1. Start buzzing")
        print("2. Switch led state")
        # print("3. Option 3")
        print("Enter 'x' to close the menu.")

        user_input = input(" >> ").lower()

        if user_input == 'x':
            set_is_menu_opened(False)
        elif user_input == '1':
            db_settings = settings['DB']
            run_db(db_settings, threads, stop_event)
            wait_for_threads()
        elif user_input == '2':
            dl_settings = settings['DL']
            run_dl(dl_settings, threads, stop_event)
            wait_for_threads()
        else:
            print("Invalid input. Try again.")


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        run_sensors(settings, threads, stop_event)
        while True:
            if not get_is_menu_opened():
                user_input = input("Enter 'm' to open the menu: ").lower()

                if user_input == 'm':
                    set_is_menu_opened(True)
                else:
                    time.sleep(2)
            else:
                open_menu()

    except KeyboardInterrupt:
        print("=" * 20)
        print('Stopping app')
        for t in threads:
            stop_event.set()

        for t in threads:
            t.join()

        print("=" * 20)
        print("App successfully stopped")