# Proposed reconstruction hardware

This is a new, internally consistent pin map. It differs from the supplied motor-control illustration, including the enable-pin controls. Follow this map when using the reconstructed firmware.

| Component | Quantity | Basis |
| --- | --- | --- |
| Arduino Uno | 2 | Uno visible; two-board architecture inferred |
| ADXL335-compatible analog breakout | 1 | Provisional choice from earlier reference material; not shown in current diagram |
| Matched ASK/OOK transmitter and receiver | 1 pair | Provisional choice from earlier reference material; not shown in current diagram |
| L293D DIP-16 | 1 | Label visible in schematic |
| DC gearmotor | 2 | Two motors depicted; ratings unconfirmed |
| Chassis, wheels and caster | 1 set | Required reconstruction choice |
| Suitable motor supply and regulated logic supplies | As needed | Original battery unknown |
| Breadboards, wires, bypass capacitors, enable pulldowns | As needed | Assembly requirements |

## Hand controller

| Device signal | Transmitter Uno |
| --- | --- |
| Sensor supply | 3.3 V for a confirmed compatible ADXL335 breakout |
| Sensor ground | GND |
| X output | A0 |
| Y output | A1 |
| Z output | Unconnected; unused in this reference code |
| RF TX data | D12 |
| RF TX supply / ground | Per module datasheet / GND |

Reserve D11 and D10 for RadioHead's unused RX/PTT signals; leave them unconnected. Check the breakout labels, orientation, and supply requirements. A bare ADXL335 operates at 1.8–3.6 V; do not assume a breakout accepts 5 V. The Uno ADC uses its default reference in this implementation.

## Robot receiver

| L293D physical DIP pin | Connection |
| --- | --- |
| 1 (1,2EN) | Uno D5; 10 kΩ pulldown to GND |
| 2 (1A) | Uno D2 |
| 3 (1Y) | Left motor terminal 1 |
| 4, 5, 12, 13 | Common robot GND |
| 6 (2Y) | Left motor terminal 2 |
| 7 (2A) | Uno D3 |
| 8 (VCC2) | Motor supply positive |
| 9 (3,4EN) | Uno D6; 10 kΩ pulldown to GND |
| 10 (3A) | Uno D4 |
| 11 (3Y) | Right motor terminal 1 |
| 14 (4Y) | Right motor terminal 2 |
| 15 (4A) | Uno D7 |
| 16 (VCC1) | Regulated 5 V logic supply |

RF receiver DATA → Uno D11. Supply it according to its own datasheet, with common robot GND. Reserve D12 and D10 as unconnected RadioHead TX/PTT outputs. Connect all required module supply/ground pins; do not infer their order from a different module's picture.

Use the IC notch to identify DIP pin 1. Add at least 0.1 µF bypass capacitors close to both L293D supply pins to GND, and appropriate bulk decoupling for the actual supply. Do not power motors from the Uno's 5 V pin. Join robot motor-supply negative, driver ground, and receiver Uno ground; the separate hand controller does not need a wire to the robot.

Choose supply and motors together: the L293D supports up to 600 mA per channel, subject to thermal limits, and has a substantial output voltage drop. Check motor stall current, not just free-running current. The reference image's 9 V battery label is not a recommendation for unknown motors. Verify supply polarity before powering.

The code uses full-speed digital enable signals. RadioHead uses Timer1 on the Uno; no Timer1 PWM or Servo dependency is introduced. Stop disables the bridges and lets motors coast; it is not active braking. Provide a reachable physical motor-power switch for bench work.

Sources: [ADXL335](https://www.analog.com/en/products/adxl335.html), [L293D datasheet](https://www.ti.com/lit/ds/symlink/l293.pdf), [RH_ASK](https://www.airspayce.com/mikem/arduino/RadioHead/classRH__ASK.html).
