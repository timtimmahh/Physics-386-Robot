from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_3
from ev3dev2.sensor.lego import TouchSensor

from classes import Claw, Wheels, Gyro
from produce_food import ProduceFoodOrbitsMission
from pushsat import PushSatMission
from repair_station import RepairStationMission
from wreckingball import WreckingBallMission

buttons = Button()
touch = TouchSensor(INPUT_3)
side_motor = MediumMotor(OUTPUT_C)
wheels = Wheels(OUTPUT_A, OUTPUT_B)
claw = Claw()
gyro = Gyro(INPUT_1)
cancel_all = False

missions = [mission(gyro, wheels, claw, touch, side_motor) for mission in [ProduceFoodOrbitsMission,
                                                                           PushSatMission,
                                                                           WreckingBallMission,
                                                                           RepairStationMission]]


def wait_for_next_mission(previous_mission, next_mission):
    global cancel_all
    print('Waiting to start mission: prev={}, next={}'.format(previous_mission.get_name() if previous_mission else 'None',
                                                              next_mission.get_name()))
    while not cancel_all:
        if buttons.left and previous_mission:
            print('Starting previous mission: {}'.format(previous_mission.get_name()))
            previous_mission.perform()
            break
        elif buttons.right:
            break
        elif buttons.enter and next_mission:
            print('Starting next mission: {}'.format(next_mission.get_name()))
            next_mission.perform()
            break
        elif buttons.backspace:
            cancel_all = True
    return cancel_all


# for i in range(len(missions)):
#     if wait_for_next_mission(previous_mission=None if i == 0 else missions[i-1], next_mission=missions[i]):
#         break

missions[0].perform()
