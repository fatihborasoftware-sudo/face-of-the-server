#!/usr/bin/env python3
# patch_intro6.py - intro captions as a transcript: the sentence being spoken materialises at the TOP, the sentences
# already spoken stay underneath (smaller, dimmed) so the viewer can read the whole text; cleared per step. Idempotent.
import sys
R=[
 ("sn.forEach((d,k)=>d.classList.toggle('on',k===si));",
  "sn.forEach((d,k)=>{ d.classList.toggle('on',k<=si); d.classList.toggle('done',k<si); });"),
 ("#cine .sn{display:none} #cine .sn.on{display:block;animation:snin .6s cubic-bezier(.2,.7,.2,1)}",
  "#cine .sub{display:flex;flex-direction:column-reverse;justify-content:flex-end} #cine .sn{display:none} #cine .sn.on{display:block;animation:snin .6s cubic-bezier(.2,.7,.2,1)} #cine .sn.done{opacity:.42;font-size:.7em;margin-top:.35em;transition:opacity .8s,font-size .8s} #cine .sn.done span{text-shadow:0 0 6px #000,0 2px 0 #000}"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "#cine .sn.done" in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:60])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
