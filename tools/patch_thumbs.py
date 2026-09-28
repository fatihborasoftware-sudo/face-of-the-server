#!/usr/bin/env python3
# patch_thumbs.py - shows each crew member's ID card as a small thumbnail next to their node on the Command Map (map.html).
# The thumbnails are embedded (webp, ~7 KB each) so the page stays self-contained. Idempotent. Usage: python3 patch_thumbs.py map.html
import sys, json, os
T=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'thumbs.json')))
KEEP=['serra','watchman','locke','corren','quill','dusk','relay','mason']
CSS=""".node .thumb{position:absolute;top:calc(50% - 30px);width:64px;height:96px;object-fit:cover;border-radius:5px;opacity:.9;box-shadow:0 0 16px rgba(0,0,0,.85),0 0 10px color-mix(in srgb,var(--c) 45%,transparent);transition:transform .25s,opacity .25s,box-shadow .25s;transform-origin:center;z-index:2}
  .node.left .thumb{left:calc(100% + 14px)}
  .node:not(.left) .thumb{right:calc(100% + 14px)}
  .node.top .thumb{top:calc(50% + 24px)}
  .node.top.left .thumb{left:auto;right:-19px}
  .node.top:not(.left) .thumb{right:auto;left:-19px}
  .node:hover .thumb{opacity:1;transform:scale(1.6);z-index:5}
  .node.talk .thumb{opacity:1;transform:scale(1.2);box-shadow:0 0 22px var(--c),0 0 40px color-mix(in srgb,var(--c) 50%,transparent)}
  @media (max-width:900px){.node .thumb{width:44px;height:66px;top:calc(50% - 20px)}}
"""
R=[
 ("</style>", CSS+"</style>"),
 ("  const N=[\n", "  const THUMBS="+json.dumps({k:T[k] for k in KEEP},separators=(',',':'))+";\n  const N=[\n"),
 ("d.innerHTML='<span class=\"ring\"></span><span class=\"lbl\">'+n.name+'</span>';",
  "d.innerHTML='<span class=\"ring\"></span><span class=\"lbl\">'+n.name+'</span>'; if(!n.app&&n.spk&&THUMBS[n.spk[0]]){ const im=document.createElement('img'); im.className='thumb'; im.alt=''; im.src=THUMBS[n.spk[0]]; d.appendChild(im); if(n.y<0.2) d.classList.add('top'); }"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'const THUMBS=' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:50])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
