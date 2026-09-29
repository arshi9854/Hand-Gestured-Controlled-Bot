"""Render original, firmware-aligned connection diagrams as SVG and PNG.
Requires Pillow for PNG export. Symbols group pins by function, not footprint.
"""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/diagrams'
INK='#173047'; MUTED='#526779'; GREEN='#21835b'; RED='#bd423d'; BLUE='#237cba'; PURPLE='#7d51a2'
class Sheet:
 def __init__(self,title,sub):
  self.im=Image.new('RGB',(1600,1100),'white'); self.d=ImageDraw.Draw(self.im)
  self.svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100">','<rect width="1600" height="1100" fill="white"/>']
  self.text(60,42,title,34); self.text(60,95,sub,19,MUTED)
  self.line([(60,140),(1540,140)],'#d7e1e8',2)
 def text(self,x,y,s,size=20,color=INK):
  font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',size)
  self.d.text((x,y),s,font=font,fill=color)
  self.svg.append(f'<text x="{x}" y="{y+size*.92}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}">{escape(s)}</text>')
 def line(self,pts,color=GREEN,width=3):
  self.d.line(pts,fill=color,width=width)
  self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="{width}"/>')
 def box(self,x,y,w,h,title,fill='#edf5fa'):
  self.d.rounded_rectangle((x,y,x+w,y+h),radius=12,fill=fill,outline=INK,width=2)
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
  if title: self.text(x+20,y+16,title,max(12,min(23, int((w-40)/len(title) * 1.7))))
 def pin(self,x,y,label,side='right',color=GREEN):
  # x is the boundary; label is inside the component, wire ends 20 px outside.
  dx=20 if side=='right' else -20
  self.line([(x,y),(x+dx,y)],color)
  self.text(x-150 if side=='right' else x+14,y-12,label,18)
  return x+dx,y
 def footer(self):
  self.line([(60,1015),(1540,1015)],'#d7e1e8',2)
  self.text(60,1040,'HAND GESTURE CONTROLLED ROBOT  /  Reconstructed design · hardware validation pending',18,MUTED)
  self.text(60,1070,'Functional connection diagram: pin positions are symbolic. Named nets connect only within their own setup.',16,MUTED)
 def save(self,name):
  self.footer();OUT.mkdir(parents=True,exist_ok=True)
  (OUT/(name+'.svg')).write_text('\n'.join(self.svg+['</svg>']))
  self.im.save(OUT/(name+'.png'))

s=Sheet('01  /  Hand-controller transmitter','Analog hand tilt → Arduino Uno → matched ASK/OOK RF transmitter')
s.box(100,220,310,350,'ADXL335-compatible sensor','#fff0ec')
s.box(710,220,310,540,'Arduino Uno · TX')
for y,a,b,c in [(320,'VCC','3.3 V',RED),(375,'GND','GND',INK),(430,'X OUT','A0',GREEN),(485,'Y OUT','A1',GREEN)]:
 p=s.pin(410,y,a,color=c);q=s.pin(710,y,b,'left',c);s.line([p,q],c)
s.text(125,530,'Z OUT: unused / open',18,MUTED)
s.box(1190,440,330,310,'ASK/OOK RF · TX','#eef8ef')
p=s.pin(1020,570,'D12');q=s.pin(1190,570,'DATA','left');s.line([p,q])
p=s.pin(1190,630,'VCC','left',RED);s.line([p,(1090,630)],RED);s.text(1045,654,'V_RF_TX',18,RED)
p=s.pin(1190,710,'GND','left',INK);s.line([p,(1090,710)],INK);s.text(1050,735,'GND_TX',18,INK)
s.text(735,650,'D10, D11: reserved',18,MUTED);s.text(735,682,'Leave unconnected',18,MUTED)
s.text(735,280,'USB power input',18,BLUE)
s.box(100,810,1420,160,'Power and calibration notes','#f7f9fb')
s.text(125,855,'GND_TX: connect Uno GND, sensor GND, and transmitter supply negative together.',20)
s.text(125,890,'V_RF_TX: use the radio module’s rated supply and verify compatibility with Uno 5 V data output.',20)
s.text(125,925,'Sensor: use a confirmed 3.3 V-compatible breakout. Hold flat during startup calibration. No wire to robot ground.',20)
s.save('01-transmitter')

s=Sheet('02  /  Robot receiver and motor driver','RF DATA on D11 · L293D physical DIP pin numbers shown beside each signal')
s.box(60,215,280,220,'ASK/OOK RF · RX','#eef8ef')
s.box(510,215,280,660,'Arduino Uno · RX')
s.box(1000,215,290,660,'L293D · dual bridge','#f1edf8')
p=s.pin(340,310,'DATA');q=s.pin(510,310,'D11','left');s.line([p,q])
s.text(80,355,'VCC → V_RF_RX',18,RED);s.text(80,391,'GND → GND_RX',18)
for y,uno,ic in [(410,'D5','1 · EN LEFT'),(470,'D2','2 · IN1'),(530,'D3','7 · IN2'),(620,'D6','9 · EN RIGHT'),(680,'D4','10 · IN3'),(740,'D7','15 · IN4')]:
 p=s.pin(790,y,uno);q=s.pin(1000,y,ic,'left');s.line([p,q])
s.text(535,795,'D10, D12: reserved',18,MUTED);s.text(535,827,'USB power input',18,BLUE)
s.text(1020,274,'16 · VCC1 → +5V_LOGIC',18,RED)
s.text(1020,307,'8 · VCC2 → VMOTOR',18,RED)
s.text(1020,808,'4, 5, 12, 13 → GND_RX',18)
for y,title,labels in [(420,'M1 · LEFT',[(420,'3 · OUT1'),(480,'6 · OUT2')]),(640,'M2 · RIGHT',[(640,'11 · OUT3'),(700,'14 · OUT4')])]:
 s.box(1410,y-55,145,160,title,'#fff3c7')
 for yy,lab in labels:
  p=s.pin(1290,yy,lab,color=BLUE);s.line([p,(1410,yy)],BLUE)
s.box(60,485,345,380,'Connection notes','#f7f9fb')
for y,t in [(535,'V_RF_RX: module-rated supply'),(578,'Match TX/RX radio frequency'),(621,'Use Uno-compatible DATA level'),(664,'All robot grounds: GND_RX'),(707,'EN pins need 10 kΩ pulldowns'),(750,'Power details: see sheet 03'),(793,'Pin layout is symbolic')]: s.text(80,y,t,18,MUTED)
s.text(60,925,'Motor terminals are provisional: verify forward rotation with wheels raised; swap leads with power off if needed.',20)
s.text(60,963,'Stop disables both bridges. Enable and supply components are drawn on sheet 03 using the same net names.',20)
s.save('02-receiver')

s=Sheet('03  /  Robot power and enable details','Connect these nets to sheet 02 · motor power and logic power have a common robot ground')
# Five independent vertical circuits with explicitly named nets avoid ambiguous crossings.
xs=[170,475,780,1085,1390]
heads=['Logic bypass','Motor bypass','Left enable','Right enable','Motor supply']
for x,title in zip(xs,heads): s.text(x-105,205,title,23)
for x,net,pin in [(170,'+5V_LOGIC','L293D pin 16'),(475,'VMOTOR','L293D pin 8')]:
 s.text(x-85,275,net,21,RED);s.text(x-90,314,pin,18,MUTED)
 s.line([(x,355),(x,460)],RED)
 s.line([(x-34,460),(x+34,460)],INK,4);s.line([(x-34,479),(x+34,479)],INK,4)
 s.line([(x,479),(x,660)],INK);s.text(x+42,455,'0.1 µF',19)
 s.text(x-55,683,'GND_RX',20)
for x,net,pin in [(780,'Uno D5','L293D pin 1'),(1085,'Uno D6','L293D pin 9')]:
 s.text(x-65,275,net,21,GREEN);s.text(x-90,314,pin,18,MUTED)
 s.line([(x,355),(x,425)],GREEN)
 s.box(x-18,425,36,110,'',fill='white')
 s.text(x+35,463,'10 kΩ',20)
 s.line([(x,535),(x,660)],INK);s.text(x-55,683,'GND_RX',20)
s.text(1310,275,'Supply +',21,RED)
s.line([(1390,320),(1390,395)],RED)
s.line([(1390,395),(1420,450)],RED);s.line([(1390,465),(1390,590)],RED)
s.text(1440,415,'SW1',18)
s.text(1325,613,'VMOTOR',20,RED);s.text(1300,690,'Supply − → GND_RX',18)
s.box(60,765,1480,225,'Assembly notes','#f7f9fb')
for y,t in [(811,'+5V_LOGIC: regulated 5 V; USB-powered Uno 5 V output may feed driver logic only, within the USB current budget.'),(847,'GND_RX joins Uno GND, RF receiver GND, motor supply negative, and L293D pins 4, 5, 12, 13.'),(883,'Place bypass capacitors close to the driver. Add bulk capacitance appropriate to the motor supply and wiring.'),(919,'Choose VMOTOR for the actual motors and driver limits. Do not power the motors from the Uno 5 V pin.'),(955,'V_RF_RX is a separate module-rated rail unless its datasheet permits +5V_LOGIC. Never connect VMOTOR to VCC1.')]:s.text(85,y,t,19)
s.save('03-power-and-enables')
print('Rendered three SVG diagrams and three PNG exports.')
