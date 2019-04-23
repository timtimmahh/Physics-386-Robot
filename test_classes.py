from classes import Claw, Wheels

claw = Claw()
wheels = Wheels()

wheels.move_straight(speed=100)

claw.grab_when_within(10.0, while_waiting=lambda: print(claw.eyes.distance_centimeters))
wheels.reverse_until_bumped()
wheels.rotate_left_in_place(amount=0.5, brake=False)
wheels.move_for_distance(distance_mm=300)
wheels.stop()
claw.open()
