from ev3dev2.motor import MediumMotor
from ev3dev2.sensor.lego import TouchSensor

from classes import Mission, Gyro, Wheels, Claw


class PushSatMission(Mission):

    def __init__(self, gyro: Gyro, wheels: Wheels, claw: Claw, touch: TouchSensor, side_motor: MediumMotor) -> None:
        super().__init__(gyro, wheels, claw, touch, side_motor)
        self.pusher = side_motor
        self.init_angle = 0

    def perform(self):
        # move forward at 50% speed until nearest object within 12 cm
        self.init_angle = self.gyro.calibrate()

        # self.ensure_straight_until(50, 20, self.init_angle)
        self.on(50)
        self.claw.wait_until_distance(20)

        # turn the wheels off
        self.wheels.off()
        # push the arm forward 4 rotations
        self.pusher.on_for_rotations(-100, 4)  # goes forward
        # bring the arm back 2 rotations
        self.pusher.on_for_rotations(50, 4, block=False)  # goes backward

        # reverse at 50% speed until touch sensor hits the wall
        self.on(-50)
        self.touch.wait_for_pressed(sleep_ms=None)

        # stop all motors
        self.release_motors()

    @classmethod
    def get_name(cls):
        return 'Push Satellite'
