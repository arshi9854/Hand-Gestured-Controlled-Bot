#include <GestureControl.h>
#include <assert.h>
#include <stdio.h>
using namespace gesture;
int main() {
  assert(classify(0,0)==Stop); assert(classify(45,-45)==Stop);
  assert(classify(0,46)==Forward); assert(classify(0,-46)==Backward);
  assert(classify(-46,0)==Left); assert(classify(46,0)==Right);
  assert(classify(100,100)==Stop); assert(classify(70,90)==Forward);
  uint8_t stop[]={'G',1,Stop}, forward[]={'G',1,Forward}, bad[]={'G',1,99};
  Receiver r;
  r.accept(forward,3,0); assert(!r.armed && r.command==Stop);
  r.accept(stop,3,10); r.accept(forward,3,20); assert(r.command==Forward);
  r.tick(519); assert(r.command==Forward); r.tick(520); assert(!r.armed && r.command==Stop);
  r.accept(forward,3,521); assert(!r.armed);
  r.accept(stop,3,530); r.accept(forward,3,540); r.accept(bad,3,550); assert(!r.armed);
  Command c=Stop;
  assert(!decode(stop,2,c)); assert(!decode(stop,0,c));
  uint8_t wrongMagic[]={'X',1,Forward}, wrongVersion[]={'G',2,Forward};
  assert(!decode(wrongMagic,3,c)); assert(!decode(wrongVersion,3,c));
  r.accept(stop,3,0xfffffff0u); r.accept(forward,3,0xfffffff1u);
  r.tick(0x100u); assert(r.command==Forward); r.tick(0x200u); assert(!r.armed);
  r.accept(stop,3,1000); r.accept(forward,3,1500); assert(!r.armed);
  puts("PASS: directions, dead zone, malformed packets, arming, timeout, and clock rollover");
}
