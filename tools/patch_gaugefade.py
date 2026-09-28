#!/usr/bin/env python3
# patch_gaugefade.py - the big situation gauge fades out where it crosses Khoa's head: after the ring is drawn,
# a soft radial hole (destination-out) is punched around the projected head so the face stays in focus. Idempotent.
import sys
A="X.restore(); X.save(); X.globalAlpha=a; X.textAlign='center'; X.fillStyle=col; X.shadowColor=col; X.shadowBlur=18;"
B=("X.restore(); if(window.serraProject){ const h=window.serraProject(0,0.55,0), t=window.serraProject(0,1.0,0); const hr=Math.max(20,Math.hypot(t[0]-h[0],t[1]-h[1])); "
   "X.save(); X.globalCompositeOperation='destination-out'; const gr=X.createRadialGradient(h[0],h[1],hr*0.55,h[0],h[1],hr*1.75); gr.addColorStop(0,'rgba(0,0,0,1)'); gr.addColorStop(0.6,'rgba(0,0,0,0.75)'); gr.addColorStop(1,'rgba(0,0,0,0)'); "
   "X.fillStyle=gr; X.beginPath(); X.arc(h[0],h[1],hr*1.75,0,Math.PI*2); X.fill(); X.restore(); }\n"
   "    X.save(); X.globalAlpha=a; X.textAlign='center'; X.fillStyle=col; X.shadowColor=col; X.shadowBlur=18;")
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "destination-out" in s and "serraProject(0,0.55,0)" in s: print(f,'already patched'); continue
    if s.count(A)!=1: sys.exit(f+': anchor not found once')
    s=s.replace(A,B,1); open(f,'w',encoding='utf-8').write(s); print(f,'patched')
