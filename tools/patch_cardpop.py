#!/usr/bin/env python3
# patch_cardpop.py - when a crew member speaks, their ID card (PNG from crew/card-<name>.png) pops up next to their node
# instead of the big info panel. Clicking a node by hand still opens the panel. Replaces the always-on thumbnails
# of patch_thumbs.py if present. Idempotent. Usage: python3 patch_cardpop.py map.html
import sys, json, os, re
_tj=os.path.join(os.path.dirname(os.path.abspath(__file__)),'thumbs.json')
T=json.load(open(_tj)) if os.path.exists(_tj) else {}
KEEP=['serra','watchman','locke','corren','quill','dusk','relay','mason']
CSS=""".node .pop{position:absolute;top:calc(50% - 34px);width:96px;height:136px;object-fit:cover;border-radius:6px;display:none;opacity:0;transform:scale(.6);transform-origin:center;box-shadow:0 0 18px rgba(0,0,0,.9),0 0 22px var(--c);transition:opacity .35s,transform .45s cubic-bezier(.2,1.4,.4,1);z-index:6;pointer-events:none}
  .node.left .pop{left:calc(100% + 16px)}
  .node:not(.left) .pop{right:calc(100% + 16px)}
  .node.top .pop{top:calc(50% + 26px)}
  .node.top.left .pop{left:auto;right:-35px}
  .node.top:not(.left) .pop{right:auto;left:-35px}
  .node.talk.pop-on .pop{display:block;opacity:1;transform:scale(1)}
  @media (max-width:900px){.node .pop{width:64px;height:90px;top:calc(50% - 22px)}}
"""
def unthumb(s):
    s=chr(10).join(l for l in s.split(chr(10)) if '.thumb' not in l)
    s=s.replace(" if(!n.app&&n.spk&&THUMBS[n.spk[0]]){ const im=document.createElement('img'); im.className='thumb'; im.alt=''; im.src=THUMBS[n.spk[0]]; d.appendChild(im); if(n.y<0.2) d.classList.add('top'); }","")
    s=re.sub(r"  const THUMBS=\{.*?\};\n","",s,flags=re.S)
    return s
R=[
 ("</style>", CSS+"</style>"),
 ("  const N=[\n", "  const THUMBS="+json.dumps({k:T[k] for k in KEEP if k in T},separators=(',',':'))+"; // small fallbacks for previews without a server\n  const N=[\n"),
 ("d.innerHTML='<span class=\"ring\"></span><span class=\"lbl\">'+n.name+'</span>';",
  "d.innerHTML='<span class=\"ring\"></span><span class=\"lbl\">'+n.name+'</span>'; if(!n.app&&n.spk){ const im=document.createElement('img'); im.className='pop'; im.alt=''; im.onerror=()=>{ if(THUMBS[n.spk[0]]&&im.src!==THUMBS[n.spk[0]]) im.src=THUMBS[n.spk[0]]; }; d.appendChild(im); if(n.y<0.2) d.classList.add('top'); }"),
 ("setTimeout(()=>{ if(talking===n) open(n,d); },160); },2600); }",
  "setTimeout(()=>{ if(talking!==n) return; const im=d.querySelector('.pop'); if(im){ if(!im.getAttribute('src')) im.src=root+'crew/card-'+n.spk[0]+'.png'; d.classList.add('pop-on'); } else open(n,d); },160); },2600); }"),
 ("talking=null; clearT=0; els.forEach(([m,e])=>{e.classList.remove('talk');e.classList.remove('hit');});",
  "talking=null; clearT=0; els.forEach(([m,e])=>{e.classList.remove('talk');e.classList.remove('hit');e.classList.remove('pop-on');});"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "im.className='pop'" in s: print(f,'already patched'); continue
    s=unthumb(s)
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:60])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
