from ev3dev2.motor import OUTPUT_C, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor

SPEED = SpeedPercent(15)


class FlySwatter:

    def __init__(self, sensorMotorOutput=OUTPUT_C, touchSensorInput=INPUT_4):
        self._sensorMotor = MediumMotor(sensorMotorOutput)
        self._touchSensor = UltrasonicSensor(touchSensorInput)
        self._sensorReadings = []

    def scan_right(self):
        self._sensorReadings = []

        num_rotations = self._sensorMotor.rotations
        self._sensorMotor.on_for_rotations(SPEED, rotations=0.25, block=False)
        while self._sensorMotor.rotations - num_rotations <= 0.25:
            self._sensorReadings.append(
                (round(self._sensorMotor.rotations, 2), round(self._touchSensor.distance_centimeters, 2)))

        print(self._sensorReadings)
        self._sensorMotor.off(brake=False)

    def scan_left(self):
        self._sensorReadings = []

        num_rotations = self._sensorMotor.rotations
        self._sensorMotor.on_for_rotations(SPEED, rotations=-0.25, block=False)
        while self._sensorMotor.rotations - num_rotations > -0.25:
            print(self._sensorMotor.rotations - num_rotations)
            self._sensorReadings.append(
                (round(self._sensorMotor.rotations, 2), round(self._touchSensor.distance_centimeters, 2)))

        print(self._sensorReadings)
        self._sensorMotor.off(brake=False)

    def take_in_readings_from_sensor(self):
        self._sensorReadings = []
        for x in range(0, 150):
            self._sensorReadings.append((self._sensorMotor.rotations, round(self._touchSensor.distance_centimeters, 2)))

        return self._sensorReadings

    def get_sensor_readings(self):
        tmp_readings = []
        for pair in self._sensorReadings:
            tmp_readings.append(pair[1])
        return tmp_readings
