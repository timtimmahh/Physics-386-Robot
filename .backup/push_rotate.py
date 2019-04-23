from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.wheel import EV3EducationSetTire

from classes import Claw

button = Button()
claw = Claw()
wheels = MoveDifferential(OUTPUT_B, OUTPUT_A, EV3EducationSetTire, 110)
touch = TouchSensor(INPUT_3)


def on(speed=50):
    wheels.on(SpeedPercent(speed), SpeedPercent(speed))


def wait_until_distance(distance=25):
    while claw.eyes.distance_centimeters > distance:
        pass


def forward_distance(distance=430, threshold=15):
    wheels.on_for_distance(SpeedPercent(30), distance - threshold)
    wheels.on_for_distance(SpeedPercent(15), threshold)


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
wait_until_distance(35)
on(speed=15)
wait_until_distance(20)

# hard turn to get off wall
wheels.turn_left(SpeedPercent(15), 45)
# arc to the left to orient towards push object
wheels.on_arc_left(SpeedPercent(30), 300, 230, brake=False)
# move forward 430 mm
forward_distance()

# reverse at an arc
wheels.on_arc_right(SpeedPercent(-50), 200, 225, brake=False)
# reverse for 145 mm
wheels.on_for_distance(SpeedPercent(-30), 155)
# reverse at an arc, orient touch sensor towards wall
wheels.on_arc_left(SpeedPercent(-50), 175, 115, brake=False)

# move back at 50% speed until touch sensor is pressed
on(speed=-50)
while not touch.is_pressed:
    pass

# rotate right 90 degrees
wheels.turn_right(SpeedPercent(35), 90)
# move forward 110 mm
forward_distance(110)

# return to the base, avoiding obstacles
return_to_base()
