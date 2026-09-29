# Hand Gesture Controlled Robot

An engineering project reconstructed from the owner’s recollections and supplied reference material: hand tilt → analog accelerometer → Arduino → RF link → Arduino → dual DC motors.

**Status:** historical project documentation recovery, with newly written reference firmware. Original source code was lost. This reconstruction has not been tested on physical hardware. The supplied image is a motor-control reference diagram, not a photograph of the assembled robot.

```mermaid
flowchart LR
    Hand[Hand tilt] --> Sensor[Analog accelerometer]
    Sensor --> TX[Transmitter Arduino Uno]
    TX --> RF[RF wireless link]
    RF --> RX[Receiver Arduino Uno]
    RX --> Driver[L293D motor driver]
    Driver --> Motors[Left and right DC motors]
```

## What is recovered

The project owner confirms that tilting the hand controlled forward movement, reverse movement, and turns.

The reference diagram shows an Arduino Uno, an L293D, two motors, and a battery labeled 9 V. The sensor and wireless link are not shown. The proposed reconstruction uses two Unos, an ADXL335-compatible analog sensor, and a matched ASK/OOK radio pair. Exact original sensor/radio variants, frequency, wiring, software, project year, and individual contributions remain unconfirmed.

## Circuit diagrams

These original connection diagrams match the reconstructed firmware. Pin positions are symbolic; the L293D labels include physical DIP pin numbers. Radio models and supply requirements still need confirmation.

### Hand-controller transmitter

![Hand-controller transmitter wiring](assets/diagrams/01-transmitter.png)

### Robot receiver and motors

![Robot receiver and L293D motor wiring](assets/diagrams/02-receiver.png)

### Power and enable connections

![Robot supply bypass and enable pulldowns](assets/diagrams/03-power-and-enables.png)

[Download SVG diagrams and read the diagram guide](docs/diagrams.md). The supplied historical reference remains in the [evidence register](docs/evidence.md).

## Reference implementation

- Neutral calibration at transmitter startup; dominant-axis tilt selects forward, backward, left, or right.
- A neutral dead zone commands stop; diagonal ties also stop.
- Versioned command packets over RadioHead ASK at 2,000 bits/s.
- Receiver starts disabled and requires a stop packet before accepting movement after startup or link loss.
- A 500 ms command timeout disables motor outputs; invalid application packets stop and disarm the receiver.
- Enable pins are disabled before changing motor direction.

These are new implementation choices, not claims about the original firmware. This is a supervised educational prototype; the radio has no authentication or acknowledgement, and a disconnected analog sensor is not reliably detected.

## Build and explore

1. Read [hardware and wiring](docs/hardware.md) before connecting power.
2. Follow [setup and calibration](docs/setup.md) to install dependencies and upload both sketches.
3. Run the host logic checks with `sh tests/run.sh` (requires a C++11 compiler).
4. Follow the [bench validation plan](docs/validation.md), keeping wheels off the ground initially.

| Path | Contents |
| --- | --- |
| `firmware/transmitter/` | Hand-controller sketch |
| `firmware/receiver/` | Robot sketch |
| `libraries/GestureControl/` | Shared classifier, packet parser, and timeout logic |
| `docs/` | Evidence, wiring, setup, validation, portfolio notes |
| `assets/reference/` | Supplied motor-control reference diagram |
| `tests/` | Host logic regression tests |

## References and attribution

- [Analog Devices ADXL335](https://www.analog.com/en/products/adxl335.html): candidate analog accelerometer specifications.
- [Texas Instruments L293D](https://www.ti.com/product/L293D): driver specifications and datasheet.
- [RadioHead RH_ASK](https://www.airspayce.com/mikem/arduino/RadioHead/classRH__ASK.html): reference firmware radio API.
