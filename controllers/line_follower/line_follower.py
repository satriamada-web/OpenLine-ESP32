"""OpenLine ESP32 - Webots line follower prototype.

Three downward 1x1 cameras approximate three TCRT5000 reflectance modules.
Two RotationalMotor devices approximate the left/right DC motors driven by
an L298N. Webots validates robot mechanics and control logic; it does not
emulate ESP32 GPIO, Bluetooth, or L298N electrical behavior.
"""
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

sensor_names = ("left sensor", "center sensor", "right sensor")
sensors = [robot.getDevice(name) for name in sensor_names]
for sensor in sensors:
    sensor.enable(timestep)

# Initial tuning for the 0.64 m circular track. Adjust after observing the run.
MAX_SPEED = 7.0
BASE_SPEED = 3.4
KP = 2.2
KD = 0.12
WHITE_LEVEL = 220.0
BLACK_LEVEL = 35.0
LINE_PRESENT = 0.18
last_error = 0.0
last_time = 0.0

WEIGHTS = (1.0, 0.0, -1.0)  # left, center, right


def clamp(value, low, high):
    return max(low, min(high, value))


def read_line_strength(sensor):
    """Return 0 for white and approximately 1 for black."""
    image = sensor.getImageArray()
    if not image or not image[0]:
        return 0.0
    pixel = image[0][0]
    brightness = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3.0
    return clamp(
        (WHITE_LEVEL - brightness) / (WHITE_LEVEL - BLACK_LEVEL),
        0.0,
        1.0,
    )


while robot.step(timestep) != -1:
    now = robot.getTime()
    dt = max(now - last_time, timestep / 1000.0)
    last_time = now

    strengths = [read_line_strength(sensor) for sensor in sensors]
    total = sum(strengths)

    if total >= LINE_PRESENT:
        # Weighted line centroid gives a continuous steering error.
        error = sum(w * s for w, s in zip(WEIGHTS, strengths)) / total
        derivative = (error - last_error) / dt
        correction = KP * error + KD * derivative
        last_error = error

        left_speed = clamp(BASE_SPEED - correction, -MAX_SPEED, MAX_SPEED)
        right_speed = clamp(BASE_SPEED + correction, -MAX_SPEED, MAX_SPEED)
    else:
        # If the line is temporarily lost, turn toward its last known side.
        direction = 1.0 if last_error >= 0 else -1.0
        left_speed = 1.0 - 0.7 * direction
        right_speed = 1.0 + 0.7 * direction

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
