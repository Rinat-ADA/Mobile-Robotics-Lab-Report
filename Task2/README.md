
# Task 2 - Line Follower Robot

## About the Task

In this task, we used an EV3 robot to follow a black line on the floor. The main goal was to make the robot follow the track without losing the line, especially at sharp turns.

## Robot Setup

- Left motor: Port B
- Right motor: Port C
- Color sensor: Port S1

## How the Code Works

We used a PD controller to control the movement of the robot. The color sensor measures the reflected light from the floor.

We set the black value to 6, the white value to 55, and the target value to 30.

The robot compares the sensor reading with the target value and adjusts the speed of the left and right motors.

We used Kp = 4.0 and Kd = 0.8 to calculate the correction.

We also added a special movement for sharp left turns. When the correction becomes smaller than -55, the left motor moves backward and the right motor moves forward.

Another part of the code helps the robot find the line again if it loses it. The robot first searches in the last turning direction. If it cannot find the line, it searches in the opposite direction.

## Main Parameters

- Normal speed: 65 deg/s
- Kp: 4.0
- Kd: 0.8
- Target reflection: 30
- Line lost threshold: 43
- Line found threshold: 28

## Files

- `main.py` - Python code for the line follower.
