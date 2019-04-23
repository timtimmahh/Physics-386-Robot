from classes import Claw, Wheels

claw = Claw()
wheels = Wheels()

wheels.move_straight(speed=100)


def on_wait():
    print(claw._us_sensor.distance_centimeters)


claw.grab_when_within(10.0)
wheels.reverse_until_bumped()
wheels.rotate_left_in_place(amount=0.5, brake=False)
wheels.move_for_distance(distance_mm=300)
wheels.stop()
claw.open()
