# Open-source references used for the Webots prototype

This project uses public line-follower projects as engineering references. The OpenLine implementation is adapted to its own planned parts list; source files are not copied wholesale.

## 1. Webots line-follower architecture

- Project: https://github.com/MshRoor/Line-Follower-Robot
- License shown by the repository: Apache-2.0
- Relevant idea: a Webots robot with line sensors and feedback-based steering.
- OpenLine adaptation: a two-wheel differential-drive chassis with three virtual reflectance sensors and a weighted-centroid PD-style controller.

The Apache-2.0 repository is a reference for the general Webots line-following approach. No source code from it is included in this implementation.

## 2. Two-wheel, caster, three-sensor Webots arrangement

- Project: https://github.com/rrishabh23/Webots_LFR
- Relevant idea described in its README: two motor-driven wheels, one caster wheel, and three IR distance sensors, with controller logic based on sensor readings.
- OpenLine adaptation: the same broad mechanical arrangement is represented with two wheel joints, a passive rear caster, and three downward-facing cameras.

This repository is used only as a design reference. Its license was not confirmed during this review, so none of its code or assets are copied.

## 3. ESP32 and reflectance-sensor firmware reference

- Project: https://github.com/FCsab/line-follower-robot
- Relevant idea: an ESP32 line follower using a reflectance sensor array, motor driver, weighted sensor readings, bounded motor speeds, and line-loss handling.
- Hardware difference: that project specifies a TB6612FNG and a five-channel TCRT5000 array. OpenLine's planned hardware specifies an L298N and three TCRT5000 modules, so its pin map and driver code are not reused.

## OpenLine hardware-to-simulation boundary

| OpenLine planned part | Webots representation | What is not simulated |
|---|---|---|
| ESP32 DevKit V1 | Python controller | ESP32 silicon, GPIO timing, Bluetooth radio |
| 3 × TCRT5000 | 3 downward 1×1 cameras | IR emitter/phototransistor electronics and comparator thresholds |
| L298N | Two velocity-controlled RotationalMotor devices | H-bridge voltage drop, current limits, heating, PWM electrical behavior |
| 2 DC gearbox motors | Two wheel joints | Exact motor torque-speed curve until motor model data is supplied |
| 2 wheels | Cylinders with collision and mass | Exact tire tread and rubber friction |
| Rear caster | Passive sphere collision shape | Real caster swivel mechanics |
| Battery pack | Not modeled | Cell voltage, BMS, wiring, current draw |

## Important configuration still required

The repository does not yet define confirmed ESP32 GPIO pins, exact TCRT5000 module variants/output modes, motor rated voltage/current/RPM, L298N wiring, or battery pack topology. Do not infer or wire those values from this simulation. Record the exact physical modules and wiring before adding an electrical pin map or final ESP32 firmware.
