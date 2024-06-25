import time
import random
from globals import *
from components.lock import lock

def generate_values():

    while True:
        n_people = get_num_of_people()
        motion = random.randint(0, 100)
        if motion > 70:
            if n_people > 0:
                direction = random.choice(["going_inside", "going_outside"])
            else:
                direction = "going_inside"

            values = [random.randint(1, 100) for _ in range(3)]

            if direction == "going_inside":
                values.sort()
                set_num_of_people(n_people + 1)
            else:
                values.sort(reverse=True)
                set_num_of_people(n_people - 1)

            with lock:
                print(direction)
                print("BROJ LJUDI JE", n_people)
            for value in values:
                yield value

      

def run_dus_simulator(delay, callback, stop_event,settings):
        for value in generate_values():
            time.sleep(delay)
            callback(value,settings)
            if stop_event.is_set():
                  break
              