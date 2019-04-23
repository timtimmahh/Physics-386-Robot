from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveSteering, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor

button = Button()
touch_sensor = TouchSensor(INPUT_3)
wrecking_ball = MediumMotor(OUTPUT_C)
wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
eyes = UltrasonicSensor(INPUT_2)


# wheels.on(0, SpeedPercent(65))


def slam():
    wrecking_ball.on_for_rotations(SpeedPercent(100), 1.25)
    wrecking_ball.on_for_rotations(SpeedPercent(-50), 1.25)


while True:
    slam()
    if touch_sensor.is_pressed:
        break

wrecking_ball.off(brake=False)
'''
while True:
    if eyes.distance_centimeters <= 10:
        break

wheels.off()
wheels.on_for_rotations(100, SpeedPercent(30), 0.1)

for y in range(2):
    slam()

wheels.on_for_rotations(-100, SpeedPercent(30), 0.1)

wheels.on(0, SpeedPercent(-100))

while True:
    if touch_sensor.is_pressed:
        break

wheels.off(brake=False)
wrecking_ball.off(brake=False)

'''
