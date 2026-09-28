#!/usr/bin/env python3
# patch_gesture3.py - keep the chest and hips still while the arms move: the arm weight now starts further out
# (x > 0.50 instead of 0.34) so only the arms bend; the body sway is removed; gestures a little smaller; more arm
# glitter (denser cloud, stronger flare while moving). Idempotent.
import sys
R=[
 ("float aw(vec3 p,float side){ return smoothstep(0.34,0.50,p.x*side)*smoothstep(0.22,-0.12,p.y); }",
  "float aw(vec3 p,float side){ return smoothstep(0.50,0.66,p.x*side)*smoothstep(0.22,-0.12,p.y); }"),
 ("body.position.y=Math.sin(now*0.0011)*0.01; { const E=(window._gest&&window._gest.E)||0; body.rotation.y=Math.sin(now*0.0004)*0.025+E*0.05*Math.sin(now*0.0006+2.0); body.rotation.z=E*0.018*Math.sin(now*0.0007); body.position.x=E*0.03*Math.sin(now*0.0005+1.0); }",
  "body.position.y=Math.sin(now*0.0011)*0.01; body.rotation.y=Math.sin(now*0.0004)*0.025; body.rotation.z=0; body.position.x=0;"),
 ("armT.L.set(-E*(0.12+0.55*wl), E*(0.08+0.42*fl)); armT.R.set(E*(0.12+0.55*wr), E*(0.08+0.42*fr));",
  "armT.L.set(-E*(0.10+0.45*wl), E*(0.08+0.40*fl)); armT.R.set(E*(0.10+0.45*wr), E*(0.08+0.40*fr));"),
 ("if(Math.abs(x)<0.5||y>0.0||Math.random()<(LITE?0.97:0.86)) continue; const off=0.02+Math.pow(Math.random(),1.5)*0.22;",
  "if(Math.abs(x)<0.55||y>0.0||Math.random()<(LITE?0.95:0.72)) continue; const off=0.02+Math.pow(Math.random(),1.5)*0.30;"),
 ("*(1.0+uArmV*2.2); c=mix(mix(CY,vec3(0.85,0.95,1.0),tw),vec3(0.95,0.99,1.0),uArmV*0.7); }",
  "*(1.0+uArmV*3.5); c=mix(mix(CY,vec3(0.85,0.95,1.0),tw),vec3(0.95,0.99,1.0),uArmV*0.8); }"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "smoothstep(0.50,0.66,p.x*side)" in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:70])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
