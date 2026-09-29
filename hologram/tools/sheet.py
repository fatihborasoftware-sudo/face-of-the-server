import sys; sys.path.insert(0,'/root/holo')
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from gauge import gauge; from morph import morph
def curve(a):
    x=a/255.0; x=np.interp(x,[0,0.025,0.2,0.55,1],[0,0,0.42,0.85,1]); return x*255
def khoa(n):
    im=cv2.imread(f'/root/holo/st-{n}.png')[70:670,84:684]; im=cv2.resize(im,(768,768),interpolation=cv2.INTER_CUBIC).astype(np.float32); return curve(im)
G=cv2.cvtColor(np.asarray(gauge(82,100,'#39ff6a',t=0.3)),cv2.COLOR_RGB2BGR).astype(np.float32)
green=khoa('green')
rows=[
 ('IDLE LOOP  ·  about 30 s, repeats',[('1  Morph in',khoa('asm1'),'dust gathers + morph-in sound'),('2  Body forms',khoa('asm2'),'sound locks in'),('3  Looks left',khoa('left'),'slow head turns'),('4  Looks right',khoa('right'),'breathes, glows'),('5  Morph out',khoa('asm2'),'body scatters to dust, loop')]),
 ('TALKING WITH GAUGES  ·  e.g. "backups"',[('1  Khoa talks',green,'turns green'),('2  Bursts to dust',morph(green,G,0.25),'body scatters'),('3  Dust swirls',morph(green,G,0.55),'green dust cloud'),('4  Gauge forms',morph(green,G,0.85),'dust lands on the ring'),('5  Gauge live',G,'ring fills, heartbeat runs')]),
]
T=300; pad=16
sheet=Image.new('RGB',(pad+5*(T+pad), 60+2*(T+110)),(12,16,22)); d=ImageDraw.Draw(sheet)
fb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22); fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15); fl=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
y=14
for title,cells in rows:
    d.text((pad,y),title,font=fb,fill=(111,220,255)); y+=38
    for i,(lab,img,cap) in enumerate(cells):
        x=pad+i*(T+pad)
        im=Image.fromarray(cv2.cvtColor(np.clip(img,0,255).astype(np.uint8),cv2.COLOR_BGR2RGB)).resize((T,T),Image.LANCZOS)
        m=Image.new('L',(T,T),0); ImageDraw.Draw(m).ellipse((0,0,T-1,T-1),fill=255)
        bg=Image.new('RGB',(T,T),(34,38,46)); bg.paste(im,(0,0),m); ImageDraw.Draw(bg).ellipse((0,0,T-1,T-1),outline=(80,100,120),width=2)
        sheet.paste(bg,(x,y)); d.text((x,y+T+6),lab,font=fl,fill=(230,236,242)); d.text((x,y+T+28),cap,font=fs,fill=(150,165,180))
        if i<4: d.text((x+T+2,y+T//2-10),'›',font=fb,fill=(111,220,255))
    y+=T+72
sheet.save('/mnt/user-data/outputs/khoa-idle-and-gauges-mockups.png'); print(sheet.size)
