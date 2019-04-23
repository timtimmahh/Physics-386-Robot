from time import sleep

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.wheel import EV3EducationSetTire

from classes import Claw

button = Button()
claw = Claw()
wheels = MoveDifferential(OUTPUT_B, OUTPUT_A, EV3EducationSetTire, 110)
touch = TouchSensor(INPUT_3)
gyro = GyroSensor(INPUT_1)

gyro.mode = GyroSensor.MODE_GYRO_CAL
sleep(1)
gyro.mode = GyroSensor.MODE_GYRO_RATE
gyro.mode = GyroSensor.MODE_GYRO_ANG


def on(speed=50):
    wheels.on(SpeedPercent(speed), SpeedPercent(speed))


def forward_distance(distance=430, threshold=15):
    wheels.on_for_distance(SpeedPercent(30), distance - threshold)
    if threshold > 0:
        wheels.on_for_distance(SpeedPercent(5), threshold)


def rotate_until_closest(degrees=45):
    gyro_init = gyro.angle
    wheels.turn_right(SpeedPercent(5), degrees, block=False)
    distances = []
    while abs(gyro.angle - gyro_init) < degrees:
        distances.append((abs(gyro.angle - gyro_init), claw._us_sensor.distance_centimeters))
    print('\n'.join(str(distance) for distance in distances))


def return_to_base():
    wheels.on_arc_left(SpeedPercent(-40), 180, 250)
    wheels.on_arc_right(SpeedPercent(-40), 180, 470)
    wheels.on_arc_left(SpeedPercent(-40), 180, 240)
    on(speed=-65)
    while not touch.is_pressed:
        pass
    wheels.off(brake=False)


def produce_food():
    # go forward until nearest object is within 25 cm
    on()
    claw.wait_until_distance()

    # hard turn to get off wall
    wheels.turn_left(SpeedPercent(15), 45)
    # arc to the left to orient towards push object
    wheels.on_arc_left(SpeedPercent(30), 300, 230, brake=False)
    # move forward 430 mm
    forward_distance(threshold=30)
