from produce_food import produce_food, wheels, claw, on, forward_distance, rotate_until_closest

produce_food()

forward_distance(-30, 0)
rotate_until_closest()

on(15)

claw.grab_when_within(distance_cm=5.0, on_close=lambda: wheels.off())
forward_distance(-160)
claw.open()
forward_distance(-100)
