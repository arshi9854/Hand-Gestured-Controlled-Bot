# Validation record and bench plan

## Current evidence

- Host classifier/parser/watchdog checks: passed on 2026-09-29 using `sh tests/run.sh` with the local C++ compiler. Covers direction mapping, dead zone, malformed packets, startup/reconnect arming, timeout boundary, and clock rollover.
- Arduino sketch compilation: not yet verified; Arduino CLI is not installed in the reconstruction environment.
- Physical wiring, motor direction, RF compatibility, and operation: not tested.
- Original project's range, latency, accuracy, runtime, and results: unknown.

## Bench procedure

| Check | Procedure | Expected behavior | Result |
| --- | --- | --- | --- |
| Power inspection | Check chip orientation, supplies, grounds and enable pulldowns with motor power off | Matches confirmed component datasheets | Pending |
| Build | Compile both sketches for Uno; record IDE/core/RadioHead versions | No build errors | Pending |
| Neutral calibration | Observe serial values with controller flat | Stable values inside dead zone | Pending |
| Startup interlock | Start receiver while transmitter commands motion | Motor enables stay low until stop received | Pending |
| Direction mapping | Lift wheels, arm at neutral, test four tilts | Correct wheel direction for each command | Pending |
| Neutral stop | Return hand to neutral | Both enables low; wheels coast | Pending |
| Link loss | Command motion, then power off transmitter | Enables low about 500 ms after last valid packet, plus loop scheduling | Pending |
| Reconnect | Restore transmitter while tilted | Remains stopped until neutral packet | Pending |
| Motor load | Measure current and driver temperature with suitable supply | Within motor/driver thermal and current limits | Pending |
| Controlled demo | Supervised clear area; reachable motor-power switch | Repeatable directions and stop | Pending |

Record actual observations, supply voltage, motor model, radio module/frequency, library versions, measured stopping behavior, and failures. Radio CRC rejects damaged frames, but interference can still cause timeouts. Application magic/version fields do not authenticate a sender. A stuck sensor, valid repeated movement packet, or software hang is outside the timeout's protection. No real-time guarantee or autonomous obstacle detection is claimed.
