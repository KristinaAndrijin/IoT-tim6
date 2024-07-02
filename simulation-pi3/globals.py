import threading

is_menu_opened = False
LedIsOn = False
lcd_message = ""
lcd_should_change = False
rgbColors = [True,False,False]
threads_done_event = threading.Event()
color_changed = False
is_timer_on = False
timer_time = None

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
