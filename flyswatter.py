from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_C, MediumMotor, SpeedPercent

fly_swatter = MediumMotor(OUTPUT_C)

button = Button()


def fly_swatting():
    fly_swatter.on_for_rotations(SpeedPercent(50), rotations=5, block=False)


'''
def swivel_swatter():
    while not button.any():
        fly_swatter.on_for_rotations(SpeedPercent(100), 0.25)
        fly_swatter.on_for_rotations(SpeedPercent(100), -0.25)

'''
