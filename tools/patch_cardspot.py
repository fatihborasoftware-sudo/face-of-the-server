#!/usr/bin/env python3
# patch_cardspot.py - the speaking agent's ID card pops up in a fixed spot: left of the figure for agents on the
# left half of the map, right of the figure for agents on the right half (big card, as in the mockup).
# Applies on top of patch_cardpop.py. Idempotent. Usage: python3 patch_cardspot.py map.html
import sys
CSS="""  .spot{position:fixed;top:49vh;height:min(38vh,320px);aspect-ratio:3/4;transform:translate(-50%,-50%) scale(.6);object-fit:cover;border-radius:10px;opacity:0;display:none;box-shadow:0 0 30px rgba(0,0,0,.9),0 0 40px var(--c,#6fdcff);transition:opacity .35s,transform .5s cubic-bezier(.2,1.4,.4,1);z-index:6;pointer-events:none}
  .spot.L{left:26vw} .spot.R{left:73vw}
  .spot.on{display:block;opacity:1;transform:translate(-50%,-50%) scale(1)}
  @media (max-width:900px){.spot{height:26vh}.spot.L{left:22vw}.spot.R{left:78vw}}
"""
R=[
 ("</style>", CSS+"</style>"),
 ("  const els=[];\n", "  const els=[];\n  const spotL=document.createElement('img'), spotR=document.createElement('img'); spotL.className='spot L'; spotR.className='spot R'; spotL.alt=spotR.alt=''; map.appendChild(spotL); map.appendChild(spotR);\n  function showSpot(n){ const im=n.x<0.5?spotL:spotR, key=n.spk[0], src=root+'crew/card-'+key+'.png'; im.style.setProperty('--c',n.c); im.onerror=()=>{ if(window.THUMBS&&THUMBS[key]&&im.src!==THUMBS[key]) im.src=THUMBS[key]; }; if(im.getAttribute('src')!==src) im.src=src; (n.x<0.5?spotR:spotL).classList.remove('on'); im.classList.remove('on'); void im.offsetWidth; im.classList.add('on'); }\n  function hideSpots(){ spotL.classList.remove('on'); spotR.classList.remove('on'); }\n"),
 ("const im=d.querySelector('.pop'); if(im){ if(!im.getAttribute('src')) im.src=root+'crew/card-'+n.spk[0]+'.png'; d.classList.add('pop-on'); } else open(n,d);",
  "if(!n.app&&n.spk) showSpot(n); else open(n,d);"),
 ("e.classList.remove('pop-on');});", "e.classList.remove('pop-on');}); hideSpots();"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'function showSpot' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:60])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
