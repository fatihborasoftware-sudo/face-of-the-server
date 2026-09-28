#!/usr/bin/env python3
# patch_bubble.py - glitter mode as a bubble: while asleep the specks gather in a floating ball that wanders around the
# screen; on wake-up the body assembles from wherever the bubble is. Applies on top of patch_sleep.py. Idempotent.
import sys, re
NEW=("if(es>0.0){ vec3 rnd=vec3(fract(sin(aSeed*127.1+311.7)*43758.5453),fract(sin(aSeed*269.5+183.3)*43758.5453),fract(sin(aSeed*419.2+371.9)*43758.5453));\n"
     "          float th=rnd.x*6.2832+uTime*0.25*(0.4+rnd.z), ph=acos(2.0*rnd.y-1.0), rr=pow(rnd.z,0.38)*0.8;\n"
     "          vec3 g=uBubble+vec3(sin(ph)*cos(th),sin(ph)*sin(th),cos(ph))*rr+vec3(sin(uTime*0.9+aSeed*40.0),cos(uTime*0.7+aSeed*27.0),sin(uTime*0.8+aSeed*19.0))*0.06;\n"
     "          fly=mix(fly,g,es); }")
R=[
 ("uSleep:{value:0},uBody:{value:0},", "uSleep:{value:0},uBody:{value:0},uBubble:{value:new THREE.Vector3(2.5,0.3,0)},"),
 ("uniform float uBuild,uLevel,uThink,uPix,uMood,uSleep,uBody; uniform vec3 uDrift;", "uniform float uBuild,uLevel,uThink,uPix,uMood,uSleep,uBody; uniform vec3 uDrift,uBubble;"),
 ("a=mix(a,(0.25+0.5*tw)*(0.5+0.5*fract(aSeed*4.7)),es);", "a=mix(a,(0.2+0.32*tw)*(0.5+0.5*fract(aSeed*4.7)),es);"),
 ("U.uSleep.value=sleepV; U.uBuild.value=b*(1-sleepV);",
  "U.uSleep.value=sleepV; U.uBuild.value=b*(1-sleepV);\n    if(asleep){ const ts=now*0.001; U.uBubble.value.set(2.6*Math.sin(ts*0.11),1.0*Math.sin(ts*0.073+1.0),0.3*Math.sin(ts*0.05)); } // the bubble wanders; it stops where it is when woken, and the body forms from there"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'uBubble' in s: print(f,'already patched'); continue
    s2=re.sub(r"if\(es>0\.0\)\{ vec3 g=vec3\(\(fract\(sin\(aSeed\*127\.1.*?fly=mix\(fly,g,es\); \}", NEW, s, count=1, flags=re.S)
    if s2==s: sys.exit(f+': glitter block not found')
    s=s2
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
