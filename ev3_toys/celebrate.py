from multiprocessing import Process

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering, LargeMotor, SpeedPercent, MediumMotor
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import TouchSensor

button = Button()

motors = MoveSteering(OUTPUT_B, OUTPUT_D)

claw = LargeMotor(OUTPUT_C)
hammer = MediumMotor(OUTPUT_A)
touch = TouchSensor(INPUT_2)


def hammer_time():
    hammer.on(SpeedPercent(100))
    while not button.any():
        pass
    hammer.off()


def grab():
    while not button.any():
        claw.on_for_rotations(SpeedPercent(100), 0.1)
        claw.on_for_rotations(SpeedPercent(100), -0.1)


def reverse_rotate():
    motors.on_for_rotations(0, SpeedPercent(100), 1)
    motors.on_for_degrees(-100, SpeedPercent(100), 360)
    motors.off()


def forward():
    motors.on(0, SpeedPercent(-100))


def check_touch():
    forward()
    while touch.wait_for_pressed():
        if touch.is_pressed:
            reverse_rotate()
            forward()


hammer_proc = Process(target=hammer_time)
claw_proc = Process(target=grab)
touch_proc = Process(target=check_touch)

hammer_proc.start()
claw_proc.start()
touch_proc.start()

hammer_proc.join()
claw_proc.join()
touch_proc.join()

motors.off()
