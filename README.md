# OpenLine ESP32

**Open-source Bluetooth-controlled line follower robot based on ESP32, with a Webots simulation environment.**

> Status: early development. The repository structure and project documentation are being prepared. Hardware, firmware, and simulation models will be added and tested incrementally.

## Project goals

- Build an affordable 2-wheel differential-drive line follower.
- Use an ESP32 DevKit with Bluetooth control from an Android phone.
- Detect a track using three reflectance sensors: left, center, and right.
- Provide a reproducible Webots simulation of the robot following a virtual line.
- Publish hardware documentation, firmware, simulation assets, and test procedures so others can learn, build, and contribute.

## Planned hardware

| Part | Planned quantity | Notes |
|---|---:|---|
| ESP32 DevKit V1 | 1 | Confirm the exact ESP32 module before choosing Bluetooth features |
| TCRT5000 reflectance modules | 3 | Left, center, right; calibrate each module's output |
| L298N motor driver | 1 | Check motor current and driver voltage drop |
| DC gearbox motor | 2 | Select after confirming motor voltage and current |
| Drive wheel | 2 | Match the motor shaft |
| 360-degree caster | 1 | Passive support wheel |
| 18650 cells | 4 | Battery series/parallel arrangement is **not decided** |
| Chassis | 1 | Acrylic or another suitable material |
| Switch, wiring, battery holder, regulator/protection | As required | Final selection depends on electrical design |

**Power safety:** Do not connect the battery pack until cell specifications, pack configuration, protection/BMS, motor ratings, and regulator requirements have been checked. Never assume four 18650 cells should be wired in series or parallel.

## System overview

1. Three reflectance sensors measure the track beneath the front of the robot.
2. The ESP32 reads the sensor states and calculates motor commands.
3. The L298N drives the left and right motors.
4. Bluetooth provides remote enable/disable and speed setting.
5. The robot stops when disabled and should enter a safe stop state if the Bluetooth connection is lost.

The initial sensor-based controller will be simple and deterministic. More advanced PID control and calibration can be added after basic tracking works.

## Simulation

The planned simulator is **Webots**. It will represent the chassis, wheels, motors, three line sensors, and a black/white track in a 3D world.

Webots simulates robot behavior; it does **not** emulate the ESP32 silicon or reproduce the exact electrical behavior of the L298N. The simulation controller will first validate movement and line-following logic. That logic will then be ported to the ESP32 firmware and tested on real hardware.

## Repository layout

```text
OpenLine-ESP32/
├── controllers/       # Webots robot controllers
├── docs/              # Build guide, architecture, and test notes
├── firmware/          # ESP32 firmware (PlatformIO)
├── hardware/          # Wiring, BOM, and mechanical design files
├── protos/            # Reusable Webots robot PROTO models
├── worlds/            # Webots arenas and track worlds
└── README.md
```

## Development roadmap

- [ ] Confirm exact ESP32 board and component specifications
- [ ] Complete the electrical power design safely
- [ ] Create the first Webots arena and robot model
- [ ] Implement and test virtual three-sensor line following
- [ ] Add ESP32 firmware and Bluetooth commands
- [ ] Assemble the physical robot and validate each subsystem
- [ ] Document calibration, testing, and troubleshooting
- [ ] Publish a first tagged release

## Initial Bluetooth command plan

The command protocol is not finalized. The proposed first commands are:

- `ON` — enable the motors
- `OFF` — stop the motors
- `SPEED:<value>` — set a bounded speed value

The final protocol and supported Bluetooth mode will be documented after confirming the exact ESP32 variant and testing with an Android device. A safe stop on disconnect is required.

## Development environment

- Windows 11
- Webots (3D simulation)
- PlatformIO with the Arduino framework or ESP-IDF (firmware decision to be documented)
- Git and GitHub

## Contributing

Contributions are welcome after the initial architecture is established. Please open an issue to discuss major changes, especially changes to the electrical design or battery configuration.

## License

Licensing will be added when the first hardware and software files are ready. The intended approach is to license software and hardware documentation/design files separately.


## Run the first Webots simulation on Windows

The first prototype contains:
- `worlds/openline_arena.wbt`: white arena, straight black track, differential-drive robot.
- `controllers/line_follower/line_follower.py`: controller with three downward 1x1 cameras used as virtual reflectance sensors.

### Get the project

Clone the public repository:

```bash
git clone https://github.com/satriamada-web/OpenLine-ESP32.git
```

Or download the repository as a ZIP from GitHub and extract it.

### Open in Webots

1. Start Webots.
2. Select **File → Open World**.
3. Open `OpenLine-ESP32/worlds/openline_arena.wbt`.
4. Press the **Run** button.

The first run is a prototype and requires validation in the installed Webots version. If the robot stops or the line is not detected, inspect the controller console and calibrate `BLACK_THRESHOLD` in `controllers/line_follower/line_follower.py`.

### Important simulation boundary

The three virtual cameras sample surface brightness to approximate three TCRT5000 reflectance modules. Webots simulates robot motion and sensor behavior; it does not emulate the ESP32 chip, Bluetooth radio, or the electrical characteristics of the L298N. Those are implemented and tested separately on the physical robot.


## Circular line-follower simulation (Webots R2025a)

The active prototype is `worlds/openline_integrated_test.wbt`:
- White floor with a **0.64 m diameter** circular black track.
- Blue chassis, two independently driven wheels, and a passive rear caster.
- Three downward-facing virtual reflectance sensors (left, center, right), representing the planned three TCRT5000 modules.
- Two velocity-controlled wheel motors, representing the two DC motors through the planned L298N driver.
- A weighted-centroid PD-style controller with a slow line-search behavior when all sensors lose the track.

Run it from PowerShell after pulling the latest changes:

```powershell
git pull
& "$env:LOCALAPPDATA\Programs\Webots\msys64\mingw64\bin\webots.exe" --stdout --stderr "$env:USERPROFILE\OpenLine-ESP32\worlds\openline_integrated_test.wbt"
```

### Simulation-to-hardware mapping

| Planned physical module | Webots representation |
|---|---|
| ESP32 DevKit V1 | Webots Python controller (control logic only; not ESP32 emulation) |
| 3 × TCRT5000 modules | 3 downward 1×1 cameras sampling black/white brightness |
| L298N | Two velocity-controlled RotationalMotor devices; driver electronics are not electrically simulated |
| 2 × DC gearbox motors | Left and right wheel joints |
| 2 drive wheels | Cylinders with physical collision and mass |
| 360-degree caster | Rear sphere visual and collision support |
| Battery pack | Not electrically modeled; voltage, current, and battery wiring remain outside Webots |

The repository currently does not define final ESP32 GPIO assignments, motor voltage/current, sensor module output mode, or battery wiring. Therefore this simulation maps the confirmed component roles, not unconfirmed electrical pin settings. Those values must be added after the exact module variants and wiring are confirmed.

### Controller tuning

Tune `BASE_SPEED`, `MAX_SPEED`, `KP`, and `KD` in `controllers/line_follower/line_follower.py` only after the robot stays on the floor and the three sensor readings distinguish black from white. Camera brightness is a simulation approximation; real TCRT5000 modules require calibration against their actual analog/digital outputs.
