
#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Button
from pybricks.tools import wait, StopWatch
from math import pi

ev3 = EV3Brick()

# =====================================
# HARDWARE
# =====================================

left = Motor(Port.B)
right = Motor(Port.C)

sensor_l = ColorSensor(Port.S3)
sensor_r = ColorSensor(Port.S4)

WHEEL_DIAMETER = 55.5
AXLE_TRACK = 104

# =====================================
# CALIBRATION
# =====================================

BLACK = 9
WHITE = 48.5
TARGET = (BLACK + WHITE) / 2

MARKER_BLACK = 12

# =====================================
# SPEED AND PD CONTROL
# =====================================

BASE_SPEED = 115
MIN_SPEED = 35
MAX_SPEED = 170

KP = 2.0
KD = 0.6

TURN_SPEED = 75
LOOP_MS = 20

# =====================================
# JUNCTION SETTINGS
# =====================================

MARKER_MIN_MM = 32
JUNCTION_GAP_MM = 65

LOST_TIMEOUT_MS = 1800
MAX_RUN_MS = 120000

# Distance to move after marker
CLEAR_MARKER_MM = 22

# =====================================
# ROUTE
# S -> M -> N -> K -> G1
# =====================================

ROUTE = ["L", "R", "S"]

clock = StopWatch()

previous_error = 0


# =====================================
# BASIC FUNCTIONS
# =====================================

def stop():
    left.stop()
    right.stop()


def clamp(value, low, high):
    return max(low, min(high, value))


def user_stop():
    return Button.CENTER in ev3.buttons.pressed()


def distance_mm():
    average_angle = (
        left.angle() + right.angle()
    ) / 2

    return (
        average_angle * pi *
        WHEEL_DIAMETER / 360
    )


def both_dark():
    return (
        sensor_l.reflection() < MARKER_BLACK
        and
        sensor_r.reflection() < MARKER_BLACK
    )


def line_visible():
    l = sensor_l.reflection()
    r = sensor_r.reflection()

    return l < TARGET or r < TARGET


def normal_line():
    return line_visible() and not both_dark()


# =====================================
# PD LINE FOLLOWING
# =====================================

def follow_step():

    global previous_error

    l = sensor_l.reflection()
    r = sensor_r.reflection()

    error = l - r
    derivative = error - previous_error

    correction = (
        KP * error +
        KD * derivative
    )

    previous_error = error

    left_speed = clamp(
        BASE_SPEED + correction,
        MIN_SPEED,
        MAX_SPEED
    )

    right_speed = clamp(
        BASE_SPEED - correction,
        MIN_SPEED,
        MAX_SPEED
    )

    left.run(left_speed)
    right.run(right_speed)


# =====================================
# MOVEMENT
# =====================================

def move_straight(mm):

    motor_angle = (
        mm * 360 /
        (pi * WHEEL_DIAMETER)
    )

    left.run_angle(
        75, motor_angle, wait=False
    )

    right.run_angle(
        75, motor_angle, wait=True
    )

    stop()


def turn_angle(degrees):

    # Positive = left
    # Negative = right

    wheel_angle = (
        degrees * AXLE_TRACK /
        WHEEL_DIAMETER
    )

    left.run_angle(
        TURN_SPEED,
        -wheel_angle,
        wait=False
    )

    right.run_angle(
        TURN_SPEED,
        wheel_angle,
        wait=True
    )

    stop()


# =====================================
# LINE RECOVERY
# =====================================

def find_line():

    stop()

    # Small search movements
    search_angles = [
        15, -30, 45, -60, 30
    ]

    for angle in search_angles:

        if user_stop():
            stop()
            return False

        turn_angle(angle)

        # Confirm the line is visible
        if normal_line():
            wait(60)

            if normal_line():
                stop()
                return True

    stop()
    return False


# =====================================
# JUNCTION TURNING
# =====================================

def execute_turn(direction):

    stop()
    wait(100)

    # Move beyond detected marker
    move_straight(CLEAR_MARKER_MM)

    if direction == "L":
        turn_angle(90)

    elif direction == "R":
        turn_angle(-90)

    elif direction == "U":
        turn_angle(180)

    elif direction == "S":
        return True

    wait(100)

    if normal_line():
        return True

    # Search for the next line
    if find_line():
        return True

    print("Turn failed")
    return False


# =====================================
# MAIN NAVIGATION
# =====================================

def run_route():

    global previous_error

    ev3.screen.clear()
    ev3.screen.print("TASK 5")

    clock.reset()

    left.reset_angle(0)
    right.reset_angle(0)

    previous_error = 0

    junction_index = 0

    marker_start = None
    last_junction = -1000

    marker_armed = True
    lost_start = None

    ev3.speaker.beep()

    # Follow route through 3 junctions
    while junction_index < len(ROUTE):

        if user_stop():
            stop()
            print("User stopped")
            return

        if clock.time() > MAX_RUN_MS:
            stop()
            print("Navigation timeout")
            return

        follow_step()

        current_distance = distance_mm()
        dark = both_dark()

        # -----------------------------
        # JUNCTION DETECTION
        # -----------------------------

        if dark and marker_armed:

            if marker_start is None:
                marker_start = current_distance

            marker_length = abs(
                current_distance - marker_start
            )

            enough_gap = (
                current_distance - last_junction
                >= JUNCTION_GAP_MM
            )

            if (
                marker_length >= MARKER_MIN_MM
                and enough_gap
            ):

                stop()

                direction = ROUTE[junction_index]

                print(
                    "Junction",
                    junction_index + 1,
                    direction
                )

                ev3.speaker.beep()

                last_junction = current_distance
                marker_armed = False

                success = execute_turn(
                    direction
                )

                if not success:
                    stop()
                    print("Route failed")
                    return

                junction_index += 1

                marker_start = None
                previous_error = 0
                lost_start = None

                wait(200)
                continue

        elif not dark:

            marker_start = None

            # Rearm after leaving marker
            if (
                current_distance - last_junction
                >= JUNCTION_GAP_MM
            ):
                marker_armed = True

        # -----------------------------
        # LOST LINE DETECTION
        # -----------------------------

        if not line_visible():

            if lost_start is None:
                lost_start = clock.time()

            elif (
                clock.time() - lost_start
                > LOST_TIMEOUT_MS
            ):

                stop()
                print("Line lost")

                if not find_line():
                    print("Cannot recover")
                    return

                lost_start = None
                previous_error = 0

        else:
            lost_start = None

        wait(LOOP_MS)

    # =================================
    # FINAL SEGMENT TO G1
    # =================================

    print("Final segment")

    final_start = clock.time()
    lost_since = None
    possible_end = False

    while (
        clock.time() - final_start
        < 12000
    ):

        if user_stop():
            break

        follow_step()

        if not line_visible():

            if lost_since is None:
                lost_since = clock.time()

            elif (
                clock.time() - lost_since
                >= 300
            ):

                stop()
                possible_end = True
                print("Possible line end")
                break

        else:
            lost_since = None

        wait(LOOP_MS)

    stop()

    if possible_end:
        print("Check G1 position")
    else:
        print("Final segment stopped")

    print("Time:", clock.time(), "ms")

    ev3.speaker.beep()
    wait(150)
    ev3.speaker.beep()


# =====================================
# START PROGRAM
# =====================================

try:
    run_route()

except Exception as error:

    stop()
    print("ERROR:", error)
    ev3.speaker.beep()

finally:
    stop()
