"""Minimal Webots controller used to isolate Python startup."""
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

while robot.step(timestep) != -1:
    pass
