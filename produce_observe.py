from ev3dev2.motor import SpeedPercent

from produce_food import produce_food, touch, wheels, on, forward_distance, return_to_base

produce_food()

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
