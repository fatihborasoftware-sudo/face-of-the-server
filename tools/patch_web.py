#!/usr/bin/env python3
# patch_web.py - "web throw": while an arm moves, its glitter streams outward from the hand along the arm's
# direction (each speck a different distance, with a slow wave), and the stream builds up and dies down slowly
# instead of flashing. Idempotent.
import sys
R=[
 ("vec3 p=aKind>1.5?bendL(pb,0.35+0.6*aSeed):bend(pb);",
  "vec3 p=aKind>1.5?bendL(pb,0.2+0.8*aSeed):bend(pb); if(aKind>1.5&&uArmV>0.001){ float sd=pb.x<0.0?-1.0:1.0; float w=aw(pb,sd); if(w>0.001){ vec3 dir=normalize(p-vec3(sd*0.46,-0.30,0.0)); float st=uArmV*w*(0.3+3.4*aSeed); p+=dir*st+vec3(sin(uTime*1.4+aSeed*31.0),cos(uTime*1.1+aSeed*17.0),sin(uTime*0.9+aSeed*23.0))*0.09*st; } }"),
 ("const tv=Math.min(1,v*1.3); U.uArmV.value+=(tv-U.uArmV.value)*(tv>U.uArmV.value?0.5:0.06);",
  "const tv=Math.min(1,v*2.6); U.uArmV.value+=(tv-U.uArmV.value)*(tv>U.uArmV.value?0.07:0.02);"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "float st=uArmV*w*" in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:70])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
