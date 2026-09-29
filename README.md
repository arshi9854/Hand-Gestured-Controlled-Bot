# Hand Gesture Controlled Robot

An engineering project: hand tilt → analog accelerometer → Arduino → RF link → Arduino → dual DC motors.

![Complete hand controller and robot connection](assets/diagrams/04-whole-system.png)

## System architecture

The hand controller and robot are separate devices. The wireless link carries direction commands; each device has its own power source.

```mermaid
flowchart LR
    subgraph HandController["Hand controller"]
        Hand["Hand tilt"] --> Sensor["Analog accelerometer"]
        Sensor -->|"X to A0; Y to A1"| TXUno["Transmitter Uno"]
        TXUno -->|"D12: encoded command"| TXRadio["RF transmitter"]
    end
    TXRadio -. "ASK/OOK wireless link" .-> RXRadio
    subgraph Robot["Robot"]
        RXRadio["RF receiver"] -->|"DATA to D11"| RXUno["Receiver Uno"]
        RXUno -->|"Direction and enable signals"| Driver["L293D motor driver"]
        Driver --> LeftMotor["Left DC motor"]
        Driver --> RightMotor["Right DC motor"]
    end
```

## Gestures and operation

![Forward, reverse, left, right, and neutral gesture guide](assets/diagrams/05-gesture-map.png)

The controller reads hand tilt and sends a direction command over RF. The robot receives that command and drives its two motors through the L293D. Neutral stops the motors; the reconstructed firmware also stops and disarms after communication loss.

[Explore the control flow and operating snapshots](docs/system-overview.md). These are newly drawn illustrations of the reconstructed design; actual hardware testing remains pending.


## What is covered

The reference diagram shows an Arduino Uno, an L293D, two motors, and a battery labeled 9 V. The sensor and wireless link are not shown. The proposed reconstruction uses two Unos, an ADXL335-compatible analog sensor, and a matched ASK/OOK radio pair. Exact original sensor/radio variants, frequency, wiring, software, project year, and individual contributions remain unconfirmed.

## How the firmware works

These diagrams describe the reconstructed code in this repository. Gesture thresholds, arming, and timeout behavior are implementation choices that still require hardware validation.

### 1. Startup and gesture classification

Calibration runs once at transmitter startup. After that, every cycle selects one command. `absX` and `absY` are the absolute deviations from the calibrated neutral readings, after applying the configured axis signs.

```mermaid
flowchart TD
    Boot["Transmitter power on"] --> Init{"Radio initialization succeeds?"}
    Init -->|"No"| Halt["Print error and halt"]
    Init -->|"Yes"| Cal["Wait 2 seconds; hold hand flat"]
    Cal --> Average["Average 100 X/Y samples over about 1 second"]
    Average --> Read["Read A0 and A1; subtract neutral; apply axis signs"]
    Read --> Neutral{"Both absolute deviations at most 45 counts?"}
    Neutral -->|"Yes"| Stop["STOP: command 0"]
    Neutral -->|"No"| Tie{"absX equals absY?"}
    Tie -->|"Yes"| Stop
    Tie -->|"No"| Axis{"absY greater than absX?"}
    Axis -->|"Yes"| YSign{"Y positive?"}
    Axis -->|"No"| XSign{"X positive?"}
    YSign -->|"Yes"| Forward["FORWARD: command 1"]
    YSign -->|"No"| Reverse["REVERSE: command 2"]
    XSign -->|"Yes"| Right["RIGHT: command 4"]
    XSign -->|"No"| Left["LEFT: command 3"]
    Stop --> Send["Send command packet; wait for transmission"]
    Forward --> Send
    Reverse --> Send
    Right --> Send
    Left --> Send
    Send --> Pause["Wait 50 ms"]
    Pause --> Read
```

The threshold is in raw ADC counts, not degrees. Total transmission-cycle time includes packet airtime and processing as well as the 50 ms delay.

### 2. Wireless command exchange

The application payload has three bytes: `G`, protocol version `1`, and command `0`–`4`. RadioHead adds framing and CRC. This diagram shows a successful arming and driving sequence; the link sends no acknowledgements.

```mermaid
sequenceDiagram
    actor Hand as Hand movement
    participant TX as Transmitter Uno
    participant RF as RF link
    participant RX as Receiver Uno
    participant Motors as L293D and motors
    Note over TX,RX: Receiver starts disarmed; motor outputs disabled
    Hand->>TX: Hold neutral after calibration
    TX->>RF: G, 1, STOP
    RF->>RX: Deliver CRC-valid frame
    RX->>RX: Validate payload and arm
    Note over RX,Motors: Motors remain off
    loop While receiving a deliberate tilt
        Hand->>TX: Tilt in a direction
        TX->>TX: Read and classify X/Y
        TX->>RF: G, 1, direction command
        RF->>RX: Deliver frame
        RX->>RX: Validate and refresh accepted-packet time
        opt Motor command changed
            RX->>Motors: Disable bridges; set direction; enable
        end
    end
    Hand->>TX: Return to neutral
    TX->>RF: G, 1, STOP
    RF->>RX: Deliver frame
    RX->>Motors: Disable both bridges; coast
    Note over TX,RX: If accepted packets stop for 500 ms, receiver disarms
```

### 3. Receiver states and recovery

An **armed** receiver may accept movement commands. A **disarmed** receiver requires a valid STOP packet first. Invalid application payloads disarm immediately; a radio CRC failure is dropped and does not refresh the timeout.

```mermaid
stateDiagram-v2
    state "Disarmed: outputs disabled" as Disarmed
    state "Armed: stopped" as Ready
    state "Armed: moving" as Moving
    [*] --> Disarmed
    Disarmed --> Disarmed: Movement packet ignored
    Disarmed --> Ready: Valid STOP packet
    Ready --> Ready: Valid STOP refreshes timeout
    Ready --> Moving: Valid direction packet
    Moving --> Moving: Valid direction refreshes timeout
    Moving --> Ready: Valid STOP packet
    Ready --> Disarmed: No accepted packet for 500 ms
    Moving --> Disarmed: No accepted packet for 500 ms
    Ready --> Disarmed: Invalid application payload
    Moving --> Disarmed: Invalid application payload
    Disarmed --> Disarmed: Invalid payload remains disarmed
```

Timeouts are checked by the firmware loop. Disabling the bridges allows coasting; it does not guarantee the wheels physically stop within 500 ms. A receiver radio-initialization failure leaves the outputs disabled and halts the sketch.

### 4. Direction commands and wheel motion

Wheel directions are viewed from above with the robot front at the top. Verify motor polarity during the raised-wheel test. The driver disables both enables before a command change; a new movement command adds a 20 ms disabled interval before energizing the outputs.

```mermaid
flowchart LR
    Command["Accepted command while armed"] --> F["1: FORWARD"]
    Command --> B["2: REVERSE"]
    Command --> L["3: LEFT"]
    Command --> R["4: RIGHT"]
    Command --> S["0: STOP"]
    F --> FF["Left forward + right forward"]
    B --> BB["Left reverse + right reverse"]
    L --> LF["Left reverse + right forward"]
    R --> RF["Left forward + right reverse"]
    S --> Off["D5 and D6 LOW: both bridges disabled"]
    LF --> CCW["Pivot counterclockwise"]
    RF --> CW["Pivot clockwise"]
```

### 5. Power and ground relationships

This is a power-distribution overview, not a physical pin-layout drawing. Use the circuit sheets below for connections, bypass capacitors, and enable pulldowns. Radio supplies and data-level compatibility depend on the actual modules.

```mermaid
flowchart TB
    subgraph HandPower["Hand-controller power domain"]
        TXPower["USB power"] --> TXBoard["Transmitter Uno"]
        TXBoard -->|"3.3 V"| Accel["Compatible accelerometer breakout"]
        TXSupply["Module-rated RF supply"] --> TXModule["RF transmitter"]
        TXGround["GND_TX: Uno, sensor, radio and supply negative"]
        TXBoard --- TXGround
        Accel --- TXGround
        TXModule --- TXGround
        TXSupply --- TXGround
    end
    subgraph RobotPower["Robot power domain"]
        RXPower["USB power"] --> RXBoard["Receiver Uno"]
        RXBoard -->|"5 V logic only, within power budget"| Logic["L293D VCC1: pin 16"]
        Battery["Motor supply matched to motors and driver"] --> Switch["Motor-power switch"]
        Switch --> MotorRail["L293D VCC2: pin 8"]
        RXSupply["Module-rated RF supply"] --> RXModule["RF receiver"]
        RXGround["GND_RX: Uno, radio, driver grounds and supply negatives"]
        RXBoard --- RXGround
        RXModule --- RXGround
        RXSupply --- RXGround
        Battery --- RXGround
        DriverGround["L293D pins 4, 5, 12, 13"] --- RXGround
    end
```

GND_TX and GND_RX are not wired together. The motor supply does not connect to the Uno 5 V rail. A module-rated RF supply may share a compatible logic rail only after its requirements and the available current are confirmed.

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
| `assets/diagrams/` | Seven illustrated PNG/SVG diagram pairs |
| `tests/` | Host logic regression tests |

## References and attribution

- [Analog Devices ADXL335](https://www.analog.com/en/products/adxl335.html): candidate analog accelerometer specifications.
- [Texas Instruments L293D](https://www.ti.com/product/L293D): driver specifications and datasheet.
- [RadioHead RH_ASK](https://www.airspayce.com/mikem/arduino/RadioHead/classRH__ASK.html): reference firmware radio API.
