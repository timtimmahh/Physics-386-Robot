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
        print(f'Motor at {output} set to {motor.command}')
        motor.on_for_rotations(30, 0.5)
        print_and_wait(motor)
        motor.on_for_degrees(30, 45)
        print_and_wait(motor)
        motor.on_to_position(30, 5)
        print_and_wait(motor)
        motor.on_for_seconds(30, 3)
        print_and_wait(motor)


def print_and_wait(*motors: Motor):

    print(''.join([f'MOTOR: {motor.address} - Tacho count per meters: {motor.count_per_m}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Tacho count per rotation: {motor.count_per_rot}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Full tacho count for travel: {motor.full_travel_count}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Duty cycle: {motor.duty_cycle}, Duty cycle set point: {motor.duty_cycle_sp}'
                   for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Polarity: {motor.polarity}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Position: {motor.position}, prop: {motor.position_p}, int: {motor.position_i},'
                   f' der: {motor.position_d}, set point: {motor.position_sp}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Max - speed: {motor.max_speed}, rot/min: {motor.max_rpm}, '
                   f'/sec: {motor.max_rps}, deg/min: {motor.max_dpm}, /sec: {motor.max_dps}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Current speed: {motor.speed}, prop: {motor.speed_p}, int: {motor.speed_i}'
                   f', der: {motor.position_d}, sp: {motor.speed_sp}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Ramp up speed: {motor.ramp_up_sp}, down: {motor.ramp_down_sp}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Current state: {motor.state}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - Current stop action: {motor.stop_action}' for motor in motors]))
    print(''.join([f'MOTOR: {motor.address} - running: {motor.is_running}, ramping: {motor.is_ramping}, '
                   f'holding: {motor.is_holding}, overloaded: {motor.is_overloaded}, stalled: {motor.is_stalled}'
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
        print(f'The current gyro mode is: {gs.mode}')
        print(f'The angle is at {gs.angle} degrees')
        print(f'The rate of rotation is {gs.rate} degrees/second')
        print(f'Here\'s both as a tuple: {gs.angle_and_rate}')
        print(f'Tilt angle: {gs.tilt_angle} degrees?')
        print(f'Tilt rate: {gs.tilt_rate} degrees/second?')
        print(f'Waiting for angle to change by 90 degrees clockwise: {gs.wait_until_angle_changed_by(90, True)}')
        print(f'Waiting for angle to change by 90 degrees any direction: {gs.wait_until_angle_changed_by(90, False)}')

    while not button.any():
        print(f'Angle: {gs.angle}, Rate: {gs.rate}')
        gs.wait_until_angle_changed_by(15, False)


def test_ultrasonic_sensor():
    us = UltrasonicSensor(INPUT_3)
    from time import sleep

    for mode in us.modes:
        us.mode = mode
        print(f'The current ultrasonic mode is: {us.mode}')
        print(f'Distance in cm: {us.distance_centimeters}, ping: {us.distance_centimeters_ping}')
        print(f'Distance in inches: {us.distance_inches}, ping: {us.distance_inches_ping}')
        print(f'Another ultrasonic sensor nearby? {us.other_sensor_present}')
        sleep(0.25)

    while not button.any():
        print(f'Inches: {us.distance_inches}, cm: {us.distance_centimeters}')
        sleep(0.25)


def test_color_sensor():
    cs = ColorSensor(INPUT_4)

    for mode in cs.modes:
        cs.mode = mode
        print(f'The current color mode is: {cs.mode}')
        print(f'{cs.raw} is the same as {cs.rgb} - (Red, Green, Blue)')
        print(f'{cs.color}: {cs.color_name}')
        hue, luminance, saturation = cs.hls
        print(f'Hue: {hue}, Luminance: {luminance}, Saturation: {saturation}')
        hue, saturation, value = cs.hsv
        print(f'Hue: {hue}, Saturation: {saturation}, Value: {value}')
        print(f'Ambient light intensity: {cs.ambient_light_intensity}')
        print(f'Reflected light intensity: {cs.reflected_light_intensity}')

    while not button.any():
        print(f'Color: {cs.rgb} which is {cs.color_name}')
        print(f'Ambient light intensity: {cs.ambient_light_intensity}')
        print(f'Reflected light intensity: {cs.reflected_light_intensity}')


test_touch_sensor()
test_gyro_sensor()
test_ultrasonic_sensor()
test_color_sensor()
