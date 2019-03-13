#!/usr/bin/env python3
from ev3dev2.motor import Motor, LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds

button = Button()


def test_left_motor():
    test_single_motor(OUTPUT_A)


def test_right_motor():
    test_single_motor(OUTPUT_B)


def test_single_motor(output):
    motor = LargeMotor(output)

    for command in motor.commands:
        motor.command = command
        print('Motor at {} set to {}'.format(output, motor.command))
        motor.on_for_rotations(30, 0.5)
        print_and_wait(motor)
        motor.on_for_degrees(30, 45)
        print_and_wait(motor)
        motor.on_to_position(30, 5)
        print_and_wait(motor)
        motor.on_for_seconds(30, 3)
        print_and_wait(motor)


def print_and_wait(*motors: Motor):
    print(''.join(['MOTOR: {} - Tacho count per meters: {}'.format(motor.address, motor.count_per_m) for motor in motors]))
    print(''.join(['MOTOR: {} - Tacho count per rotation: {}'.format(motor.address, motor.count_per_rot) for motor in
                   motors]))
    print(''.join(['MOTOR: {} - Full tacho count for travel: {}'.format(motor.address, motor.full_travel_count) for motor
                   in motors]))
    print(''.join(
        ['MOTOR: {} - Duty cycle: {}, Duty cycle set point: {}'.format(motor.address, motor.duty_cycle, motor.duty_cycle_sp)
         for motor in motors]))
    print(''.join(['MOTOR: {} - Polarity: {}'.format(motor.address, motor.polarity) for motor in motors]))
    print(''.join(['MOTOR: {} - Position: {}, prop: {}, int: {},'
                   ' der: {}, set point: {}'.format(motor.address, motor.position, motor.position_p,
                                                    motor.position_i, motor.position_d, motor.position_sp) for motor in
                   motors]))
    print(''.join(['MOTOR: {} - Max - speed: {}, rot/min: {}, '
                   '/sec: {}, deg/min: {}, /sec: {}'.format(motor.address,
                                                            motor.max_speed,
                                                            motor.max_rpm,
                                                            motor.max_rps, motor.max_dpm, motor.max_dps) for motor in
                   motors]))
    print(''.join(['MOTOR: {} - Current speed: {}, prop: {}, int: {}'
                   ', der: {}, sp: {}'.format(motor.address, motor.speed, motor.speed_p,
                                              motor.speed_i, motor.position_d, motor.speed_sp
                                              ) for motor in
                   motors]))
    print(''.join(['MOTOR: {} - Ramp up speed: {}, down: {}'
                  .format(motor.address, motor.ramp_up_sp, motor.ramp_down_sp) for motor in motors]))
    print(''.join(['MOTOR: {} - Current state: {}'.format(motor.address, motor.state) for motor in motors]))
    print(''.join(['MOTOR: {} - Current stop action: {}'.format(motor.address, motor.stop_action) for motor in motors]))
    print(''.join(['MOTOR: {} - running: {}, ramping: {}, '
                   'holding: {}, overloaded: {}, stalled: {}'.format(
        motor.address, motor.is_running, motor.is_ramping, motor.is_holding, motor.is_overloaded, motor.is_stalled)
        for motor in motors]))
    for motor in motors:
        motor.wait_until_not_moving()


def test_both_motors(steering: bool = False):
    ms = MoveSteering(OUTPUT_A, OUTPUT_B) if steering else MoveTank(OUTPUT_A, OUTPUT_B)


def test_touch_sensor():
    ts = TouchSensor(INPUT_1)
    leds = Leds()

    print("Press the touch sensor to change the LED color!")

    while not button.any():
        if ts.is_pressed:
            leds.set_color("LEFT", "GREEN")
            leds.set_color("RIGHT", "GREEN")
        else:
            leds.set_color("LEFT", "RED")
            leds.set_color("RIGHT", "RED")


def test_gyro_sensor():
    gs = GyroSensor(INPUT_2)

    for mode in gs.modes:
        gs.mode = mode
        print('The current gyro mode is: {}'.format(gs.mode))
        print('The angle is at {} degrees'.format(gs.angle))
        print('The rate of rotation is {} degrees/second'.format(gs.rate))
        print('Here\'s both as a tuple: {}'.format(gs.angle_and_rate))
        print('Tilt angle: {} degrees?'.format(gs.tilt_angle))
        print('Tilt rate: {} degrees/second?'.format(gs.tilt_rate))
        print('Waiting for angle to change by 90 degrees clockwise: {}'.format(gs.wait_until_angle_changed_by(90, True)))
        print('Waiting for angle to change by 90 degrees any direction: {}'.format(gs.wait_until_angle_changed_by(90, False))
              )

    while not button.any():
        print('Angle: {}, Rate: {}'.format(gs.angle, gs.rate))
        gs.wait_until_angle_changed_by(15, False)


def test_ultrasonic_sensor():
    us = UltrasonicSensor(INPUT_3)
    from time import sleep

    for mode in us.modes:
        us.mode = mode
        print('The current ultrasonic mode is: {}'.format(us.mode))
        print('Distance in cm: {}, ping: {}'.format(us.distance_centimeters, us.distance_centimeters_ping))
        print('Distance in inches: {}, ping: {}'.format(us.distance_inches, us.distance_inches_ping))
        print('Another ultrasonic sensor nearby? {}'.format(us.other_sensor_present))
        sleep(0.25)

    while not button.any():
        print('Inches: {}, cm: {}'.format(us.distance_inches, us.distance_centimeters))
        sleep(0.25)


def test_color_sensor():
    cs = ColorSensor(INPUT_4)

    for mode in cs.modes:
        cs.mode = mode
        print('The current color mode is: {}'.format(cs.mode))
        print('{} is the same as {} - (Red, Green, Blue)'.format(cs.raw, cs.rgb))
        print('{}: {}'.format(cs.color, cs.color_name))
        hue, luminance, saturation = cs.hls
        print('Hue: {}, Luminance: {}, Saturation: {}'.format(hue, luminance, saturation))
        hue, saturation, value = cs.hsv
        print('Hue: {}, Saturation: {}, Value: {}'.format(hue, saturation, value))
        print('Ambient light intensity: {}'.format(cs.ambient_light_intensity))
        print('Reflected light intensity: {}'.format(cs.reflected_light_intensity))

    while not button.any():
        print('Color: {} which is {}'.format(cs.rgb, cs.color_name))
        print('Ambient light intensity: {}'.format(cs.ambient_light_intensity))
        print('Reflected light intensity: {}'.format(cs.reflected_light_intensity))


test_touch_sensor()
test_gyro_sensor()
test_ultrasonic_sensor()
test_color_sensor()
