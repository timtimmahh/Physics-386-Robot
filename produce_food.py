from ev3dev2.motor import MediumMotor
from ev3dev2.sensor.lego import TouchSensor

from classes import Mission, Gyro, Wheels, Claw


class ProduceFoodMission(Mission):

    def __init__(self, gyro: Gyro, wheels: Wheels, claw: Claw, touch: TouchSensor, side_motor: MediumMotor) -> None:
        super().__init__(gyro, wheels, claw, touch, side_motor)
        # calibrate gyro
        self.init_angle = 0

    def forward_carefully(self, distance=420, threshold=15):
        """
        Move forward with a speed of 30% for (distance - threshold) mm then move threshold mm at 5% speed.
        """
        # init_rotations = self.wheels.get_rotations()
        # init_angle = self.gyro.angle
        # move straight with distance - threshold at 30% speed
        if distance != 0:
            self.wheels.on_for_distance(-30 if distance < 0 else 30, abs(distance) - threshold)
        # threshold += self.ensure_straight(30, distance - threshold, init_rotations, init_angle)
        # carefully move forward at 5% speed for threshold distance
        if threshold > 0:
            self.wheels.on_for_distance(5, threshold)

    def rotate_until_closest(self, degrees=45):
        """
        Rotate right until lined up with the closest object.
        """
        # gyro_init = self.gyro.angle
        # turn slowly
        self.wheels.turn_right(5, degrees)
        # distances = []
        # while abs(self.gyro.angle - gyro_init) < degrees:
        #     distances.append((abs(self.gyro.angle - gyro_init), self.claw.eyes.distance_centimeters))
        # print('\n'.join(str(distance) for distance in distances))

    def return_to_base(self):
        """
        Return to the base by moving in an S form around obstacles.
        """
        self.wheels.on_arc_left(-40, 180, 250)
        self.wheels.on_arc_right(-40, 190, 470)
        self.wheels.on_arc_left(-40, 180, 230)
        self.on(speed=-65)
        self.touch.wait_for_pressed(sleep_ms=None)
        # while not self.touch.is_pressed:
        #     pass
        self.release_motors()
        # self.wheels.off(brake=False)

    def perform(self):
        self.init_angle = self.gyro.calibrate()
        # go forward until nearest object is within 25 cm
        self.on(50)
        self.claw.wait_until_distance()

        # hard turn to get off wall
        self.wheels.turn_left(15, 45, brake=False)
        # arc to the left to orient towards push object
        self.wheels.on_arc_left(30, 300, 230, brake=False)
        # move forward carefully 430 mm
        self.forward_carefully(threshold=30)

    @classmethod
    def get_name(cls):
        return 'Produce Food'


class ProduceFoodOrbitsMission(ProduceFoodMission):

    def perform(self):
        # perform produce food
        super().perform()

        self.wheels.off()
        # move backward carefully 30 mm
        self.forward_carefully(0, -30)
        # self.wheels.on_for_distance(-15, 30)
        # rotate until facing satellite
        self.wheels.turn_right(5, 45)

        # grab the satellite when close enough and turn off the wheels
        self.on(30)
        self.claw.grab_when_within(distance_cm=10.0, on_close=self.wheels.off)

        # reverse at an arc of 55 for 55 mm
        self.wheels.on_arc_right(-25, 55, 55)
        # self.wheels.on_arc_right(-40, 300, 150)
        print('Current angle: {} turn angle: {}'.format(self.gyro.angle, 90 - (self.gyro.angle - self.init_angle)))
        self.wheels.turn_left(10, 90 - (self.gyro.angle - self.init_angle))
        self.wheels.on_for_distance(-5, 25)
        # drop the satellite
        self.claw.open()
        # reverse at 50% speed until touch sensor hits the wall
        self.on(-50)
        self.touch.wait_for_pressed(sleep_ms=None)
        self.wheels.off()
        # rotate right 90 degrees to face the observatory
        print('Current angle: {} turn angle: {}'.format(self.gyro.angle, self.gyro.angle - self.init_angle))
        self.wheels.turn_right(15, self.gyro.angle - self.init_angle)
        if self.gyro.angle != self.init_angle:
            self.wheels.turn(15, self.gyro.angle - self.init_angle)
        # move carefully pushing the observatory
        self.forward_carefully(0, threshold=90)

        # mission complete, return to the base
        self.return_to_base()

    @classmethod
    def get_name(cls):
        return super().get_name() + ' Orbits'


class ProduceFoodObservatoryMission(ProduceFoodMission):

    def perform(self):
        super().perform()

        # reverse at an arc
        self.wheels.on_arc_right(-50, 200, 225, brake=False)
        # reverse for 145 mm
        self.wheels.on_for_distance(-30, 155)
        # reverse at an arc, orient touch sensor towards wall
        self.wheels.on_arc_left(-50, 175, 115, brake=False)

        # move back at 50% speed until touch sensor is pressed
        self.on(speed=-50)
        self.touch.wait_for_pressed(sleep_ms=None)
        # while not self.touch.is_pressed:
        #     pass

        # rotate right 90 degrees
        self.wheels.turn_right(35, 90)
        # move forward 110 mm
        self.forward_carefully(110)

        # return to the base, avoiding obstacles
        self.return_to_base()

    @classmethod
    def get_name(cls):
        return super().get_name() + ' Observatory'
