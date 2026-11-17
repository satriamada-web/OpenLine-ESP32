"""OpenLine ESP32 - Webots prototype controller.

Three downward-facing LightSensor devices approximate the three TCRT5000
reflectance modules. This validates robot motion/control logic; it does not
emulate ESP32 silicon or the electrical L298N driver.
"""
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

sensor_names = ["left sensor", "center sensor", "right sensor"]
sensors = [robot.getDevice(name) for name in sensor_names]
for sensor in sensors:
    sensor.enable(timestep)

MAX_SPEED = 8.0
BASE_SPEED = 5.0
KP = 2.4
# LightSensor values depend on the rendered scene and device calibration.
# Start with a relative threshold and inspect printed readings if needed.
THRESHOLD = 0.5

def clamp(value, low, high):
    return max(low, min(high, value))

while robot.step(timestep) != -1:
    readings = [sensor.getValue() for sensor in sensors]

    # For the initial prototype, determine which sensor sees the darker line.
    # If the sensor scale is inverted or differs on your Webots version,
    # we will calibrate this threshold from the live readings.
    line_detected = [value < THRESHOLD for value in readings]

    weights = [1.0, 0.0, -1.0]  # left, center, right
    active = [weights[i] for i in range(3) if line_detected[i]]

    if active:
        error = sum(active) / len(active)
        correction = KP * error
        left_speed = clamp(BASE_SPEED - correction, -MAX_SPEED, MAX_SPEED)
        right_speed = clamp(BASE_SPEED + correction, -MAX_SPEED, MAX_SPEED)
    else:
        # No sensor sees the line: stop safely until calibration is complete.
        left_speed = 0.0
        right_speed = 0.0

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
