#pragma once
#include <stdint.h>
#include <stddef.h>
namespace gesture {
enum Command : uint8_t { Stop = 0, Forward = 1, Backward = 2, Left = 3, Right = 4 };
inline Command classify(int x, int y, int threshold = 45) {
  const int ax = x < 0 ? -x : x, ay = y < 0 ? -y : y;
  if ((ax <= threshold && ay <= threshold) || ax == ay) return Stop;
  if (ay > ax) return y > 0 ? Forward : Backward;
  return x > 0 ? Right : Left;
}
// Payload: ASCII G, protocol version 1, command. RadioHead supplies frame CRC.
inline bool decode(const uint8_t* data, size_t size, Command& command) {
  if (size != 3 || data[0] != 'G' || data[1] != 1 || data[2] > Right) return false;
  command = static_cast<Command>(data[2]);
  return true;
}
struct Receiver {
  bool armed = false;
  uint32_t last = 0;
  Command command = Stop;
  void disarm() { armed = false; command = Stop; }
  void tick(uint32_t now) {
    if (armed && static_cast<uint32_t>(now - last) >= 500) disarm();
  }
  void accept(const uint8_t* data, size_t size, uint32_t now) {
    tick(now);
    Command next;
    if (!decode(data, size, next)) { disarm(); return; }
    if (next == Stop) armed = true;
    if (armed) { command = next; last = now; }
  }
};
}
