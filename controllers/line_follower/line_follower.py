"""OpenLine ESP32: Webots prototype using three downward 1x1 cameras.

Each camera approximates one TCRT5000 reflectance sensor by sampling the
surface brightness beneath it. This is a behavioral simulation, not an
electrical/ESP32/L298N emulation.
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
BLACK_THRESHOLD = 100  # RGB brightness 0..255; calibrate after first run

def clamp(value, low, high):
    return max(low, min(high, value))

while robot.step(timestep) != -1:
    brightness = []
    for sensor in sensors:
        pixels = sensor.getImageArray()
        # A 1x1 camera returns one RGB(A) pixel.
        pixel = pixels[0][0]
        brightness.append((int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3.0)

    # Dark pixels indicate the black track.
    on_black = [value < BLACK_THRESHOLD for value in brightness]
    weights = [1.0, 0.0, -1.0]  # left, center, right

    active_weights = [weights[i] for i in range(3) if on_black[i]]
    if active_weights:
        error = sum(active_weights) / len(active_weights)
        correction = KP * error
        left_speed = clamp(BASE_SPEED - correction, -MAX_SPEED, MAX_SPEED)
        right_speed = clamp(BASE_SPEED + correction, -MAX_SPEED, MAX_SPEED)
    else:
        # Safe stop if the line is not detected; calibration comes next.
        left_speed = 0.0
        right_speed = 0.0

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
