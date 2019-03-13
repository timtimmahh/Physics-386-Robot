#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds

button = Button()


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
