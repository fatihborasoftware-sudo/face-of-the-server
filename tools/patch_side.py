#!/usr/bin/env python3
# patch_side.py - sleep glitter gathers as a cloud on a random side of the screen (left or right, new pick each time);
# it drifts slowly there, and on wake-up the body assembles from where the cloud is. Applies after patch_field.py. Idempotent.
import sys, re
R=[
 ("if(es>0.0){ vec3 g=vec3((fract(sin(aSeed*127.1+311.7)*43758.5453)-0.5)*5.8,(fract(sin(aSeed*269.5+183.3)*43758.5453)-0.5)*2.7,(fract(sin(aSeed*419.2+371.9)*43758.5453)-0.5)*1.0);\n          g.x=mod(g.x+uTime*0.12*(fract(sin(aSeed*77.7+13.1)*43758.5453)-0.5)+2.9,5.8)-2.9;",
  "if(es>0.0){ vec3 g=vec3((fract(sin(aSeed*127.1+311.7)*43758.5453)-0.5)*2.6,(fract(sin(aSeed*269.5+183.3)*43758.5453)-0.5)*2.6,(fract(sin(aSeed*419.2+371.9)*43758.5453)-0.5)*1.0);\n          g.x=mod(g.x+uTime*0.12*(fract(sin(aSeed*77.7+13.1)*43758.5453)-0.5)+1.3,2.6)-1.3; g+=uBubble;"),
 ("if(wantSleep&&!asleep){ asleep=true;", "if(wantSleep&&!asleep){ asleep=true; sleepSide=Math.random()<0.5?-1:1; sleepT0=now;"),
 ("if(asleep){ const ts=now*0.001; U.uBubble.value.set(2.6*Math.sin(ts*0.11),1.0*Math.sin(ts*0.073+1.0),0.3*Math.sin(ts*0.05)); }",
  "if(asleep){ const ts=(now-sleepT0)*0.001; U.uBubble.value.set(sleepSide*2.0+0.4*Math.sin(ts*0.09),0.5*Math.sin(ts*0.07),0.2*Math.sin(ts*0.05)); }"),
 ("let lastTouch=performance.now(), asleep=false, sleepV=0;", "let lastTouch=performance.now(), asleep=false, sleepV=0, sleepSide=1, sleepT0=0;"),
 ("sleepV+=((asleep?1:0)-sleepV)*Math.min(1,dt*(asleep?0.22:0.45)); if(Math.abs(sleepV-(asleep?1:0))<0.003) sleepV=asleep?1:0;", "if(asleep){ sleepV+=(1-sleepV)*Math.min(1,dt*0.22); if(sleepV>0.997) sleepV=1; } else { sleepV=Math.max(0,sleepV-dt/6.5); } // waking: a steady 6.5 s assembly from the cloud"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'sleepSide' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
