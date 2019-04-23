from classes import Mission, Gyro, Wheels, Claw, TouchSensor, MediumMotor


class RepairStationMission(Mission):

    def __init__(self, gyro: Gyro, wheels: Wheels, claw: Claw, touch: TouchSensor, side_motor: MediumMotor) -> None:
        super().__init__(gyro, wheels, claw, touch, side_motor)
        # calibrate the GyroSensor
        self.gyro.calibrate()

    def perform(self):
        # close the claw by 0.7 rotations (the width of the station)
        self.claw.claw_motor.on_for_rotations(100, -0.7)
        # orient towards the station
        self.wheels.turn_left(10, 13.5)

        # move forward at 35% for 1000 mm using the self.gyro to ensure moving straight
        base_speed = 35
        distance_to_ship = 1000
        self.ensure_straight(base_speed, distance_to_ship, self.wheels.get_rotations(), self.gyro.angle)

        # push the tube module all the way in by moving back and forth twice
        for distance in (75, 125):
            self.wheels.on_for_distance(base_speed, distance)
            self.wheels.on_for_distance(-base_speed, distance)

        # go back to the base ensuring orientation
        self.ensure_straight(-60, 900, self.wheels.get_rotations(), self.gyro.angle)
        # rotate towards the wall
        self.wheels.turn_right(10, 13.5)
        # move backwards until the touch sensor hits the wall
        self.wheels.on(0, -60)
        self.touch.wait_for_pressed(sleep_ms=None)

        # reset the claw to open and turn off the wheels
        self.claw.open()
        self.release_motors()
        self.wheels.off(brake=False)

    @classmethod
    def get_name(cls):
        return 'Repair Station'
