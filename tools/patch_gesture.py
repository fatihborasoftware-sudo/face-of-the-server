#!/usr/bin/env python3
# patch_gesture.py - talk gestures for the Face: while Khoa speaks, the arms move like a person talking with their
# hands (beat gestures on the loud syllables, held poses, both hands on emphasis, slow return to rest in the pauses).
# The arm glitter flares and streaks with the speed of the hand (uArmV), so the movement reads as light, not as a
# moved image. Face page only (the Command Map keeps its node-pointing arm). Idempotent.
import sys
GEST = r"""    // talk gestures: hands move with the speech - a beat on each loud syllable, a held pose, rest in the pauses
    { const G=window._gest||(window._gest={L:{p:0,t:0,hold:0},R:{p:0,t:0,hold:0},lv:0,onset:0,rest:0}); const talking=window.fbGestures!==false&&(mode==='speaking'||level>0.15)&&!building&&sleepV<0.5;
      if(talking){ G.rest=now; const on=level>0.35&&now-G.onset>300&&(level>G.lv*1.1||now-G.onset>700+Math.random()*600); G.lv=level*0.12+G.lv*0.88;
        if(on){ G.onset=now; const r=Math.random(), both=r<0.28; const pick=s=>{ const g=G[s], sg=s==='L'?-1:1, amp=0.3+Math.random()*0.6; g.p=sg*amp; g.t=0.2+Math.random()*0.5; g.hold=now+350+Math.random()*900; };
          if(both||r<0.64) pick('R'); if(both||r>=0.64) pick('L'); }
        ['L','R'].forEach(s=>{ const g=G[s], sg=s==='L'?-1:1; if(now>g.hold){ g.p*=0.985; g.t*=0.985; } const flick=0.07*level*Math.sin(now*0.021+(s==='L'?1.7:0)); armT[s].set(g.p+sg*flick, g.t+0.04*Math.sin(now*0.013+(s==='L'?2.3:0))); }); }
      else if(now-G.rest<3000&&(G.L.p||G.R.p||G.L.t||G.R.t)){ ['L','R'].forEach(s=>{ const g=G[s]; g.p*=0.95; g.t*=0.95; if(Math.abs(g.p)<0.01) g.p=0; if(Math.abs(g.t)<0.01) g.t=0; armT[s].set(g.p,g.t); }); } }
    { const pl=U.uArmL.value.clone(), pr=U.uArmR.value.clone(); const ka=1-Math.pow(0.001,dt*0.55), kd=1-Math.pow(0.001,dt*0.32); U.uArmL.value.lerp(armT.L,ka); U.uArmR.value.lerp(armT.R,ka); U.uArmLd.value.lerp(U.uArmL.value,kd); U.uArmRd.value.lerp(U.uArmR.value,kd);
      const v=(pl.distanceTo(U.uArmL.value)+pr.distanceTo(U.uArmR.value))/Math.max(0.001,dt); const tv=Math.min(1,v*0.45); U.uArmV.value+=(tv-U.uArmV.value)*(tv>U.uArmV.value?0.5:0.06); }"""
R=[
 ("    { const ka=1-Math.pow(0.001,dt*0.55), kd=1-Math.pow(0.001,dt*0.32); U.uArmL.value.lerp(armT.L,ka); U.uArmR.value.lerp(armT.R,ka); U.uArmLd.value.lerp(U.uArmL.value,kd); U.uArmRd.value.lerp(U.uArmR.value,kd); }",
  GEST),
 ("uniform vec2 uArmL,uArmR,uArmLd,uArmRd;", "uniform vec2 uArmL,uArmR,uArmLd,uArmRd; uniform float uArmV;"),
 ("uArmLd:{value:new THREE.Vector2()},", "uArmLd:{value:new THREE.Vector2()},uArmV:{value:0},"),
 # glitter: flares white and grows with hand speed
 ("a=(0.05+0.35*tw)*(0.3+0.7*(1.0-aSeed))*(0.35+0.65*clamp(armAmt*2.0,0.,1.)); c=mix(CY,vec3(0.85,0.95,1.0),tw); }",
  "a=(0.05+0.35*tw)*(0.3+0.7*(1.0-aSeed))*(0.35+0.65*clamp(armAmt*2.0,0.,1.))*(1.0+uArmV*2.2); c=mix(mix(CY,vec3(0.85,0.95,1.0),tw),vec3(0.95,0.99,1.0),uArmV*0.7); }"),
 ("(aKind>1.5?0.9*aSeed:0.0)", "(aKind>1.5?0.9*aSeed+1.6*uArmV*aSeed:0.0)"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "window._gest" in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:70])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
