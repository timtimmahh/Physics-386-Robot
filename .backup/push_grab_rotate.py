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
        wheels.on_for_distance(SpeedPercent(15), threshold)


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


# go forward until nearest object is within 25 cm
on()
claw.wait_until_distance()

# hard turn to get off wall
wheels.turn_left(SpeedPercent(15), 45)
# arc to the left to orient towards push object
wheels.on_arc_left(SpeedPercent(30), 300, 230, brake=False)
# move forward 430 mm
forward_distance(threshold=30)

# wheels.on_for_distance(SpeedPercent(-30), 30)
forward_distance(-30, 0)
rotate_until_closest()

speed = 15
distance = 2.0
on(speed=speed)


def decrease_speed(distance_cm):
    global speed
    speed = speed / distance_cm - distance
    return speed


claw.grab_when_within(distance_cm=distance, on_close=lambda: wheels.off(),
                      while_waiting=lambda d_cm: on(decrease_speed(d_cm)))
forward_distance(-80)
claw.open()
forward_distance(-100)

#
# # reverse at an arc
# wheels.on_arc_right(SpeedPercent(-50), 200, 225, brake=False)
# # reverse for 145 mm
# wheels.on_for_distance(SpeedPercent(-30), 155)
# # reverse at an arc, orient touch sensor towards wall
# wheels.on_arc_left(SpeedPercent(-50), 175, 115, brake=False)
#
# # move back at 50% speed until touch sensor is pressed
# on(speed=-50)
# while not touch.is_pressed:
#     pass
#
# # rotate right 90 degrees
# wheels.turn_right(SpeedPercent(35), 90)
# # move forward 110 mm
# forward_distance(110)
#
# # return to the base, avoiding obstacles
# return_to_base()
