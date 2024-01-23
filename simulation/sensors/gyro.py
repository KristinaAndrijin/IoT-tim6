#!/usr/bin/env python3
import auxiliary.MPU6050 as MPU6050
import time
import os
    
def run_gyro_loop(mpu, delay, callback, stop_event, settings):
    accel = [0] * 3
    gyro = [0] * 3

    mpu.dmp_initialize()

    while(True):
        accel = mpu.get_acceleration()      #get accelerometer data
        gyro = mpu.get_rotation()           #get gyroscope data
        os.system('clear')
        #print("a/g:%d\t%d\t%d\t%d\t%d\t%d "%(accel[0],accel[1],accel[2],gyro[0],gyro[1],gyro[2]))
        #print("a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s"%(accel[0]/16384.0,accel[1]/16384.0,
            #accel[2]/16384.0,gyro[0]/131.0,gyro[1]/131.0,gyro[2]/131.0))

        accel_result = [a / 16384.0 for a in accel]
        gyro_result = [g / 131.0 for g in gyro]

        callback(accel_result,gyro_result, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)

