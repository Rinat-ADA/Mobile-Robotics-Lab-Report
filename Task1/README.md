
# Task 1 - Square Movement

## About the Task

In this task, we programmed the EV3 robot to move in a square. The robot needs to move forward 50 cm, turn 90 degrees, and repeat this four times.

We used Python with Pybricks to control the motors.

## Robot Setup

For this task, we used two motors:
- Left motor: Port B
- Right motor: Port C

The wheel radius was set to 3 cm, and the distance between the wheels was set to 11 cm.

## How the Code Works

We created two functions in the code.

The first function, `drive_straight()`, calculates how much the motors need to rotate to move a certain distance.

The second function, `turn()`, makes the robot turn by moving the two wheels in opposite directions.

In the main part of the code, we repeated the same movement four times: move forward 50 cm and turn -90 degrees.

The motor speed was set to 300 degrees per second.

## Files

- `main.py` - The Python code used to control the robot.
