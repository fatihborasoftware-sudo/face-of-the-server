#!/usr/bin/env python3
# patch_edge.py - sleep in two stages: the body loosens into glitter, then the glitter spreads out along the EDGES of the
# screen (around the dashboard) and floats there; a few specks rain slowly down through the dashboard. On wake-up the
# dashboard blurs away into dust while the particles fly back into the body. Applies after patch_side.py. Idempotent.
import sys, re
NEW=("if(es>0.0){ vec3 rnd=vec3(fract(sin(aSeed*127.1+311.7)*43758.5453),fract(sin(aSeed*269.5+183.3)*43758.5453),fract(sin(aSeed*419.2+371.9)*43758.5453)); float role=fract(sin(aSeed*91.3+7.7)*43758.5453);\n"
     "          vec3 gc=p+(rnd-0.5)*0.9+vec3(sin(uTime*0.5+aSeed*40.0),cos(uTime*0.4+aSeed*27.0),sin(uTime*0.45+aSeed*19.0))*0.12; /* stage 1: loose glitter body */\n"
     "          vec3 ge; if(role<0.12){ ge=vec3((rnd.x-0.5)*6.6, 1.35-mod(uTime*(0.22+0.3*rnd.y)+rnd.x*13.0,3.7), (rnd.z-0.5)*0.6); } /* rain through the dashboard */\n"
     "          else { float W=3.75,H=1.78; float t=fract(rnd.x+uTime*0.012*(rnd.y-0.5)); float per=4.0*(W+H); float d=t*per; vec2 q;\n"
     "            if(d<2.0*W) q=vec2(-W+d,H); else if(d<2.0*W+2.0*H) q=vec2(W,H-(d-2.0*W)); else if(d<4.0*W+2.0*H) q=vec2(W-(d-2.0*W-2.0*H),-H); else q=vec2(-W,-H+(d-4.0*W-2.0*H));\n"
     "            q*=1.0+(rnd.z-0.5)*0.11; ge=vec3(q.x, q.y-0.45, (fract(rnd.z*7.0)-0.5)*0.8)+vec3(sin(uTime*0.3+aSeed*40.0),cos(uTime*0.25+aSeed*27.0),0.0)*0.06; } /* the frame around the dashboard */\n"
     "          float es2=smoothstep(rnd.y*0.5,rnd.y*0.5+0.5,uSpread); es2=es2*es2*(3.0-2.0*es2);\n"
     "          fly=mix(fly,gc,es); fly=mix(fly,ge,es*es2); }")
R=[
 ("uSleep:{value:0},uBody:{value:0},", "uSleep:{value:0},uBody:{value:0},uSpread:{value:0},"),
 ("uniform float uBuild,uLevel,uThink,uPix,uMood,uSleep,uBody;", "uniform float uBuild,uLevel,uThink,uPix,uMood,uSleep,uBody,uSpread;"),
 ("let lastTouch=performance.now(), asleep=false, sleepV=0,", "let lastTouch=performance.now(), asleep=false, sleepV=0, spreadV=0,"),
 ("if(asleep){ sleepV+=(1-sleepV)*Math.min(1,dt*0.22); if(sleepV>0.997) sleepV=1; } else { sleepV=Math.max(0,sleepV-dt/6.5); }",
  "if(asleep){ sleepV+=(1-sleepV)*Math.min(1,dt*0.22); if(sleepV>0.997) sleepV=1; spreadV=sleepV>0.85?Math.min(1,spreadV+dt/5):spreadV; } else { sleepV=Math.max(0,sleepV-dt/6.5); spreadV=Math.max(0,spreadV-dt/4.5); }\n"
  "    U.uSpread.value=spreadV; { const sl=document.getElementById('sl'); if(sl){ const k=asleep?spreadV:Math.max(0,spreadV*1.25-0.25); sl.style.opacity=k; sl.style.filter='blur('+((1-k)*5).toFixed(1)+'px)'; sl.style.transform='scale('+(1+(1-k)*0.04).toFixed(3)+')'; sl.style.transformOrigin='50% 40%'; sl.style.letterSpacing=((1-k)*0.25+0.06).toFixed(2)+'em'; } }"),
 ("  body.sleep #sl{opacity:1}\n", ""),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'uSpread' in s: print(f,'already patched'); continue
    s2=re.sub(r"if\(es>0\.0\)\{ vec3 g=vec3\(\(fract\(sin\(aSeed\*127\.1.*?fly=mix\(fly,g,es\); \}", NEW, s, count=1, flags=re.S)
    if s2==s: sys.exit(f+': glitter block not found'); 
    s=s2
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    s=s.replace("#sl{position:fixed;left:24px;right:24px;top:74px;bottom:64px;max-width:1500px;margin:0 auto;display:grid;grid-template-columns:1.15fr 1.15fr 1fr;grid-template-rows:auto auto auto 1fr;gap:12px;opacity:0;pointer-events:none;transition:opacity .9s;",
                "#sl{position:fixed;left:24px;right:24px;top:74px;bottom:64px;max-width:1500px;margin:0 auto;display:grid;grid-template-columns:1.15fr 1.15fr 1fr;grid-template-rows:auto auto auto 1fr;gap:12px;opacity:0;pointer-events:none;",1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
