# Hand Gesture Controlled Robot

An engineering project reconstructed from five surviving reference snapshots: hand tilt → analog accelerometer → Arduino → RF link → Arduino → dual DC motors.

**Status:** historical project documentation recovery, with newly written reference firmware. Original source code was lost. This reconstruction has not been tested on physical hardware. The snapshots show reference diagrams and presentation material, not a photograph of the assembled robot.

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

Arduino Uno boards, RF transmitter/receiver diagrams, an analog accelerometer breakout, and an L293D motor-driver schematic appear in the supplied images. The proposed reconstruction uses two Unos, an ADXL335-compatible analog sensor, and a matched ASK/OOK radio pair. Exact original sensor/radio variants, frequency, wiring, software, project year, and individual contributions remain unconfirmed.

See the [evidence register](docs/evidence.md) for the five images and their limitations.

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
| `assets/reference/` | Unmodified supplied photographs |
| `tests/` | Host logic regression tests |

## Portfolio context

The project can demonstrate sensor interfacing, embedded programming, wireless communication, and motor control once personal contributions are confirmed. No range, accuracy, latency, payload, or reliability results are claimed. Use [portfolio notes](docs/portfolio.md) to record the original work and distinguish it from this reconstruction.

## References and attribution

- [Analog Devices ADXL335](https://www.analog.com/en/products/adxl335.html): candidate analog accelerometer specifications.
- [Texas Instruments L293D](https://www.ti.com/product/L293D): driver specifications and datasheet.
- [RadioHead RH_ASK](https://www.airspayce.com/mikem/arduino/RadioHead/classRH__ASK.html): reference firmware radio API.

Supplied photos contain third-party diagrams, including visible Fritzing and microcontroller-project.com markings. They are retained as historical reference material; authorship of those diagrams is not claimed. No blanket license is applied to these images or this repository pending ownership review.
