from multiprocessing import Process

from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveSteering, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor
from ev3dev2.sound import Sound

from classes import Claw

button = Button()
wheels = MoveSteering(OUTPUT_A, OUTPUT_B)
claw = Claw()
gyro = GyroSensor(INPUT_1)
touch = TouchSensor(INPUT_3)
sound = Sound()

eyes = UltrasonicSensor(INPUT_4)
eyes_motor = MediumMotor(OUTPUT_C)


def scan_surroundings():
    while not button.any():
        eyes_motor.on_for_degrees(SpeedPercent(25), 180, block=True)
        eyes_motor.on_for_degrees(SpeedPercent(25), -180, block=True)
        print('Proximity distance {}'.format(eyes.distance_centimeters))


def grab_everything():
    # claw.on_for_rotations(SpeedPercent(100), 2, block=False)
    wheels.on(0, SpeedPercent(50))

    def on_wait():
        if touch.is_pressed:
            wheels.on_for_rotations(0, SpeedPercent(-50), 1, block=True)
            wheels.on_for_rotations(100, SpeedPercent(100), 1.5, block=True)
        else:
            wheels.on(0, SpeedPercent(50))

    while not button.any():
        if claw.grab_when_within(5.0, while_waiting=on_wait, cancel=lambda: button.any()):
            wheels.on_for_seconds(0, SpeedPercent(-100), 1, block=True)
            wheels.on_for_rotations(45, SpeedPercent(100), 0.5, block=True)
            wheels.on_for_rotations(0, SpeedPercent(85), 5, block=True)
            claw.open()
            wheels.on_for_rotations(0, SpeedPercent(-100), 1, block=True)
            wheels.on_for_degrees(-100, SpeedPercent(100), 360)


# sound.play_file("Sonic The Hedgehog-Green Hill Zone Theme.mp3")

proc = Process(target=grab_everything)
scanner = Process(target=scan_surroundings)
# play_song = Thread(target=sound.play_file, args=("Sonic The Hedgehog-Green Hill Zone Theme.mp3",))


proc.start()
scanner.start()
# play_song.start()

proc.join()
scanner.join()
# play_song_join()


wheels.off()
claw.release()
