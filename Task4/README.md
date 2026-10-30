# Task 4 - Robot Arena

## About the Task

In this task, we programmed our EV3 robot to move inside an arena without crossing the black boundary lines or hitting other robots.

We used a color sensor to detect the black lines and an ultrasonic sensor to detect objects in front of the robot.

## Robot Setup

For this task, we used two motors and two sensors.

- Left motor: Port B
- Right motor: Port C
- Ultrasonic sensor: Port S1
- Color sensor: Port S3
- Wheel diameter: 55.5 mm
- Distance between wheels: 104 mm

## How the Code Works

We used three main behaviours to control the robot.

**1. Boundary Escape**

The color sensor checks the floor. If the reflection value is below 25, the robot detects the black boundary line. It moves backward 150 mm and then turns randomly between 110 and 170 degrees in either direction.

**2. Obstacle Avoidance**

The ultrasonic sensor measures the distance to objects in front of the robot. If an object is closer than 250 mm, the robot moves backward 100 mm and turns randomly between 90 and 140 degrees to avoid it.

**3. Random Wandering**

When there is no boundary or obstacle, the robot normally moves forward at 150 mm/s. Every 3 to 6 seconds, it makes a random turn to change its direction.

## Behaviour Priority

We used a priority system in the code:

1. Boundary escape
2. Obstacle avoidance
3. Random wandering

Boundary escape has the highest priority because we wanted the robot to stay inside the arena.

## Main Parameters

- Forward speed: 150 mm/s
- Safe distance: 250 mm
- Black threshold: 25
- Boundary reverse distance: 150 mm
- Obstacle reverse distance: 100 mm
- Game duration: 120 seconds
- Control loop delay: 20 ms

## Files

- `main.py` - Python code used to control the robot in the arena.