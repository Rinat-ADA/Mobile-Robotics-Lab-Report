
# Task 3 - Robot Distance Control

## About the Task

In this task, we used an ultrasonic sensor to control the distance between the EV3 robot and an object in front of it.

Our goal was to keep the robot approximately 20 cm away from the object.

## Robot Setup

We used two motors and one ultrasonic sensor.

- Left motor: Port B
- Right motor: Port C
- Ultrasonic sensor: Port S1
- Wheel diameter: 55.5 mm
- Distance between wheels: 104 mm

## How the Code Works

We used a PD controller to control the forward and backward movement of the robot.

The ultrasonic sensor measures the distance to the object. The program compares this distance with our target of 200 mm.

If the object is farther than 200 mm, the robot moves forward. If the object is closer than 200 mm, the robot moves backward.

We used Kp = 2.0 and Kd = 0.3 for the controller.

We also added a dead band of 10 mm to prevent the robot from moving too much when it is already close to the target distance.

The derivative value is filtered to reduce sudden changes caused by sensor readings.

The maximum speed is limited to 150 mm/s.

## Main Parameters

- Target distance: 200 mm
- Kp: 2.0
- Kd: 0.3
- Maximum speed: 150 mm/s
- Dead band: 10 mm
- Control loop: 50 ms
- Derivative filter alpha: 0.3

## Files

- `main.py` - Python code for distance control.
