#!/usr/bin/env python3
import sys
R=[("const nx=(0.5-face.x)*2.4, ny=(face.y-0.5)*2.2;","const nx=(0.5-face.x)*3.6, ny=(face.y-0.5)*3.2;"),
("    btn.classList.add('on'); btn.textContent='◉ CAMERA ON';","    window.fbCamOn=true; btn.classList.add('on'); btn.textContent='◉ CAMERA ON';"),
("  function stop(){ clearInterval(timer); timer=0;","  function stop(){ window.fbCamOn=false; clearInterval(timer); timer=0;"),
("addEventListener('pointermove',e=>setTargetFromScreen((e.clientX/innerWidth)*2-1,(e.clientY/innerHeight)*2-1));","addEventListener('pointermove',e=>{ if(window.fbCamOn) return; setTargetFromScreen((e.clientX/innerWidth)*2-1,(e.clientY/innerHeight)*2-1); });"),
("document.getElementById('gaze').textContent=idle?'LOOKING AT · AROUND THE ROOM':'LOOKING AT · YOU (MOUSE)';","if(!window.fbCamOn) document.getElementById('gaze').textContent=idle?'LOOKING AT · AROUND THE ROOM':'LOOKING AT · YOU (MOUSE)';")]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fbCamOn' in s: print(f,'already'); continue
    n=0
    for a,b in R:
        if a not in s: sys.exit(f+': anchor missing: '+a[:40])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
