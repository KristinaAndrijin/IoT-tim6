import threading

is_menu_opened = False
LedIsOn = False
rgbColors = [True,False,False]
threads_done_event = threading.Event()


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
