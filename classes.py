from datetime import datetime

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MediumMotor, SpeedPercent, MoveSteering, MoveDifferential
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor
from ev3dev2.wheel import EV3EducationSetTire


class Claw:

    def __init__(self, motor_address=OUTPUT_D, us_sensor_address=INPUT_2):
        self._claw = MediumMotor(motor_address)
        self._us_sensor = UltrasonicSensor(us_sensor_address)
        self.is_open = False

    def open(self):
        if self.is_open:
            self.close()
        self._claw.on_for_degrees(SpeedPercent(50), 570, brake=False, block=True)
        self.is_open = True

    def close(self):
        if not self.is_open:
            self.open()
        self._claw.on_for_degrees(SpeedPercent(50), -570, brake=False, block=True)
        self.is_open = False

    def grab_when_within(self, distance_cm=5.0, while_waiting=None, cancel=None):
        self.open()
        while self._us_sensor.distance_centimeters >= distance_cm:
            if cancel and cancel():
                return False
            if while_waiting:
                while_waiting()
        self.close()
        return True

    def release(self):
        self._claw.off()


class Wheels:

    def __init__(self, left_address=OUTPUT_A, right_address=OUTPUT_B, touch_address=INPUT_3):
        self._wheels = MoveSteering(left_address, right_address)
        self._left = self._wheels.left_motor
        self._right = self._wheels.right_motor
        self._touch = TouchSensor(touch_address)

    def move_straight(self, speed=50):
        self._wheels.on(0, SpeedPercent(speed))

    def move_for_distance(self, speed=50, distance_mm=100):
        MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, 80).on_for_distance(speed, distance_mm, brake=False)

    def rotate_right_in_place(self, speed=50, amount=1.0, brake=True, block=True):
        self._wheels.on_for_rotations(-100, SpeedPercent(speed), amount, brake=brake, block=block)

    def rotate_left_in_place(self, speed=50, amount=1.0, brake=True, block=True):
        self._wheels.on_for_rotations(100, SpeedPercent(speed), amount, brake=brake, block=block)

    def reverse(self, speed=50):
        self._wheels.on(0, SpeedPercent(-speed))

    def reverse_until_bumped(self, speed=50, timeout=None):
        self.reverse(speed)
        time = datetime.now()
        ms = time.microsecond
        while not timeout or time.microsecond - ms < timeout:
            if self._touch.is_pressed:
                self._wheels.off()
                break

    def stop(self):
        self._wheels.off(brake=False)
