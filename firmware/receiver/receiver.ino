// Reconstructed reference firmware; not recovered original code.
#include <SPI.h>
#include <RH_ASK.h>
#include <GestureControl.h>
RH_ASK radio(2000, 11, 12, 10);
gesture::Receiver controller;
const uint8_t EN_L = 5, EN_R = 6, L1 = 2, L2 = 3, R1 = 4, R2 = 7;
gesture::Command applied = gesture::Stop;
void drive(gesture::Command command) {
  digitalWrite(EN_L, LOW); digitalWrite(EN_R, LOW);
  digitalWrite(L1, LOW); digitalWrite(L2, LOW);
  digitalWrite(R1, LOW); digitalWrite(R2, LOW);
  if (command == gesture::Stop) return;
  // Brief disabled interval before energizing a new direction; tune for actual mechanics.
  delay(20);
  bool leftForward = command == gesture::Forward || command == gesture::Right;
  bool rightForward = command == gesture::Forward || command == gesture::Left;
  digitalWrite(L1, leftForward ? HIGH : LOW); digitalWrite(L2, leftForward ? LOW : HIGH);
  digitalWrite(R1, rightForward ? HIGH : LOW); digitalWrite(R2, rightForward ? LOW : HIGH);
  digitalWrite(EN_L, HIGH); digitalWrite(EN_R, HIGH);
}
void setup() {
  const uint8_t pins[] = {EN_L, EN_R, L1, L2, R1, R2};
  for (uint8_t pin : pins) { digitalWrite(pin, LOW); pinMode(pin, OUTPUT); }
  drive(gesture::Stop);
  Serial.begin(9600);
  if (!radio.init()) { Serial.println("Radio init failed; motors disabled"); while (true) {} }
}
void loop() {
  uint8_t packet[RH_ASK_MAX_MESSAGE_LEN];
  uint8_t length = sizeof(packet);
  controller.tick(millis());
  if (radio.recv(packet, &length)) controller.accept(packet, length, millis());
  if (controller.command != applied) { drive(controller.command); applied = controller.command; }
}
