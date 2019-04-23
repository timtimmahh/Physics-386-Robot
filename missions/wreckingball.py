from ev3dev2.motor import MediumMotor
from ev3dev2.sensor.lego import TouchSensor

from classes import Mission, Gyro, Wheels, Claw, WreckingBall


class WreckingBallMission(Mission):

    def __init__(self, gyro: Gyro, wheels: Wheels, claw: Claw, touch: TouchSensor, side_motor: MediumMotor) -> None:
        super().__init__(gyro, wheels, claw, touch, side_motor)
        self.wrecking_ball = WreckingBall(side_motor)

    def perform(self):
        # move forward at 50% speed until within a distance of 20 cm
        self.on(50)
        self.claw.wait_until_distance(20)

        # turn the wheels off
        self.wheels.off()

        # turn right 7.2 degrees
        self.wheels.turn_right(30, 7.2)
        # self.wheels.on_for_rotations(-100, 30, 0.02)  # turns right a little

        # slam the wrecking ball/hammer 11 times, rotating left 7.2 degrees during the 4th through 9th slams
        self.wrecking_ball.slam(11, on_slam=[... for _ in range(4)]
                                .extend([lambda: self.wheels.turn_left(30, 7.2) for _ in range(5)])
                                .extend([... for _ in range(2)]))

        # for x in range(4):
        #     wrecking_ball.slam()
        #
        # for z in range(5):
        #     wheels.on_for_rotations(100, 30, 0.02)
        #     wrecking_ball.slam()
        #
        # for y in range(2):
        #     wrecking_ball.slam()

        # closes and opens the claw, performing necessary rotations in-between
        for between in ((lambda: self.wheels.on_for_rotations(-100, 30, 0.35),),
                        (lambda: self.wheels.on_for_rotations(0, 100, 0.1),
                         lambda: self.wheels.on_for_rotations(0, -100, 0.1)),
                        (lambda: None,)):
            self.claw.close()
            for do in between:
                do()
            self.claw.open()
        # claw.close()
        # wheels.on_for_rotations(-100, 30, 0.35)  # turns right a little
        # claw.open()
        # wheels.on_for_rotations(0, 100, 0.1)  # goes forward
        # wheels.on_for_rotations(0, -100, 0.1)  # goes backwards
        # claw.close()
        # claw.open()
        # claw.close()
        # claw.open()

        # turn back left 36 degrees
        self.wheels.turn_left(30, 36)
        # self.wheels.on_for_rotations(100, 30, 0.1)  # turns back left

        # reverse at 50% speed until the touch sensor hits the wall
        self.on(-50)
        self.touch.wait_for_pressed(sleep_ms=None)

        # stop all motors
        self.release_motors()

    @classmethod
    def get_name(cls):
        return 'Wrecking Ball'
