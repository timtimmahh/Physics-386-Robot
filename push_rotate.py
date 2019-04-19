from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.wheel import EV3EducationSetTire

from classes import Claw

button = Button()
claw = Claw()
claw.open()
wheels = MoveDifferential(OUTPUT_B, OUTPUT_A, EV3EducationSetTire, 110)
touch = TouchSensor(INPUT_3)


def on(speed=50):
    wheels.on(SpeedPercent(speed), SpeedPercent(speed))


def wait_until_distance(distance=25):
    while claw._us_sensor.distance_centimeters > distance:
        pass


def forward_distance(distance=415):
    wheels.on_for_distance(SpeedPercent(35), distance)


def return_to_base():
    wheels.on_arc_left(SpeedPercent(-40), 190, 250)
    wheels.on_arc_right(SpeedPercent(-40), 200, 500)
    wheels.on_arc_left(SpeedPercent(-40), 200, 230)
    on(speed=-65)
    while not touch.is_pressed:
        pass
    wheels.off(brake=False)


#
# on(speed=15)
# wait_until_distance(10)
# wheels.on_arc_left(SpeedPercent(15), 55, 70, brake=True)


on()
wait_until_distance()

wheels.on_arc_left(SpeedPercent(50), 220, 215, brake=False)

forward_distance()
offset = 15
print(claw._us_sensor.distance_centimeters)
if not claw._us_sensor.distance_centimeters > offset:
    forward_distance((claw._us_sensor.distance_centimeters - offset) * 10)

wheels.on_arc_right(SpeedPercent(-50), 200, 225, brake=False)
wheels.on_for_distance(SpeedPercent(-30), 130)
wheels.on_arc_left(SpeedPercent(-50), 150, 115, brake=False)

on(speed=-50)
while not touch.is_pressed:
    pass

wheels.turn_right(SpeedPercent(35), 90)
wheels.on_for_distance(SpeedPercent(30), 175, brake=True)

return_to_base()
