from abc import ABC, abstractmethod
from time import sleep

from ev3dev2.motor import OUTPUT_C, OUTPUT_D, MediumMotor, LargeMotor, SpeedValue, SpeedPercent, MoveSteering, \
    MoveDifferential
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor
from ev3dev2.wheel import EV3EducationSetTire


class Claw:

    def __init__(self, motor_address=OUTPUT_D, us_sensor_address=INPUT_2, start_open=True):
        self.claw_motor = MediumMotor(motor_address)
        self.eyes = UltrasonicSensor(us_sensor_address)
        if start_open and not self.is_open():
            self.open()
        elif not start_open and self.is_open():
            self.close()

    def open(self):
        if self.is_open():
            self.close()
        self.claw_motor.on_to_position(SpeedPercent(100), 0, brake=False, block=True)

    def close(self):
        if not self.is_open():
            self.open()
        self.claw_motor.on_for_rotations(SpeedPercent(100), -1.6 + self.get_rotations(), brake=False, block=True)

    def grab_when_within(self, distance_cm=5.0, on_close=None, while_waiting=None, cancel=None):
        if not self.is_open():
            self.open()
        while self.eyes.distance_centimeters >= distance_cm:
            if cancel and cancel():
                return False
            if while_waiting:
                while_waiting()
        if on_close:
            on_close()
        self.close()
        return True

    def release(self):
        self.claw_motor.off(brake=False)

    def wait_until_distance(self, distance_cm=25, on_wait=None):
        while self.eyes.distance_centimeters > distance_cm:
            if on_wait:
                on_wait()

    def get_rotations(self):
        return self.claw_motor.rotations

    def is_open(self):
        return abs(self.get_rotations()) < 0.1

    def is_closed(self):
        return abs(self.get_rotations())


class Wheels(MoveSteering):

    def __init__(self, left_motor_port, right_motor_port, desc=None, motor_class=LargeMotor):
        super().__init__(left_motor_port, right_motor_port, desc, motor_class)
        self.diff = MoveDifferential(left_motor_port, right_motor_port, EV3EducationSetTire, 110, desc, motor_class)

    def get_rotations(self):
        return (self.diff.left_motor.rotations + self.diff.right_motor.rotations) / 2.0

    def distance_remaining(self, total_distance, initial_rotations):
        return total_distance - ((self.get_rotations() - initial_rotations) * self.diff.circumference_mm)

    @staticmethod
    def __speed(speed):
        return speed if isinstance(speed, SpeedValue) else SpeedPercent(speed)

    def on_for_rotations(self, steering, speed, rotations, brake=True, block=True):
        super().on_for_rotations(steering, self.__speed(speed), rotations, brake, block)

    def on_for_degrees(self, steering, speed, degrees, brake=True, block=True):
        super().on_for_degrees(steering, self.__speed(speed), degrees, brake, block)

    def on_for_seconds(self, steering, speed, seconds, brake=True, block=True):
        super().on_for_seconds(steering, self.__speed(speed), seconds, brake, block)

    def on(self, steering, speed):
        super().on(steering, self.__speed(speed))

    def get_speed_steering(self, steering, speed):
        return super().get_speed_steering(steering, self.__speed(speed))

    def on_for_distance(self, speed, distance_mm, brake=True, block=True):
        self.diff.on_for_distance(self.__speed(speed), distance_mm, brake, block)

    def on_arc_right(self, speed, radius_mm, distance_mm, brake=True, block=True):
        self.diff.on_arc_right(self.__speed(speed), radius_mm, distance_mm, brake, block)

    def on_arc_left(self, speed, radius_mm, distance_mm, brake=True, block=True):
        self.diff.on_arc_left(self.__speed(speed), radius_mm, distance_mm, brake, block)

    def turn_right(self, speed, degrees, brake=True, block=True):
        self.diff.turn_right(self.__speed(speed), degrees, brake, block)

    def turn_left(self, speed, degrees, brake=True, block=True):
        self.diff.turn_left(self.__speed(speed), degrees, brake, block)

    def turn(self, speed, degrees, brake=True, block=True):
        (self.turn_left if degrees < 0 else self.turn_right)(speed, degrees, brake, block)


class WreckingBall:

    def __init__(self, side_motor=MediumMotor(OUTPUT_C)) -> None:
        super().__init__()
        self.wb = side_motor

    def slam(self, repeat=1, on_slam=None):
        for i in range(repeat):
            self.wb.on_for_rotations(SpeedPercent(100), 1.25)
            self.wb.on_for_rotations(SpeedPercent(-50), 1.25)
            if on_slam:
                if type(on_slam) == list and on_slam[i]:
                    on_slam[i]()
                else:
                    on_slam()


class Gyro(GyroSensor):

    def calibrate(self):
        self.mode = GyroSensor.MODE_GYRO_CAL
        sleep(1)
        self.mode = GyroSensor.MODE_GYRO_RATE
        self.mode = GyroSensor.MODE_GYRO_ANG
        return self.angle


class Mission(ABC):

    def __init__(self, gyro: Gyro, wheels: Wheels, claw: Claw, touch: TouchSensor, side_motor: MediumMotor) -> None:
        super().__init__()
        self.gyro = gyro
        self.wheels = wheels
        self.claw = claw
        self.touch = touch
        self.side_motor = side_motor

    @abstractmethod
    def perform(self):
        pass

    @classmethod
    @abstractmethod
    def get_name(cls):
        return 'Mission'

    def on(self, speed):
        self.wheels.on(0, speed)

    def ensure_straight(self, speed, total_distance, init_rotations, init_angle):
        """
        Use the self.gyro to correct any curves when attempting to go straight.
        """
        self.wheels.on_for_distance(speed, total_distance)
        while self.wheels.distance_remaining(total_distance, init_rotations) > 0:
            if self.gyro.angle != init_angle:
                self.wheels.turn(20, self.gyro.angle - init_angle)
                # if self.gyro.angle < init_angle:
                #     self.wheels.turn_left(20, angle_offset())
                # elif self.gyro.angle > init_angle:
                #     self.wheels.turn_right(20, angle_offset())
                # elif turned:
                self.wheels.on_for_distance(speed,
                                            self.wheels.distance_remaining(total_distance, init_rotations))
        return self.wheels.distance_remaining(total_distance, init_rotations)

    def release_motors(self):
        self.wheels.off(brake=False)
        self.side_motor.off(brake=False)
        self.claw.claw_motor.off(brake=False)
