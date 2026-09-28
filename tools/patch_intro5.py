#!/usr/bin/env python3
# patch_intro5.py - intro captions: under the left title (left-aligned block, width 34vw), and words no longer pop:
# each word materialises sci-fi style - blurred, wide-tracked and dim, then focuses, tightens and lights up
# (0.7 s ease-out); sentences dissolve in the same way. Idempotent.
import sys
R=[
 ("#cine .sub{position:absolute;left:50%;bottom:1.2vh;transform:translateX(-50%);width:70vw;text-align:center;font:400 34px/1.2 Impact,",
  "#cine .sub{position:absolute;left:6vw;top:calc(14vh + 118px);width:34vw;text-align:left;font:400 30px/1.25 Impact,"),
 ("#cine .sub span{display:inline-block;margin:0 .18em;opacity:0;transform:scale(1.8) translateY(6px);text-shadow:0 0 18px var(--sc,#6fdcff),0 0 6px #000,0 0 28px #000,0 2px 0 #000} #cine .sub span.on{animation:wpop .28s cubic-bezier(.2,1.4,.4,1) forwards}",
  "#cine .sub span{display:inline-block;margin:0 .14em;opacity:0;text-shadow:0 0 18px var(--sc,#6fdcff),0 0 6px #000,0 0 28px #000,0 2px 0 #000} #cine .sub span.on{animation:wfade .7s cubic-bezier(.2,.7,.2,1) forwards}"),
 ("@keyframes wpop{0%{opacity:0;transform:scale(1.8) translateY(6px)}60%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:none}}",
  "@keyframes wfade{0%{opacity:0;filter:blur(8px) brightness(2.5);letter-spacing:.3em;transform:translateY(4px)}55%{opacity:1;filter:blur(1px) brightness(1.6)}100%{opacity:1;filter:none;letter-spacing:.04em;transform:none}}"),
 ("@keyframes snin{0%{opacity:0;transform:translateY(10px)}100%{opacity:1;transform:none}}",
  "@keyframes snin{0%{opacity:0;filter:blur(6px);transform:translateX(-14px)}100%{opacity:1;filter:none;transform:none}}"),
 ("#cine .sn{display:none} #cine .sn.on{display:block;animation:snin .35s ease-out}",
  "#cine .sn{display:none} #cine .sn.on{display:block;animation:snin .6s cubic-bezier(.2,.7,.2,1)}"),
 ("@media (max-width:900px){#cine .ttl b{font-size:24px} #cine .sub{font-size:14px}}",
  "@media (max-width:900px){#cine .ttl b{font-size:24px} #cine .sub{font-size:14px;top:calc(14vh + 76px);width:60vw}}"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "@keyframes wfade" in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:60])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
