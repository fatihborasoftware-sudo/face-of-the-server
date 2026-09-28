#!/usr/bin/env python3
# patch_intro2.py - intro captions: Impact font, words pop in one by one in time with the voice; no scene shrink;
# thin top bar so the head is never cut. Applies after patch_intro.py. Idempotent.
import sys
R=[
 ("body.cine #cine .bt,body.cine #cine .bb{height:9vh}", "body.cine #cine .bt{height:3vh} body.cine #cine .bb{height:11vh}"),
 ("#stage,#fx{transition:transform 1.4s ease;transform-origin:50% 52%} body.cine #stage,body.cine #fx{transform:scale(0.84)}", "body.cine #fx{transform:translateY(-2vh)}"),
 ("#cine .sub{position:absolute;left:50%;bottom:1.6vh;transform:translateX(-50%);max-width:72vw;text-align:center;font:600 20px/1.5 \"IBM Plex Mono\",ui-monospace,monospace;color:#e8f4ff;letter-spacing:.06em;text-shadow:0 0 12px #000,0 0 30px #6fdcff66;opacity:0;transition:opacity .4s} #cine .sub.on{opacity:1}",
  "#cine .sub{position:absolute;left:50%;bottom:2.2vh;transform:translateX(-50%);width:86vw;text-align:center;font:400 34px/1.2 Impact,'Arial Narrow Bold','Franklin Gothic Medium',sans-serif;color:#fff;letter-spacing:.04em;text-transform:uppercase;opacity:0;transition:opacity .3s} #cine .sub.on{opacity:1}\n  #cine .sub span{display:inline-block;margin:0 .18em;opacity:0;transform:scale(1.8) translateY(6px);text-shadow:0 0 14px var(--sc,#6fdcff),0 2px 0 #000} #cine .sub span.on{animation:wpop .28s cubic-bezier(.2,1.4,.4,1) forwards}\n  @keyframes wpop{0%{opacity:0;transform:scale(1.8) translateY(6px)}60%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:none}}\n  @media (max-width:900px){#cine .sub{font-size:20px}}"),
 ("const say=t=>new Promise(res=>{ let done=false; const fin=()=>{ if(!done){ done=true; sub.classList.remove('on'); res(); } }; window.fbSayDone=fin; sub.textContent=t; sub.classList.add('on'); window.fbSay(t,{force:true}); setTimeout(fin,600+t.split(/\\s+/).length*560); const iv=setInterval(()=>{ if(abort){ clearInterval(iv); fin(); } },100); });",
  "const say=t=>new Promise(res=>{ let done=false; const words=t.split(/\\s+/); sub.innerHTML=words.map(w=>'<span>'+w.replace(/</g,'&lt;')+'</span>').join(' '); const sp=[...sub.querySelectorAll('span')]; sub.classList.add('on');\n    const fin=()=>{ if(!done){ done=true; clearInterval(iv); sub.classList.remove('on'); res(); } }; window.fbSayDone=fin; window.fbSay(t,{force:true}); const t0=performance.now(); let shown=0;\n    const iv=setInterval(()=>{ if(abort){ fin(); return; } const a=window.fbAudio; let p; if(a&&a.duration&&!a.paused){ p=a.currentTime/a.duration; } else p=(performance.now()-t0)/(400+words.length*430); const n=Math.min(words.length,Math.floor(p*words.length+0.6)); while(shown<n){ sp[shown].classList.add('on'); shown++; } },40);\n    setTimeout(fin,1500+words.length*600); });"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'wpop' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
