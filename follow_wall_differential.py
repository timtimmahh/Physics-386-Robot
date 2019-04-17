from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.wheel import EV3EducationSetTire

from classes import Claw

claw = Claw()
claw.open()
wheels = MoveDifferential(OUTPUT_B, OUTPUT_A, EV3EducationSetTire, 110)
touch = TouchSensor(INPUT_3)


def on(speed=50):
    wheels.on(SpeedPercent(speed), SpeedPercent(speed))


def wait_until_distance(distance=25):
    while claw._us_sensor.distance_centimeters > distance:
        print(claw._us_sensor.distance_centimeters)


on()
wait_until_distance()

wheels.on_arc_left(SpeedPercent(50), 200, 215, brake=False)

on(speed=40)
wait_until_distance(5)
wheels.on_arc_right(SpeedPercent(-50), 200, 225, brake=False)
wheels.on_for_distance(SpeedPercent(-30), 75)
wheels.on_arc_left(SpeedPercent(-50), 150, 100, brake=False)
on(speed=-50)
while not touch.is_pressed:
    print('Waiting for touch...')
wheels.turn_right(SpeedPercent(30), 70)
on(speed=30)
wait_until_distance(25)
wheels.off()
# wheels.turn_right(SpeedPercent(50), 90)
# on()
# claw.grab_when_within(while_waiting=lambda: print(claw._us_sensor.distance_centimeters))
# on(-50)
# wait_until_distance(50)
# wheels.off(brake=False)
# wheels.on_for_distance(SpeedPercent(50), 200, brake=False)
# wheels.on_arc_right(SpeedPercent(40), 150, 150, brake=False)
# wheels.off(brake=False)
