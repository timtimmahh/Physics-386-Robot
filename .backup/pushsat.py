from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor

pusher = MediumMotor(OUTPUT_C)
wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
proximity_sensor = UltrasonicSensor(INPUT_2)
ts = TouchSensor(INPUT_3)

wheels.on(0, SpeedPercent(50))

while True:
    if proximity_sensor.distance_centimeters <= 12:
        break

wheels.off(brake=True)

pusher.on_for_rotations(SpeedPercent(-100), 4, block=True)  # goes forward
pusher.on_for_rotations(SpeedPercent(50), 2, block=False)  # goes backward

wheels.on(0, SpeedPercent(-50))
while True:
    if ts.is_pressed:
        break

wheels.off(brake=False)
pusher.off(brake=False)
