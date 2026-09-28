#!/usr/bin/env python3
# patch_plain.py - Face page only: no background twinkles (dust, particle landscape, rivers) - just the body.
# Idempotent. Usage: python3 patch_plain.py face.html / index.html
import sys
R=[("if(!LITE) scene.add(new THREE.Points(terGeo,terMat));","if(false) scene.add(new THREE.Points(terGeo,terMat));"),
   ("if(!LITE) scene.add(new THREE.LineSegments(terLineGeo,terLineMat));","if(false) scene.add(new THREE.LineSegments(terLineGeo,terLineMat));"),
   ("if(!LITE) scene.add(new THREE.Points(rivGeo,rivMat));","if(false) scene.add(new THREE.Points(rivGeo,rivMat));"),
   ("if(!LITE) scene.add(new THREE.Points(dustGeo,dustMat));","if(false) scene.add(new THREE.Points(dustGeo,dustMat));")]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "if(false) scene.add(new THREE.Points(dustGeo" in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:50])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
# second step: hide the vitals overlays (storage panel, rings, heart/ECG, net line) - just the body
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if '.vt{display:none!important}' in s: print(f,'overlays already hidden'); continue
    if s.count('</style>')!=1: sys.exit(f+': style anchor')
    s=s.replace('</style>','  .vt{display:none!important} /* Face panel: body only */\n</style>',1)
    open(f,'w',encoding='utf-8').write(s); print(f,'overlays hidden')
