# Circuit diagram guide

| Setup | Editable vector | PNG image |
| --- | --- | --- |
| Hand-controller transmitter | [SVG](../assets/diagrams/01-transmitter.svg) | [PNG](../assets/diagrams/01-transmitter.png) |
| Robot receiver and motors | [SVG](../assets/diagrams/02-receiver.svg) | [PNG](../assets/diagrams/02-receiver.png) |
| Robot power and enable details | [SVG](../assets/diagrams/03-power-and-enables.svg) | [PNG](../assets/diagrams/03-power-and-enables.png) |

These are newly drawn functional connection diagrams for this repository’s firmware, not recovered original schematics or breadboard placement instructions. Read sheets 02 and 03 together. Identical net names on those sheets are electrically connected. TX and RX grounds belong to separate wireless devices and are not wired together.

The supplied example establishes the desired diagram style. Its Bluetooth module and wiring are not incorporated into this RF reconstruction. No third-party watermark or artwork has been copied into the generated diagrams.

Radio module models remain unspecified: V_RF_TX and V_RF_RX mean module-rated supply rails, not fixed voltages. Confirm module pin order, supply and data-level compatibility before assembly. The ADXL335-compatible sensor is also a provisional component choice. Follow the [hardware guide](hardware.md) for the complete map and component constraints.

Pin numbers were checked against the [TI L293D datasheet](https://www.ti.com/lit/ds/symlink/l293.pdf); signal assignments match `firmware/transmitter/transmitter.ino` and `firmware/receiver/receiver.ino`. The circuit has not been validated on hardware.

Regenerate with `python3 scripts/draw_circuits.py` from an environment with Pillow. The renderer currently uses the macOS Arial font path; adjust that path on other systems. SVGs are independently editable in a vector editor.
