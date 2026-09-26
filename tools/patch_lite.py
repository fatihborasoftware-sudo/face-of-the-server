#!/usr/bin/env python3
# patch_lite.py — adds a "?lite" mode to face.html / map.html (or index.html) for weak GPUs (the laptop kiosk):
# lower pixel ratio, no bloom pass, fewer particles, no landscape/dust. Idempotent. Usage: python3 patch_lite.py FILE...
import sys, re
R=[
 ("renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.setClearColor(0x000000,1); renderer.autoClear=false;",
  "const LITE=/[?&]lite/.test(location.search)||/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname); window.FB_LITE=LITE;\n  renderer.setPixelRatio(LITE?0.6:Math.min(devicePixelRatio,2)); renderer.setClearColor(0x000000,1); renderer.autoClear=false;"),
 ("for(let i=0;i<NV;i++){ if(Math.random()<0.35) continue;", "for(let i=0;i<NV;i++){ if(Math.random()<(LITE?0.75:0.35)) continue;"),
 ("if(y<0.3||Math.random()<0.8) continue;", "if(y<0.3||Math.random()<(LITE?0.95:0.8)) continue;"),
 ("if(Math.abs(x)<0.5||y>0.0||Math.random()<0.86) continue;", "if(Math.abs(x)<0.5||y>0.0||Math.random()<(LITE?0.97:0.86)) continue;"),
 ("scene.add(new THREE.Points(terGeo,terMat));", "if(!LITE) scene.add(new THREE.Points(terGeo,terMat));"),
 ("scene.add(new THREE.LineSegments(terLineGeo,terLineMat));", "if(!LITE) scene.add(new THREE.LineSegments(terLineGeo,terLineMat));"),
 ("scene.add(new THREE.Points(rivGeo,rivMat));", "if(!LITE) scene.add(new THREE.Points(rivGeo,rivMat));"),
 ("scene.add(new THREE.Points(dustGeo,dustMat));", "if(!LITE) scene.add(new THREE.Points(dustGeo,dustMat));"),
 ("composite(); requestAnimationFrame(tick);", "if(LITE){ renderer.setRenderTarget(null); renderer.clear(); renderer.render(scene,camera); } else composite(); requestAnimationFrame(tick);"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'window.FB_LITE' in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if a not in s: sys.exit(f+': anchor not found: '+a[:50])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n,'places')
