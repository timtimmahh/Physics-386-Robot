from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound

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
sound = Sound()


def wait_for_next_mission(missions, index):
    if index == len(missions) + 1 or index == -1:
        return True
    print('Waiting to start mission: prev={}, next={}'.format(missions[index - 1].get_name() if index > 0 else 'None',
                                                              missions[index].get_name() if index < len(missions) else
                                                              'None'))

    while not buttons.backspace:
        if buttons.left and index > 0:
            buttons.wait_for_released([buttons.left])
            print('Starting previous mission: {}'.format(missions[index - 1].get_name()))
            missions[index - 1].perform()
            return wait_for_next_mission(missions, index)
        elif buttons.right:
            buttons.wait_for_released([buttons.right])
            return wait_for_next_mission(missions, index + 1)
        elif buttons.enter and index < len(missions) and missions[index]:
            buttons.wait_for_released([buttons.enter])
            print('Starting next mission: {}'.format(missions[index].get_name()))
            missions[index].perform()
            return wait_for_next_mission(missions, index + 1)
        elif buttons.up and index < len(missions):
            buttons.wait_for_released([buttons.up])
            return wait_for_next_mission(missions, index + 1)
        elif buttons.down and index > 0:
            buttons.wait_for_released([buttons.down])
            return wait_for_next_mission(missions, index - 1)
    return False


sound.speak('I AM THE BEETLE')

wait_for_next_mission([mission(gyro, wheels, claw, touch, side_motor) for mission in [PushSatMission,
                                                                                      WreckingBallMission,
                                                                                      RepairStationMission,
                                                                                      ProduceFoodOrbitsMission]], 0)
