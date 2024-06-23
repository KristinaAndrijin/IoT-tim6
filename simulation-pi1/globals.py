import threading

is_menu_opened = False
LedIsOn = False
is_alarm_on = False
threads_done_event = threading.Event()
is_db_on = False

def get_is_db_on():
    return is_db_on

def set_is_db_on(value):
    global is_db_on
    is_db_on = value

def get_is_alarm_on():
    return is_alarm_on

def set_is_alarm_on(value):
    global is_alarm_on
    is_alarm_on = value

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
