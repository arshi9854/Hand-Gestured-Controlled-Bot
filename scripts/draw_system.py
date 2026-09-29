"""Original system illustrations for the reconstructed firmware; requires Pillow."""
from draw_circuits import Sheet, INK, MUTED, GREEN, RED, BLUE, PURPLE
import math
class Visual(Sheet):
 def footer(self):
  self.line([(60,1015),(1540,1015)],'#d7e1e8',2)
  self.text(60,1040,'HAND GESTURE CONTROLLED ROBOT  /  System illustrations · reconstructed reference design',18,MUTED)
  self.text(60,1070,'Illustrative snapshots, not photographs or measured results. Sensor mounting and motor direction require calibration.',16,MUTED)
 def polygon(self,pts,fill,stroke=INK):
  self.d.polygon(pts,fill=fill);self.line(pts+[pts[0]],stroke,2)
  self.svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
 def arrow(self,x1,y1,x2,y2,c=BLUE):
  self.line([(x1,y1),(x2,y2)],c,4)
  a=math.atan2(y2-y1,x2-x1)
  self.polygon([(x2,y2),(x2-15*math.cos(a-.45),y2-15*math.sin(a-.45)),(x2-15*math.cos(a+.45),y2-15*math.sin(a+.45))],c,c)
 def hand(self,x,y,scale=1,angle=0):
  # Stylized dorsal view with wrist and four separated fingers.
  shape=[(40,195),(40,165),(12,127),(0,101),(9,90),(25,104),(38,118),(36,44),(44,35),(53,42),(56,97),(57,15),(66,7),(76,14),(77,96),(81,7),(90,0),(100,8),(98,99),(108,28),(119,25),(125,36),(116,127),(106,155),(105,195)]
  a=math.radians(angle)
  def tr(p):
   px,py=p[0]-65,p[1]-110
   return (x+scale*(65+px*math.cos(a)-py*math.sin(a)),y+scale*(110+px*math.sin(a)+py*math.cos(a)))
  self.polygon([tr(p) for p in shape],'#f8e2cc')
  self.polygon([tr(p) for p in [(49,110),(101,110),(101,145),(49,145)]],'#daedf5')
  self.polygon([tr(p) for p in [(64,118),(87,118),(87,137),(64,137)]],BLUE)
 def bot(self,x,y,w=270,h=300,detail=True):
  self.box(x,y,w,h,'','#e6f0f5')
  for xx in [x-22,x+w-13]:self.box(xx,y+h*.50,35,h*.33,'','#344858')
  self.text(x+w/2-30,y+16,'FRONT',15,MUTED)
  if detail:
   self.box(x+24,y+58,w-48,55,'RF receiver','#eaf6ed')
   self.box(x+24,y+126,w-48,55,'Arduino Uno','#d9ecf7')
   self.box(x+24,y+194,w-48,55,'L293D','#eae2f5')
   self.arrow(x+w/2,y+113,x+w/2,y+126,GREEN);self.arrow(x+w/2,y+181,x+w/2,y+194,GREEN)
  else:self.box(x+28,y+65,w-56,60,'BOT','#d9ecf7')

def notes(s,lines,y=835):
 s.box(60,y,1480,155,'Reading this diagram','#f7f9fb')
 for i,t in enumerate(lines):s.text(85,y+48+i*32,t,19)

s=Visual('04  /  From hand tilt to robot movement','Whole-system view: two independently powered devices communicate through a one-way RF link')
s.box(60,190,580,600,'HAND CONTROLLER','#f8fafc');s.hand(95,305,1.3)
s.text(90,590,'ADXL335-compatible',21);s.text(90,624,'Hand-mounted tilt sensor',18,MUTED);s.text(90,657,'X to A0 / Y to A1',18,GREEN)
s.box(365,285,235,105,'Arduino Uno · TX');s.text(387,330,'Calibrate + classify',18)
s.box(365,465,235,105,'RF transmitter','#eaf6ed');s.text(387,510,'DATA from Uno D12',18)
s.arrow(280,452,345,340,GREEN);s.arrow(482,390,482,465,GREEN)
s.text(90,713,'Local power + GND_TX',20,RED)
s.arrow(640,518,940,518,BLUE);s.text(687,455,'WIRELESS RF',23,BLUE);s.text(668,552,'Matched ASK/OOK pair',18,MUTED)
s.text(679,590,'Receiver DATA to Uno D11',17,MUTED);s.text(679,623,'No cable between devices',17,MUTED)
s.box(960,190,580,600,'ROBOT RECEIVER','#f8fafc');s.bot(1110,300,270,335)
s.text(1020,680,'Left motor     ← L293D →     Right motor',20)
s.text(1020,726,'Logic + motor supplies share GND_RX',19,RED)
notes(s,['Tilt selects a direction; transmitter sends it; receiver validates it; the driver energizes the two motors.', 'The RF link carries commands, not power. Actual module frequency, voltage, chassis and sensor mounting are provisional.', 'Illustration matches the repository architecture; it is not evidence of the original robot’s physical appearance.'])
s.save('04-whole-system')

s=Visual('05  /  Hand gestures and wheel movement','Default reference mapping · positive / negative axes depend on how the sensor is mounted')
items=[('FORWARD','+Y dominates','Both wheels forward',0,1,1),('REVERSE','−Y dominates','Both wheels reverse',180,-1,-1),('LEFT TURN','−X dominates','Pivot counterclockwise',-25,-1,1),('RIGHT TURN','+X dominates','Pivot clockwise',25,1,-1),('NEUTRAL / STOP','Inside dead zone','Motor outputs disabled',0,0,0)]
for i,(title,axis,action,angle,l,r) in enumerate(items):
 x=60+i*300;s.box(x,195,280,610,title,'#f8fafc')
 s.hand(x+78,275,.78,angle if angle!=180 else 0)
 if i==0:s.arrow(x+215,410,x+215,310)
 elif i==1:s.arrow(x+215,310,x+215,410)
 elif i==2:s.arrow(x+200,435,x+85,435)
 elif i==3:s.arrow(x+85,435,x+200,435)
 s.text(x+22,470,axis,19,GREEN)
 s.bot(x+75,525,130,175,False)
 for xx,d in [(x+40,l),(x+240,r)]:
  if d:s.arrow(xx,655 if d>0 else 560,xx,560 if d>0 else 655,GREEN)
  else:s.line([(xx-10,605),(xx+10,605)],RED,4)
 s.text(x+20,730,action,17)
 s.text(x+20,765,'Command '+str([1,2,3,4,0][i]),18,MUTED)
notes(s,['Blue arrows illustrate intended hand directions. Tune sensor orientation / axis signs to make those motions match.', 'Wheel arrows show motion viewed from above, with the robot front at the top. Turning is an in-place pivot.', 'Dead zone: ±45 raw ADC counts on both axes. Equal absolute X/Y deviations also select STOP.'])
s.save('05-gesture-map')

s=Visual('06  /  How the control loop works','Calibrate once at startup; then repeat steps 2–6: sample → classify → transmit → validate → drive')
steps=[('1  Calibrate neutral',['Wait 2 s after radio init','Average 100 samples (~1 s)']),('2  Read hand tilt',['A0 = X; A1 = Y','Subtract neutral; apply signs']),('3  Choose command',['Dominant axis; 45-count threshold','Stop in dead zone or on a tie'])]
for i,(title,lines) in enumerate(steps):
 x=60+i*510;s.box(x,215,460,175,title)
 for j,t in enumerate(lines):s.text(x+22,277+j*35,t,19)
 if i<2:s.arrow(x+460,302,x+500,302,GREEN)
s.arrow(1310,390,1310,465,GREEN)
for x,title,lines in [(1080,'4  Send over RF',['Payload: G | version 1 | command','RadioHead frame CRC; 2,000 bit/s']), (570,'5  Validate on robot',['Check length, magic, version, command','STOP required to arm after link loss']), (60,'6  Apply motor command',['L293D selects wheel directions','Disable bridges before changing state'])]:
 s.box(x,465,460,175,title,'#eef7f1')
 for j,t in enumerate(lines):s.text(x+22,527+j*35,t,19)
 if x>60:s.arrow(x,552,x-50,552,GREEN)
s.box(60,700,1480,265,'Stop and reconnect behavior','#fff4ed')
for y,t in [(750,'No accepted packet for ≥500 ms → disable motor outputs and disarm.'),(792,'Malformed application payload → stop and disarm. A radio CRC failure is dropped; the timeout still runs.'),(834,'After startup or disarming → movement packets cannot arm the robot; a valid STOP packet must arrive first.'),(876,'Returning the hand to neutral sends STOP. Motors coast when disabled; the robot does not actively brake.'),(918,'The radio has no authentication or acknowledgements. Firmware hangs and stuck sensor values are not covered.')]:s.text(85,y,t,20)
s.save('06-control-flow')

s=Visual('07  /  Important operating snapshots','Illustrated bench sequence · expected behavior, not recorded test results')
states=[('A  POWER ON / CALIBRATE','Hold the controller flat',['Transmitter measures neutral.','Receiver stays disabled.'],'#edf5fa'),('B  NEUTRAL / ARM','Keep the hand centered',['A valid STOP packet arms the receiver.','Motors remain disabled.'],'#eef7f1'),('C  TILT / DRIVE','Tilt after arming',['Direction packets update the motors.','Return to neutral to stop.'],'#edf5fa'),('D  LINK LOST / RECOVER','Switch transmitter off',['After ~500 ms without accepted data: stop.','Reconnect, then return to neutral to re-arm.'],'#fff4ed')]
for i,(title,caption,lines,fill) in enumerate(states):
 x=60+(i%2)*755;y=190+(i//2)*395
 s.box(x,y,725,365,title,fill);s.hand(x+30,y+75,.75,25 if i==2 else 0)
 s.bot(x+530,y+65,130,170,False)
 if i in (0,3):
  color=RED if i==3 else MUTED
  for dx in range(190,470,32):s.line([(x+dx,y+160),(x+dx+16,y+160)],color,3)
  s.line([(x+322,y+150),(x+342,y+170)],color,3)
  s.line([(x+322,y+170),(x+342,y+150)],color,3)
 else:s.arrow(x+190,y+160,x+470,y+160,BLUE)
 s.text(x+190,y+113,'RF timeout' if i==3 else ('No packets yet' if i==0 else ('DIRECTION' if i==2 else 'STOP packet')),19)
 s.text(x+30,y+250,caption,21)
 for j,t in enumerate(lines):s.text(x+30,y+292+j*28,t,18,MUTED)
s.save('07-operating-snapshots')
print('Rendered four system diagrams in SVG and PNG.')
