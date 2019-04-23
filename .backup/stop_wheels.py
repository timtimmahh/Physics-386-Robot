from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank

wheels = MoveTank(OUTPUT_B, OUTPUT_A)
wheels.off(brake=True)
