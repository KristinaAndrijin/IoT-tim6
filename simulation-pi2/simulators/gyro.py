import time
import random

def generate_values(initial_accel=[0, 0, 0], initial_gyro=[0, 0, 0]):
    accel = initial_accel
    gyro = initial_gyro

    while True:
        accel = [a + random.randint(-32768, 32767) for a in accel]
        gyro = [g + random.randint(-1000, 1000) for g in gyro]

        # Ensure values are within a reasonable range
        accel = [max(accel_val, 0) for accel_val in accel]
        gyro = [max(gyro_val, 0) for gyro_val in gyro]

        yield accel, gyro



def run_gyro_simulator(delay, callback, stop_event, settings):
    initial_acceleration = [0, 0, 0]
    initial_gyro = [0, 0, 0]

    for accel, gyro in generate_values(initial_acceleration, initial_gyro):
        time.sleep(delay)
        callback(accel, gyro, settings)
        if stop_event.is_set():
            break
