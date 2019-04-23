#!/usr/bin/python3
from multiprocessing import Value, Pipe

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering, MediumMotor, LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor
from ev3dev2.sound import Sound

from multithread_utils import start_thread

button = Button()
wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
big_claw = LargeMotor(OUTPUT_C)
claw = MediumMotor(OUTPUT_D)
gyro = GyroSensor(INPUT_1)
proximity = UltrasonicSensor(INPUT_2)
touch = TouchSensor(INPUT_3)


def grab_everything(button_pressed: Value, pipe: Pipe):
    parent_conn = pipe[0]
    claw.on_for_rotations(SpeedPercent(100), 2, block=False)
    wheels.on(0, SpeedPercent(50))
    while button_pressed.value == 0:
        if proximity.distance_centimeters < 5.0:
            # wheels.off()
            parent_conn.send(1)
            claw.on_for_rotations(SpeedPercent(50), -2)
            wheels.on_for_seconds(0, SpeedPercent(-100), 1, block=False)
            if touch.wait_for_pressed(timeout_ms=1, sleep_ms=None):
                wheels.on_for_rotations(0, SpeedPercent(100), 1)
            claw.on_for_rotations(SpeedPercent(50), 2)
            wheels.on_for_degrees(-100, SpeedPercent(100), 720)
            wheels.on(0, SpeedPercent(50))
            parent_conn.send(0)


def run_big_claw(button_pressed: Value, pipe: Pipe):
    while button_pressed.value == 0:
        big_claw.on_for_rotations(SpeedPercent(100), 0.2)
        big_claw.on_for_rotations(SpeedPercent(100), -0.2)


def play_sonic(button_pressed: Value, pipe: Pipe):
    child_conn = pipe[1]
    sound = Sound()
    # songs = ['sonic_songs/{}'.format(file) for file in listdir('sonic_songs')]
    # size = len(songs)
    # count = 0
    switch = {
        0: lambda: sound.tone([
            (392, 350, 100), (392, 350, 100), (392, 350, 100), (311.1, 250, 100),
            (466.2, 25, 100), (392, 350, 100), (311.1, 250, 100), (466.2, 25, 100),
            (392, 700, 100), (587.32, 350, 100), (587.32, 350, 100),
            (587.32, 350, 100), (622.26, 250, 100), (466.2, 25, 100),
            (369.99, 350, 100), (311.1, 250, 100), (466.2, 25, 100), (392, 700, 100),
            (784, 350, 100), (392, 250, 100), (392, 25, 100), (784, 350, 100),
            (739.98, 250, 100), (698.46, 25, 100), (659.26, 25, 100),
            (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200), (554.36, 350, 100),
            (523.25, 250, 100), (493.88, 25, 100), (466.16, 25, 100), (440, 25, 100),
            (466.16, 50, 400), (311.13, 25, 200), (369.99, 350, 100),
            (311.13, 250, 100), (392, 25, 100), (466.16, 350, 100), (392, 250, 100),
            (466.16, 25, 100), (587.32, 700, 100), (784, 350, 100), (392, 250, 100),
            (392, 25, 100), (784, 350, 100), (739.98, 250, 100), (698.46, 25, 100),
            (659.26, 25, 100), (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200),
            (554.36, 350, 100), (523.25, 250, 100), (493.88, 25, 100),
            (466.16, 25, 100), (440, 25, 100), (466.16, 50, 400), (311.13, 25, 200),
            (392, 350, 100), (311.13, 250, 100), (466.16, 25, 100),
            (392.00, 300, 150), (311.13, 250, 100), (466.16, 25, 100), (392, 700)
        ], play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE),
        1: lambda: (sound.speak("Chomp") for _ in range(5))
    }
    switch.get(0)
    while button_pressed.value == 0:
        switch.get(child_conn.recv())()


values = [Value('i', 0), Pipe()]
procs = start_thread(target=[grab_everything, play_sonic, run_big_claw], value=values)

while not button.any():
    print('Proximity(cm): {}'.format(proximity.distance_centimeters))
    print('Claw(\u00B0): {}'.format(claw.degrees))

values[0].value = 1
procs[0].join()
procs[1].join()

wheels.off()
claw.off()
