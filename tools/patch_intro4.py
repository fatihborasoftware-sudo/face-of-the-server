#!/usr/bin/env python3
# patch_intro4.py - intro: no letterbox bars at all (nothing of Khoa is cut); captions float over the lower body
# with a dark halo so they read against the particles; PANELS switch hidden during the intro. Idempotent.
import sys
R=[
 ("body.cine #cine .bt{height:0} body.cine #cine .bb{height:11vh}",
  "body.cine #cine .bt{height:0} body.cine #cine .bb{height:0}"),
 ("#cine .sub{position:absolute;left:50%;bottom:2.2vh;transform:translateX(-50%);width:86vw;",
  "#cine .sub{position:absolute;left:50%;bottom:1.2vh;transform:translateX(-50%);width:70vw;"),
 ("text-shadow:0 0 14px var(--sc,#6fdcff),0 2px 0 #000}",
  "text-shadow:0 0 18px var(--sc,#6fdcff),0 0 6px #000,0 0 28px #000,0 2px 0 #000}"),
 ("body.cine .bar,body.cine .hud,body.cine #status,",
  "body.cine .bar,body.cine .hud,body.cine #status,body.cine #fbpanels-b,body.cine #fbpanels-m,"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "body.cine #cine .bb{height:0}" in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:60])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
