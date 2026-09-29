# Setup and calibration

These instructions target two Arduino Unos. Verify components against the hardware document first. Original software/library choices are unknown.

1. Install Arduino IDE and the Arduino AVR Boards package for the Uno.
2. Download RadioHead from its [official project page](https://www.airspayce.com/mikem/arduino/RadioHead/index.html), and add its ZIP using the IDE library installer. Record the version used during actual compilation.
3. Copy `libraries/GestureControl` to the `libraries` folder inside your Arduino sketchbook, then restart the IDE if needed.
4. Open `firmware/transmitter/transmitter.ino`. Select Arduino Uno and the hand-controller serial port, verify, then upload.
5. Open `firmware/receiver/receiver.ino`. Select the robot's Uno port, verify, then upload with motor power disconnected.
6. Follow the validation plan before a floor demonstration.

The transmitter prints a calibration message at 9600 baud, waits two seconds, then averages 100 samples over approximately one second. Hold the sensor flat and still throughout. Reset it to recalibrate. Debug rows are `x deviation,y deviation,command number` in raw ADC counts.

Default mapping: positive Y → forward (1), negative Y → backward (2), negative X → left (3), positive X → right (4), neutral → stop (0). Turning commands pivot by driving wheels in opposite directions. Physical hand directions depend on sensor mounting: adjust `X_SIGN` and `Y_SIGN`, or exchange axes if needed. If a motor rotates backwards, power off and swap its two leads.

The threshold is 45 ADC counts from startup neutral. This is a starting value, not a measured angle or recovered calibration. Tune it after observing neutral noise and deliberate tilts. There is no filtering, hysteresis, or verified disconnected-sensor detection in this initial implementation.

After powering the receiver or losing the link, hold the hand neutral to arm it. Movement packets alone do not arm it. Calibration does not transmit packets, so a previously running receiver should time out while the controller resets.

For Arduino CLI users with AVR core and RadioHead installed:

```sh
arduino-cli compile --fqbn arduino:avr:uno --libraries ./libraries firmware/transmitter
arduino-cli compile --fqbn arduino:avr:uno --libraries ./libraries firmware/receiver
```

Host-only logic checks:

```sh
sh tests/run.sh
```

Host checks do not compile Arduino sketches or verify electrical behavior.
