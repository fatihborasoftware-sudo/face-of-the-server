#!/usr/bin/env python3
# patch_gesture2.py - calm talk gestures: instead of jumping to new poses on each syllable, the arms wander slowly
# (layered slow sines, like the head's idle wander), lifted by the speech energy and settling in the pauses; the
# arm easing is slower, and the whole body sways very gently while speaking. Replaces the beat gestures. Idempotent.
import sys
NEW = r"""if(talking||G.E>0.01){ if(talking) G.rest=now; const tE=talking?Math.min(1,0.35+level*0.7):0; G.E=(G.E||0)+(tE-(G.E||0))*(tE>(G.E||0)?0.035:0.012); const E=G.E, T=now*0.001;
        const wl=0.5+0.5*Math.sin(T*0.9+1.7)*0.6+0.4*Math.sin(T*0.53+0.4), wr=0.5+0.5*Math.sin(T*0.83)*0.6+0.4*Math.sin(T*0.47+2.1);
        const fl=0.5+0.5*Math.sin(T*0.71+2.3)*0.7+0.3*Math.sin(T*0.37+1.1), fr=0.5+0.5*Math.sin(T*0.66+0.9)*0.7+0.3*Math.sin(T*0.41+3.0);
        armT.L.set(-E*(0.12+0.55*wl), E*(0.08+0.42*fl)); armT.R.set(E*(0.12+0.55*wr), E*(0.08+0.42*fr)); G.L.p=armT.L.x; G.R.p=armT.R.x; G.L.t=armT.L.y; G.R.t=armT.R.y; }"""
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "G.E>0.01" in s: print(f,'already patched'); continue
    i=s.find("if(talking){ G.rest=now;"); j=s.find("armT[s].set(g.p,g.t); }); } }", i)
    if i<0 or j<0: sys.exit(f+': gesture block not found')
    j+=len("armT[s].set(g.p,g.t); }); } }")-1   # keep the closing brace of the outer block
    s=s[:i]+NEW+s[j:]
    a="const ka=1-Math.pow(0.001,dt*0.55), kd=1-Math.pow(0.001,dt*0.32); U.uArmL.value.lerp(armT.L,ka);"
    b="const ka=1-Math.pow(0.001,dt*(window._gest&&window._gest.E>0.02?0.22:0.55)), kd=1-Math.pow(0.001,dt*0.32); U.uArmL.value.lerp(armT.L,ka);"
    if s.count(a)!=1: sys.exit(f+': lerp anchor not found')
    s=s.replace(a,b,1)
    a2="const tv=Math.min(1,v*0.45);"; b2="const tv=Math.min(1,v*1.3);"
    if s.count(a2)!=1: sys.exit(f+': uArmV anchor not found')
    s=s.replace(a2,b2,1)
    # a gentle body sway while speaking: the whole figure leans and drifts slowly with the speech energy
    a3="body.position.y=Math.sin(now*0.0011)*0.01; body.rotation.y=Math.sin(now*0.0004)*0.025;"
    b3="body.position.y=Math.sin(now*0.0011)*0.01; { const E=(window._gest&&window._gest.E)||0; body.rotation.y=Math.sin(now*0.0004)*0.025+E*0.05*Math.sin(now*0.0006+2.0); body.rotation.z=E*0.018*Math.sin(now*0.0007); body.position.x=E*0.03*Math.sin(now*0.0005+1.0); }"
    if s.count(a3)!=1: sys.exit(f+': sway anchor not found')
    s=s.replace(a3,b3,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
