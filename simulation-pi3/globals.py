import threading

is_menu_opened = False
LedIsOn = False
lcd_message = ""
lcd_should_change = False
rgbColors = [True, False, False]
threads_done_event = threading.Event()
is_alarm_on = False
is_bb_on = False
ds_trigger = 1


def get_is_menu_opened():
    return is_menu_opened


def set_is_menu_opened(value):
    global is_menu_opened
    is_menu_opened = value


def get_rgb_colors():
    return rgbColors


def set_rgb_colors(value):
    global rgbColors
    rgbColors = value


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


def get_is_alarm_on():
    return is_alarm_on


def set_is_alarm_on(value):
    global is_alarm_on
    is_alarm_on = value


def get_is_bb_on():
    return is_bb_on


def set_is_bb_on(value):
    global is_bb_on
    is_bb_on = value


def get_ds_trigger():
    return ds_trigger


def set_ds_trigger(value):
    global ds_trigger
    ds_trigger = value
