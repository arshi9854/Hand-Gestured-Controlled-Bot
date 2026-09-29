// Reconstructed reference firmware; not recovered original code.
#include <SPI.h>
#include <RH_ASK.h>
#include <GestureControl.h>
RH_ASK radio(2000, 11, 12, 10);
int neutralX = 0, neutralY = 0;
const int X_SIGN = 1, Y_SIGN = 1; // Change to -1 if mounting reverses an axis.
void setup() {
  Serial.begin(9600);
  if (!radio.init()) { Serial.println("Radio init failed"); while (true) {} }
  Serial.println("Hold hand flat and still: calibrating in 2 seconds");
  delay(2000);
  long sumX = 0, sumY = 0;
  for (int i = 0; i < 100; ++i) {
    sumX += analogRead(A0); sumY += analogRead(A1); delay(10);
  }
  neutralX = sumX / 100; neutralY = sumY / 100;
  Serial.println("Calibration complete");
}
void loop() {
  int x = X_SIGN * (analogRead(A0) - neutralX);
  int y = Y_SIGN * (analogRead(A1) - neutralY);
  gesture::Command command = gesture::classify(x, y);
  uint8_t packet[] = {'G', 1, static_cast<uint8_t>(command)};
  if (radio.send(packet, sizeof(packet))) radio.waitPacketSent();
  Serial.print(x); Serial.print(','); Serial.print(y); Serial.print(','); Serial.println(packet[2]);
  delay(50); // Interval also includes packet airtime; not a claimed 20 Hz rate.
}
