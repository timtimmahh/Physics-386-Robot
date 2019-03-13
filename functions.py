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

    repeat_until_button_press()

    while not button.any():
        if ts.is_pressed:
            leds.set_color("LEFT", "GREEN")
            leds.set_color("RIGHT", "GREEN")
        else:
            leds.set_color("LEFT", "RED")
            leds.set_color("RIGHT", "RED")


def test_color_sensor():
    ls = ColorSensor(INPUT_4)
    ls.command(LightSensor.MODE_REFLECT)

    print(f'Reflected light intensity is: ')


def test_ultrasonic_sensor():
    pass

def test_gyro_sensor():
    pass


while not button.any():
    test_touch_sensor()
    test_color_sensor()
