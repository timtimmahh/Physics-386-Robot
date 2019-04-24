#!/usr/bin/python3
from multiprocessing import Process, Value
from time import sleep

from ev3dev2.motor import OUTPUT_A, OUTPUT_C, SpeedPercent, MoveDifferential
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.wheel import EV3EducationSetTire

from ev3_toys.logger import get_logger

# done = False


gs = GyroSensor(INPUT_4)
# reset the angle and rate values for the Gyro by changing the mode
gs.mode = GyroSensor.MODE_GYRO_CAL
sleep(1)
gs.mode = GyroSensor.MODE_GYRO_RATE
gs.mode = GyroSensor.MODE_GYRO_ANG
gs.mode = GyroSensor.MODE_GYRO_G_A
sleep(1)

motors = MoveDifferential(OUTPUT_C, OUTPUT_A, EV3EducationSetTire, 103)


def check_gyro(val: Value, logger, gyro: GyroSensor):
    # write to a file for testing
    while val.value == 0:
        logger.info('(Angle, Rate) = {}\n'.format(gyro.angle_and_rate))
        sleep(0.5)


value = Value('i', 0)
t = Process(target=check_gyro, args=(value, get_logger('arc.gyro'), gs))
t.start()

motors.on_arc_left(SpeedPercent(50), 200, 1256.64)

# done = True
value.value = 1
t.join()
