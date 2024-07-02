import threading

is_menu_opened = False
LedIsOn = False
is_ds_alarm_on = False
threads_done_event = threading.Event()
is_db_on = False
dl_should_turn_off = None
num_of_people = 0
ds_trigger = 1
is_alarm_on = False
dms_alarm_on = False


def get_num_of_people():
    return num_of_people


def set_num_of_people(value):
    global num_of_people
    num_of_people = value


def get_dl_should_turn_off():
    return dl_should_turn_off


def set_dl_should_turn_off(value):
    global dl_should_turn_off
    dl_should_turn_off = value


def get_is_db_on():
    return is_db_on


def set_is_db_on(value):
    global is_db_on
    is_db_on = value


def get_is_ds_alarm_on():
    return is_ds_alarm_on


def set_is_ds_alarm_on(value):
    global is_ds_alarm_on
    is_ds_alarm_on = value


def get_is_menu_opened():
    return is_menu_opened


def set_is_menu_opened(value):
    global is_menu_opened
    is_menu_opened = value


def led_is_on():
    return LedIsOn


def set_led_state(value):
    global LedIsOn
    LedIsOn = value


def set_threads_done():
    global threads_done_event
    threads_done_event.set()


def wait_for_threads():
    global threads_done_event
    threads_done_event.wait()
    threads_done_event.clear()


def get_ds_trigger():
    return ds_trigger


def set_ds_trigger(value):
    global ds_trigger
    ds_trigger = value


def get_is_alarm_on():
    return is_alarm_on


def set_is_alarm_on(value):
    global is_alarm_on
    is_alarm_on = value


def is_dms_alarm_on():
    return dms_alarm_on


def set_dms_alarm_on(value):
    global dms_alarm_on
    dms_alarm_on = value
