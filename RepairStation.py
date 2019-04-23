from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_3
from ev3dev2.sensor.lego import TouchSensor

from classes import Wheels, Gyro, Claw

wheels = Wheels(OUTPUT_A, OUTPUT_B)
claw = Claw()
proximity_sensor = claw.eyes
touch_sensor = TouchSensor(INPUT_3)
button = Button()
gyro = Gyro(INPUT_1)

intialAngle = gyro.calibrate()
initial_rotations = wheels.get_rotations()
if not claw.is_open():
    claw.open()
claw.claw_motor.on_for_rotations(SpeedPercent(100), -0.7)
wheels.turn_left(15, 14)

total_distance = 970
wheels.on_for_distance(25, total_distance)
angleCorrection = gyro.angle
while wheels.distance_remaining(total_distance, initial_rotations) > 0:
    if gyro.angle < intialAngle:
        difference = abs(gyro.angle - intialAngle)
        wheels.turn_left(20, difference, True)
    elif gyro.angle > intialAngle:
        difference = abs(gyro.angle - intialAngle)
        wheels.turn_right(20, difference, True)
    else:
        wheels.on_for_distance(25, wheels.distance_remaining(total_distance, initial_rotations))

for distance in range(75, 150, 25):
    wheels.on_for_distance(-25, distance)
    wheels.on_for_distance(25, distance)

wheels.on(0, -60)
touch.wait_for_pressed(sleed_ms=None)
# while not touch_sensor.is_pressed:
#    pass

#
# wheels.on_for_rotations(0, SpeedPercent(-20), 0.5) #
# wheels.off(brake=True)
#
# #wheels.on_for_rotations(0, SpeedPercent(10), 0.5)  # moves up to get the claw on the
# #front_claw.on_for_degrees(SpeedPercent(20), -570)  # clenches the claw
# #front_claw.on_for_degrees(SpeedPercent(100), 570, block=False)  #opens the claw again
#
# wheels.on_for_rotations(0, SpeedPercent(40), 0.5) #
# wheels.off(brake=True)
#
# wheels.on_for_rotations(0, SpeedPercent(-90), 0.5) #

claw.open()
wheels.off(brake=False)
