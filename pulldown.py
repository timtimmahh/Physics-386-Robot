import time

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor

spear_head = MediumMotor(OUTPUT_C)

wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
front_claw = MediumMotor(OUTPUT_D)
proximity_sensor = UltrasonicSensor(INPUT_2)
touch_sensor = TouchSensor(INPUT_3)
button = Button()
gyro = GyroSensor(INPUT_1)
'''
spear_head.on_for_rotations(SpeedPercent(60), 3)
spear_head.on_for_rotations(SpeedPercent(-60), 3)
spear_head.off(brake=False)
'''

gyro.mode = GyroSensor.MODE_GYRO_CAL
gyro.mode = GyroSensor.MODE_GYRO_RATE
gyro.mode = GyroSensor.MODE_GYRO_ANG
time.sleep(1)

front_claw.on_for_degrees(SpeedPercent(20), 570)  # opens the claw
wheels.on(0, SpeedPercent(50))
while proximity_sensor.distance_centimeters >= 22:
    print('First wall: {}'.format(proximity_sensor.distance_centimeters))


wheels.on(-100, SpeedPercent(15))

start_angle = gyro.angle
while gyro.angle > -82:
    print(gyro.angle)

wheels.on(0, SpeedPercent(50))
while proximity_sensor.distance_centimeters >= 12:
    pass
wheels.off(brake=True)

front_claw.on_for_degrees(SpeedPercent(20), -570)  # clenches the claw
wheels.on_for_rotations(0, SpeedPercent(25), 0.5)  # moves up to get the claw on the
front_claw.on_for_degrees(SpeedPercent(100), 570, block=False)  # opens the claw again
wheels.on_for_rotations(0, SpeedPercent(-100), 0.5)
wheels.on_for_rotations(0, SpeedPercent(100), 0.5)
wheels.on_for_rotations(0, SpeedPercent(-100), 0.5)

front_claw.on_for_degrees(SpeedPercent(20), -570)
wheels.on(0, SpeedPercent(-50))

while not touch_sensor.is_pressed:
    pass

wheels.off()

gyro.mode = GyroSensor.MODE_GYRO_CAL
gyro.mode = GyroSensor.MODE_GYRO_RATE
gyro.mode = GyroSensor.MODE_GYRO_ANG
time.sleep(1)

wheels.on(-100, SpeedPercent(15))


while gyro.angle > -90:
    print('Gyro angle {}'.format(gyro.angle))

wheels.on(0, SpeedPercent(50))

while proximity_sensor.distance_centimeters >= 10:
    pass

wheels.off(brake=False)
