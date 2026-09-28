#!/usr/bin/env python3
# patch_cardside.py - when a node is clicked, the info panel opens with the member's ID card (PNG) standing beside it.
# Idempotent. Usage: python3 patch_cardside.py map.html
import sys
CSS=""".card .side{position:absolute;top:0;width:150px;height:210px;object-fit:cover;border-radius:8px;box-shadow:0 0 22px rgba(0,0,0,.9),0 0 26px var(--c);animation:pop .25s ease-out}
  .card.side-r .side{left:calc(100% + 16px)}
  .card.side-l .side{right:calc(100% + 16px)}
  @media (max-width:900px){.card .side{display:none}}
"""
R=[
 ("</style>", CSS+"</style>"),
 ("card.innerHTML=(n._img?`<div class=\"idc\"><img src=\"${n._img}\" alt=\"\" onerror=\"this.parentNode.remove()\"></div>`:'')+",
  "card.classList.toggle('side-r',n.x<0.5); card.classList.toggle('side-l',n.x>=0.5); const sideSrc=(!n.app&&n.spk)?root+'crew/card-'+n.spk[0]+'.png':''; card.innerHTML=(sideSrc?`<img class=\"side\" src=\"${sideSrc}\" alt=\"\" onerror=\"if(window.THUMBS&&THUMBS['${n.spk[0]}']&&this.src!==THUMBS['${n.spk[0]}'])this.src=THUMBS['${n.spk[0]}'];else this.remove()\">`:'')+(n._img?`<div class=\"idc\"><img src=\"${n._img}\" alt=\"\" onerror=\"this.parentNode.remove()\"></div>`:'')+"),
 ("  const THUMBS=", "  window.THUMBS="),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'class="side"' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:60])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
