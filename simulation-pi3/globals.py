import threading
from datetime import datetime

is_menu_opened = False
LedIsOn = False
lcd_message = ""
lcd_should_change = False
rgbColors = [True, False, False]
threads_done_event = threading.Event()
color_changed = False
is_timer_on = False
timer_time = None
is_ds_alarm_on = False
is_bb_on = False
ds_trigger = 1
is_alarm_on = False
dms_alarm_on = False
rpir_alarm_on = False
gyro_alarm_on = False
is_sd_working = False
display_iter = 0

def get_display_iter():
    return display_iter


def set_display_iter(value):
    global display_iter
    display_iter = value

def get_is_sd_working():
    return is_sd_working


def set_is_sd_working(value):
    global is_sd_working
    is_sd_working = value

def get_timer_time():
    return timer_time


def set_timer_time(value):
    global timer_time
    timer_time = value

def get_is_timer_on():
    return is_timer_on


def set_is_timer_on(value):
    global is_timer_on
    is_timer_on = value

def get_is_color_changed():
    return color_changed


def set_is_color_changed(value):
    global color_changed
    color_changed = value

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

def set_rgb_colors_index(value,index):
    global rgbColors
    rgbColors[index] = value

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


def get_is_ds_alarm_on():
    return is_ds_alarm_on


def set_is_ds_alarm_on(value):
    global is_ds_alarm_on
    is_ds_alarm_on = value


def is_dms_alarm_on():
    return dms_alarm_on


def set_dms_alarm_on(value):
    global dms_alarm_on
    dms_alarm_on = value


def is_rpir_alarm_on():
    return rpir_alarm_on


def set_rpir_alarm_on(value):
    global rpir_alarm_on
    rpir_alarm_on = value


def is_gyro_alarm_on():
    return gyro_alarm_on


def set_gyro_alarm_on(value):
    global gyro_alarm_on
    gyro_alarm_on = value

def check_timer():
    if not is_timer_on:
        return False
    if timer_time is None:
        return False
    else:
        current_datetime = datetime.now()
        #print(timer_time, current_datetime, timer_time < current_datetime)
        if timer_time < current_datetime:
            return True
        else:
            return False