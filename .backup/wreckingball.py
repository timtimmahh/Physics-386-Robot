from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor

button = Button()
touch_sensor = TouchSensor(INPUT_3)
wrecking_ball = MediumMotor(OUTPUT_C)
wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
eyes = UltrasonicSensor(INPUT_2)
front_claw = MediumMotor(OUTPUT_D)


def close():
    front_claw.on_for_degrees(SpeedPercent(100), -570)  # clenches the claw


def open():
    front_claw.on_for_degrees(SpeedPercent(100), 570)  # opens the claw


def slam():
    wrecking_ball.on_for_rotations(SpeedPercent(100), 1.25)
    wrecking_ball.on_for_rotations(SpeedPercent(-50), 1.25)


wheels.on(0, SpeedPercent(50))

while True:
    if eyes.distance_centimeters <= 20:
        break

wheels.off(brake=True)

wheels.on_for_rotations(-100, SpeedPercent(30), 0.02)  # turns right a little

for x in range(4):
    slam()

for z in range(5):
    wheels.on_for_rotations(100, SpeedPercent(30), 0.02)
    slam()

for y in range(2):
    slam()

close()
wheels.on_for_rotations(-100, SpeedPercent(30), 0.35)  # turns right a little
open()
wheels.on_for_rotations(0, SpeedPercent(100), 0.1)  # goes forward
wheels.on_for_rotations(0, SpeedPercent(-100), 0.1)  # goes backwards
close()
open()
close()
open()

wheels.on_for_rotations(100, SpeedPercent(30), 0.1)  # turns back left

wheels.on(0, SpeedPercent(-50))

while True:
    if touch_sensor.is_pressed:
        break

wheels.off(brake=False)
wrecking_ball.off(brake=False)
