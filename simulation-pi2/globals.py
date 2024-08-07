import threading

is_menu_opened = False
lcd_message = ""
lcd_should_change = False
threads_done_event = threading.Event()
num_of_people = 0
gdht_humidity = 0
gdht_temperature = 0

def get_gdht_temperature():
    return gdht_temperature

def set_gdht_temperature(value):
    global gdht_temperature
    gdht_temperature = value

def get_gdht_humidity():
    return gdht_humidity

def set_gdht_humidity(value):
    global gdht_humidity
    gdht_humidity = value

def get_num_of_people():
    return num_of_people

def set_num_of_people(value):
    global num_of_people
    num_of_people = value

def get_is_menu_opened():
    return is_menu_opened


def set_is_menu_opened(value):
    global is_menu_opened
    is_menu_opened = value


def set_threads_done():
    global threads_done_event
    threads_done_event.set()


def wait_for_threads():
    global threads_done_event
    threads_done_event.wait()
    threads_done_event.clear()
