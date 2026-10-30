# Task 5 - Mapping and Navigation

## About the Task

In this task, I worked on making the EV3 robot follow a specific route using two color sensors. The robot had to follow the black line, detect junctions and choose the correct direction to reach the goal.

My planned route was:

**S → M → N → K → G1**

The robot needed to turn left at M, right at N and go straight at K.

## Robot Setup

I used two motors and two color sensors.

- Left motor: Port B
- Right motor: Port C
- Left color sensor: Port S3
- Right color sensor: Port S4
- Wheel diameter: 55.5 mm
- Distance between wheels: 104 mm

## How the Code Works

I used a PD controller to help the robot follow the black line. The color sensors measure the reflected light, and the program uses the difference between their readings to adjust the motor speeds.

I also added a junction detection system. When both sensors detect a dark surface for a certain distance, the robot considers it a junction and follows the next direction from the route list.

I stored the route instructions as `["L", "R", "S"]`.

I also included a line recovery function to help the robot find the line again if it loses it.

## Main Parameters

- Base speed: 115 deg/s
- Kp: 2.0
- Kd: 0.6
- Black reflection value: 9
- White reflection value: 48.5
- Marker threshold: 12
- Minimum marker length: 32 mm
- Junction gap: 65 mm
- Loop delay: 20 ms

## Problems Faced During the Lab

During the lab, I faced some problems with the navigation.

One of the main difficulties was detecting the junctions correctly. Sometimes the robot did not recognize the marker at the right moment, which affected its next movement.

Another problem was turning at the junctions. After making a turn, the robot did not always find the next line correctly.

I tried to improve the junction detection and added a line recovery function to help the robot return to the line.

However, these changes did not completely solve the navigation problems during the lab.

## Current Status

This is not the final working version of my code.

I completed the lab work and made changes to improve the robot's navigation, but the robot still had problems with junction detection and turning.

The current version includes these improvements, but it needs further adjustments before it can reliably complete the full route.

## Future Improvements

I would focus on improving the junction detection and adjusting the distance the robot moves before turning.

I would also test different PD controller values and improve the line recovery function.

## Files

- `main.py` - Python code for the mapping and navigation task. This is an updated version, but it is not the final working solution.