
#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from random import randint

ev3 = EV3Brick()

# Motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Sensors
ultrasonic = UltrasonicSensor(Port.S1)
color = ColorSensor(Port.S3)

# Robot dimensions
robot = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=55.5,
    axle_track=104
)

# Parameters
SPEED = 150
TURN_SPEED = 120

SAFE_DISTANCE = 250
BLACK_THRESHOLD = 25
GAME_TIME = 120000

# Robot settings
robot.settings(
    straight_speed=150,
    straight_acceleration=300,
    turn_rate=120,
    turn_acceleration=200
)

# Timer
timer = StopWatch()

last_wander = 0
next_wander = randint(3000, 6000)

try:
    while timer.time() < GAME_TIME:

        distance = ultrasonic.distance()
        light = color.reflection()

        # Priority 1: Escape boundary
        if light < BLACK_THRESHOLD:

            robot.stop()
            robot.straight(-150)

            angle = randint(110, 170)
            direction = randint(0, 1)

            if direction == 0:
                angle = -angle

            robot.turn(angle)

            last_wander = timer.time()
            next_wander = randint(3000, 6000)

        # Priority 2: Avoid other robots
        elif distance < SAFE_DISTANCE:

            robot.stop()
            robot.straight(-100)

            angle = randint(90, 140)

            if randint(0, 1) == 0:
                angle = -angle

            robot.turn(angle)

            last_wander = timer.time()
            next_wander = randint(3000, 6000)

        # Priority 3: Random wandering
        elif timer.time() - last_wander > next_wander:

            angle = randint(-90, 90)

            robot.turn(angle)

            last_wander = timer.time()
            next_wander = randint(3000, 6000)

        # Normal forward movement
        else:
            robot.drive(SPEED, 0)

        wait(20)

finally:
    robot.stop()
    ev3.speaker.beep()
