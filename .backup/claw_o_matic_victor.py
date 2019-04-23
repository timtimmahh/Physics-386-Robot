from threading import Thread

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor
from ev3dev2.sound import Sound

# from swatter import FlySwatter

button = Button()
wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
claw = MediumMotor(OUTPUT_D)
gyro = GyroSensor(INPUT_1)
proximity = UltrasonicSensor(INPUT_2)
touch = TouchSensor(INPUT_3)
sound = Sound()

eyes = UltrasonicSensor(INPUT_4)
eyes_motor = MediumMotor(OUTPUT_C)


# swatter_sensor = FlySwatter()


def grab_everything():
    claw.on_for_rotations(SpeedPercent(100), 2, block=False)
    wheels.on(0, SpeedPercent(50))

    while not button.any():
        if proximity.distance_centimeters < 5.0:
            # swatter_sensor.scan_left()
            # swatter_sensor.scan_right()
            # if max(swatter_sensor.get_sensor_readings()) >= 250:
            #     wheels.on_for_rotations(100, SpeedPercent(50), 0.75)
            #     wheels.on_for_rotations(0, SpeedPercent(35), 1)
            claw.on_for_rotations(SpeedPercent(50), -2)
            wheels.on_for_seconds(0, SpeedPercent(-100), 1, block=True)
            wheels.on_for_rotations(45, SpeedPercent(100), 0.5, block=True)
            wheels.on_for_rotations(0, SpeedPercent(85), 5, block=True)
            claw.on_for_rotations(SpeedPercent(50), 2)
            wheels.on_for_rotations(0, SpeedPercent(-100), 1, block=True)
            wheels.on_for_degrees(-100, SpeedPercent(100), 360)
        elif touch.is_pressed:

            wheels.on_for_rotations(0, SpeedPercent(-50), 1, block=True)
            wheels.on_for_rotations(100, SpeedPercent(100), 1.5, block=True)



        else:
            wheels.on(0, SpeedPercent(50))


proc = Thread(target=grab_everything)
proc.start()
proc.join()
wheels.off(brake=False)
claw.off(brake=False)
