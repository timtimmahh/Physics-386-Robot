from ev3dev2.motor import MediumMotor
from ev3dev2.sensor.lego import TouchSensor

from classes import Mission, Gyro, Wheels, Claw, WreckingBall


class WreckingBallMission(Mission):

    def __init__(self, gyro: Gyro, wheels: Wheels, claw: Claw, touch: TouchSensor, side_motor: MediumMotor) -> None:
        super().__init__(gyro, wheels, claw, touch, side_motor)
        self.wrecking_ball = WreckingBall(side_motor)

    def perform(self):
        init_angle = self.gyro.calibrate()
        # move forward at 50% speed until within a distance of 20 cm
        # self.ensure_straight_until(50, 20, init_angle)
        self.on(50)
        self.claw.wait_until_distance(20)

        # turn the wheels off
        self.wheels.off()

        # slam the wrecking ball/hammer 11 times, rotating left 7.2 degrees in between slam
        self.wrecking_ball.slam(11, on_slam=lambda: self.wheels.turn_left(30, 7.2))

        self.wheels.turn_left(50, 90 - (self.gyro.angle - init_angle))
        self.wheels.on_for_rotations(0, 30, 1)
        self.wheels.on_for_rotations(0, 30, -1)
        self.wheels.turn_right(50, self.gyro.angle - init_angle)

        # reverse at 50% speed until the touch sensor hits the wall
        self.on(-50)
        self.touch.wait_for_pressed(sleep_ms=None)

        # stop all motors
        self.release_motors()

    @classmethod
    def get_name(cls):
        return 'Wrecking Ball'
