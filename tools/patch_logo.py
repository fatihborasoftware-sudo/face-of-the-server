#!/usr/bin/env python3
# patch_logo.py - replaces the "FBSERVER" text in the top-left corner with the FB Server logo (embedded webp).
# Idempotent. Usage: python3 patch_logo.py face.html map.html
import sys, os
B64=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'logo.b64')).read().strip()
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'class="logo"' in s: print(f,'already patched'); continue
    a='<div class="hud"><div class="name">FBSERVER</div>'
    if s.count(a)!=1: sys.exit(f+': hud anchor not found once')
    s=s.replace(a,'<div class="hud"><img class="logo" alt="FB Server" src="'+B64+'">',1)
    s=s.replace('</style>','  .hud .logo{display:block;height:44px;width:auto;margin:-6px 0 4px -2px;filter:drop-shadow(0 0 10px rgba(80,170,255,.45))}\n  @media (max-width:900px){.hud .logo{height:30px}}\n</style>',1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
