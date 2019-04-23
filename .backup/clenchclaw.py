from threading import Thread

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveSteering, MediumMotor
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import TouchSensor

claw = MediumMotor(OUTPUT_C)

motors = MoveSteering(OUTPUT_A, OUTPUT_B)

ts = TouchSensor(INPUT_2)

button = Button()


def button_press():
    button.any()


def clench():
    claw.on_for_rotations(SpeedPercent(15), rotations=-0.25)
    claw.on_for_rotations(SpeedPercent(15), rotations=0.25)


def movestraight():
    motors.on_for_rotations(steering=0, rotations=1, speed=25)


def rotate():
    motors.on_for_rotations(steering=-100, rotations=1, speed=25, block=False)


str = Thread(target=movestraight)

while not button.any():
    clench()
    movestraight()
    rotate()
