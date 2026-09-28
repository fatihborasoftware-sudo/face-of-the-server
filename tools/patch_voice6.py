#!/usr/bin/env python3
# patch_voice6.py - voice fixes: no "Back..." line while the intro (or a situation) runs; a newer line cancels an
# older one that is still being fetched (no overlapping voices / wrong voice).
import sys
R=[
 ("let firstWake=true; window.fbOnWake=function(){", "let firstWake=true; window.fbOnWake=function(){ if(window.fbIntroQuiet||window.fbSit) return;"),
 ("const ctrl=new AbortController(), tm=setTimeout(()=>ctrl.abort(),8000);", "const my=(window.fbSayId=(window.fbSayId||0)+1); const ctrl=new AbortController(), tm=setTimeout(()=>ctrl.abort(),8000);"),
 (".then(r=>{ clearTimeout(tm); if(!r.ok) throw 0; return r.blob(); }).then(b=>{\n      const a=new Audio(URL.createObjectURL(b));", ".then(r=>{ clearTimeout(tm); if(!r.ok) throw 0; return r.blob(); }).then(b=>{ if(my!==window.fbSayId) return;\n      const a=new Audio(URL.createObjectURL(b));"),
 ("}).catch(()=>{ clearTimeout(tm); browserSay(); }); };", "}).catch(()=>{ clearTimeout(tm); if(my===window.fbSayId) browserSay(); }); };"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fbSayId' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
