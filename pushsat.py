from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor

pusher = MediumMotor(OUTPUT_C)
wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
proximity_sensor = UltrasonicSensor(INPUT_2)
ts = TouchSensor(INPUT_3)
claw = MediumMotor(OUTPUT_D)

claw.on_for_degrees(SpeedPercent(35), 570)
wheels.on(0, SpeedPercent(50))

while proximity_sensor.distance_centimeters >= 13:
    pass

wheels.off(brake=True)

pusher.on_for_rotations(SpeedPercent(-100), 7)

wheels.on(0, SpeedPercent(-50))
while True:
    if ts.is_pressed:
        break

wheels.off(brake=False)
pusher.off(brake=False)
