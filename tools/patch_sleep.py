#!/usr/bin/env python3
# patch_sleep.py - "glitter mode": when nobody has used the figure for a while (default 60 s) the body dissolves into
# particles that drift around the window; any mouse move, click, key, camera face, voice state or agent gesture wakes it
# and the body reassembles with the assembly sound. window.FB_SLEEP_MS changes the delay. Idempotent.
import sys
R=[
 # uniforms
 ("uMood:{value:0},", "uMood:{value:0},uSleep:{value:0},uBody:{value:0},"),
 # particle shader: build from uBody, then drift to a float field when asleep
 ("vertexShader:bendGLSL+`uniform float uBuild,uLevel,uThink,uPix,uMood; uniform vec3 uDrift; attribute vec3 aStart;",
  "vertexShader:bendGLSL+`uniform float uBuild,uLevel,uThink,uPix,uMood,uSleep,uBody; uniform vec3 uDrift; attribute vec3 aStart;"),
 ("float e=smoothstep(aSeed*0.55,aSeed*0.55+0.45,uBuild); e=e*e*(3.0-2.0*e);",
  "float e=smoothstep(aSeed*0.55,aSeed*0.55+0.45,uBody); e=e*e*(3.0-2.0*e);"),
 ("vec3 fly=mix(s,p,e); fly.x+=sin(e*3.1416)*(0.6*(aSeed-0.5)); fly.z+=sin(e*3.1416)*0.8;",
  "vec3 fly=mix(s,p,e); fly.x+=sin(e*3.1416)*(0.6*(aSeed-0.5)); fly.z+=sin(e*3.1416)*0.8;\n"
  "        // glitter mode: each speck has its own resting spot spread over the window and drifts slowly around it\n"
  "        float es=smoothstep(aSeed*0.6,aSeed*0.6+0.4,uSleep); es=es*es*(3.0-2.0*es);\n"
  "        if(es>0.0){ vec3 g=vec3((fract(sin(aSeed*127.1+311.7)*43758.5453)-0.5)*11.0,(fract(sin(aSeed*269.5+183.3)*43758.5453)-0.5)*6.0,(fract(sin(aSeed*419.2+371.9)*43758.5453)-0.5)*3.0);\n"
  "          g.x=mod(g.x+uTime*0.12*(fract(sin(aSeed*77.7+13.1)*43758.5453)-0.5)+5.5,11.0)-5.5; g+=vec3(sin(uTime*0.17+aSeed*40.0)*0.7,cos(uTime*0.13+aSeed*27.0)*0.45,sin(uTime*0.11+aSeed*19.0)*0.3);\n"
  "          fly=mix(fly,g,es); }"),
 ("a*=mix(1.4,1.0,e)*mix(1.0,0.5,smoothstep(0.2,0.4,position.y));",
  "a*=mix(1.4,1.0,e)*mix(1.0,0.5,smoothstep(0.2,0.4,position.y)); a=mix(a,(0.25+0.5*tw)*(0.5+0.5*fract(aSeed*4.7)),es); c=mix(c,mix(CY,vec3(0.9,0.97,1.0),tw*0.6),es);"),
 ("+0.8*(1.0-e))*uPix*(5.0/-mv.z);", "+0.8*(1.0-e)+1.4*es)*uPix*(5.0/-mv.z);"),
 # wake-up hooks
 ("function setTargetFromScreen(nx,ny){", "let lastTouch=performance.now(), asleep=false, sleepV=0; window.fbTouch=()=>{ lastTouch=performance.now(); };\n  addEventListener('pointerdown',window.fbTouch); addEventListener('keydown',window.fbTouch); addEventListener('touchstart',window.fbTouch);\n  function setTargetFromScreen(nx,ny){ lastTouch=performance.now();"),
 ("window.serraArm=(side,phi,th)=>{", "window.serraArm=(side,phi,th)=>{ if(phi||th) lastTouch=performance.now();"),
 ("const breath=0.9+0.1*Math.sin(now*0.0016), B=b*b;", "const breath=0.9+0.1*Math.sin(now*0.0016), B=b*b*(1-sleepV);"),
 ("const setState=s=>{mode=s;", "const setState=s=>{if(s!=='idle') lastTouch=performance.now(); mode=s;"),
 # tick
 ("const b=Math.min(1,(now-buildT0)/BUILD_MS); U.uBuild.value=b;",
  "const b=Math.min(1,(now-buildT0)/BUILD_MS); U.uBody.value=b;\n"
  "    const wantSleep=b>=1&&(now-lastTouch)>(window.FB_SLEEP_MS||60000)&&mode==='idle';\n"
  "    if(wantSleep&&!asleep){ asleep=true; if(window.sfx) window.sfx('whoosh'); statusEl.textContent='STATUS: DRIFTING'; }\n"
  "    else if(!wantSleep&&asleep){ asleep=false; if(window.sfx) window.sfx('assemble'); setState(mode); }\n"
  "    sleepV+=((asleep?1:0)-sleepV)*Math.min(1,dt*(asleep?0.22:0.45)); if(Math.abs(sleepV-(asleep?1:0))<0.003) sleepV=asleep?1:0;\n"
  "    U.uSleep.value=sleepV; U.uBuild.value=b*(1-sleepV);"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'uSleep' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
