import time

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveDifferential, MoveSteering, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor
from ev3dev2.wheel import EV3EducationSetTire

spear_head = MediumMotor(OUTPUT_C)

wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
wheelsV2 = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, 110)
front_claw = MediumMotor(OUTPUT_D)
extend_arm = MediumMotor(OUTPUT_C)
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
while proximity_sensor.distance_centimeters >= 20:
    print('First wall: {}'.format(proximity_sensor.distance_centimeters))

wheels.on(-79, SpeedPercent(15))

start_angle = gyro.angle
while gyro.angle > -79:
    print(gyro.angle)

wheels.on(0, SpeedPercent(20))
while proximity_sensor.distance_centimeters >= 10:
    pass
wheels.off(brake=True)

# wheels.on_for_rotations(0, SpeedPercent(10), 0.2)  # moves up to get the claw on the
extend_arm.on_for_rotations(SpeedPercent(-20), 1.2, False)

# front_claw.on_for_degrees(SpeedPercent(20), -570)  # clenches the claw
# wheels.on_for_rotations(0, SpeedPercent(10), 0.5)  # moves up to get the claw on the
# front_claw.on_for_degrees(SpeedPercent(100), 570, block=False)  #opens the claw again

#
wheels.on_for_rotations(0, SpeedPercent(-50), 1)
extend_arm.on_for_rotations(SpeedPercent(60), 1.2, False)
wheels.on_for_rotations(0, SpeedPercent(35), 1)
wheels.on_for_rotations(0, SpeedPercent(-50), 1)

# front_claw.on_for_degrees(SpeedPercent(20), -570)
wheels.on(0, SpeedPercent(-25))

while not touch_sensor.is_pressed:
    pass

wheels.off()

gyro.mode = GyroSensor.MODE_GYRO_CAL
gyro.mode = GyroSensor.MODE_GYRO_RATE
gyro.mode = GyroSensor.MODE_GYRO_ANG
time.sleep(1)

# Make car do 180 and run over rest of crater
# wheels.on(-187, SpeedPercent(15))
# wheelsV2.on_for_distance(15, 50)
# wheels.on(187, SpeedPercent(15))
# wheelsV2.on_for_distance(15, -50)


wheels.on(-85, SpeedPercent(15))

while gyro.angle > -85:
    print('Gyro angle {}'.format(gyro.angle))

wheels.on(0, SpeedPercent(25))

while proximity_sensor.distance_centimeters >= 16:
    pass

# wheels.on(-100, SpeedPercent(-50))
# start_angleV2 = gyro.angle
# while gyro.angle > -80:
#    print(gyro.angle)

# wheelsV2.on_for_distance(50, 100)

# wheelsV2.on_arc_left(50, 80)

wheels.off(brake=False)
extend_arm.off(brake=False)
