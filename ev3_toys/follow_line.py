#!/usr/bin/python3
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, list_sensors
from ev3dev2.sensor.lego import ColorSensor

from ev3_toys.logger import get_logger

btn = Button()
left_cs, right_cs, center_cs = ColorSensor(INPUT_1), ColorSensor(INPUT_2), ColorSensor(INPUT_3)
last_bl_cs = None
motors = MoveSteering(OUTPUT_B, OUTPUT_A)
logger_cs = get_logger('line.color_sensor')
logger_m = get_logger('line.motors')
SPEED_PERCENTAGE = -30
SPEED_TURN_PERCENTAGE = 5


def straight():
    motors.on(0, SpeedPercent(SPEED_PERCENTAGE))
    global last_bl_cs
    last_bl_cs = center_cs


def turn_right():
    if left_cs.reflected_light_intensity <= 15:
        motors.on(-SPEED_PERCENTAGE, SpeedPercent(SPEED_PERCENTAGE))
        global last_bl_cs
        last_bl_cs = left_cs
        return True
    return False


def turn_left():
    if right_cs.reflected_light_intensity <= 15:
        motors.on(SPEED_PERCENTAGE, SpeedPercent(SPEED_PERCENTAGE))
        global last_bl_cs
        last_bl_cs = right_cs
        return True
    return False


def log_data(conn: Connection, cs_logger):
    print('Starting log...')
    while True:
        data = conn.recv()
        if not data:
            conn.close()
            print('Closing...')
            return
        cs_logger.info(data)


def follow_line(conn: Connection):
    conn.send(
        '''
        left_cs - Reflected light: {}
        right_cs - Reflected light: {}
        '''.format(left_cs.reflected_light_intensity, right_cs.reflected_light_intensity))
    if left_cs.reflected_light_intensity <= 15 and right_cs.reflected_light_intensity <= 15:
        straight()
    else:
        turn_right()
        turn_left()


def follow_line_three(conn: Connection):
    conn.send(
        '''
        left_cs - Reflected light: {}
        center_cs - Reflected light: {}
        right_cs - Reflected light: {}
        '''.format(
            left_cs.reflected_light_intensity,
            center_cs.reflected_light_intensity,
            right_cs.reflected_light_intensity))
    if left_cs.reflected_light_intensity > 15 >= center_cs.reflected_light_intensity \
            and right_cs.reflected_light_intensity > 15:
        straight()
    else:
        if not turn_left() and not turn_right() and center_cs.reflected_light_intensity > 15:
            conn.send('------------------------------ OFF THE LINE ------------------------------')
            turn_right() if last_bl_cs is left_cs else turn_left() if last_bl_cs is right_cs else straight()


three = [sensor.driver_name for sensor in list_sensors()].count('lego-ev3-color') == 3

logger_conn, motor_conn = Pipe(False)
p = Process(target=log_data, args=(logger_conn, logger_cs))
p.start()

while not btn.any():
    follow_line_three(motor_conn) if three else follow_line(motor_conn)

motors.off()
motor_conn.send(None)
p.join()
print('Process joined')
