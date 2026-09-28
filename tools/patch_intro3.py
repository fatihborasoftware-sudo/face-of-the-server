#!/usr/bin/env python3
# patch_intro3.py - intro polish: no top bar, Khoa framed bigger (camera moves in, head kept in frame), captions one
# short sentence at a time (words still pop with the voice), and the server voice is used from any origin.
import sys
NEW_SAY="""const say=t=>new Promise(res=>{ let done=false; const sents=t.split(/(?<=[.!?])\\s+/); const words=[]; sents.forEach((sn,si)=>sn.split(/\\s+/).forEach(w=>words.push([si,w])));
    sub.innerHTML=sents.map((sn,si)=>'<div class="sn" data-i="'+si+'">'+sn.split(/\\s+/).map(w=>'<span>'+w.replace(/</g,'&lt;')+'</span>').join(' ')+'</div>').join(''); const sp=[...sub.querySelectorAll('span')], sn=[...sub.querySelectorAll('.sn')]; sub.classList.add('on'); let curS=-1;
    const fin=()=>{ if(!done){ done=true; clearInterval(iv); sub.classList.remove('on'); res(); } }; window.fbSayDone=fin; window.fbSay(t,{force:true}); const t0=performance.now(); let shown=0;
    const iv=setInterval(()=>{ if(abort){ fin(); return; } const a=window.fbAudio; let p; if(a&&a.duration&&!a.paused){ p=a.currentTime/a.duration; } else p=(performance.now()-t0)/(400+words.length*430); const n=Math.min(words.length,Math.floor(p*words.length+0.6)); while(shown<n){ const [si]=words[shown]; if(si!==curS){ curS=si; sn.forEach((d,k)=>d.classList.toggle('on',k===si)); } sp[shown].classList.add('on'); shown++; } },40);
    setTimeout(fin,1500+words.length*600); });"""
R=[
 ("body.cine #cine .bt{height:3vh} body.cine #cine .bb{height:11vh}", "body.cine #cine .bt{height:0} body.cine #cine .bb{height:11vh}"),
 ("body.cine #fx{transform:translateY(-2vh)}", "#cine .sn{display:none} #cine .sn.on{display:block;animation:snin .35s ease-out}\n  @keyframes snin{0%{opacity:0;transform:translateY(10px)}100%{opacity:1;transform:none}}"),
 ("camera.lookAt(0,-0.45,0);\n", "{ const zt=window.fbCamZoom||1, lt=window.fbCamLookY!=null?window.fbCamLookY:-0.45; const zb=innerWidth<700?9.2:6.9; camera.position.z+=(zb/zt-camera.position.z)*Math.min(1,dt*1.5); camLook+=(lt-camLook)*Math.min(1,dt*1.5); } camera.lookAt(0,camLook,0);\n"),
 ("let sitA=0, lastTouch=performance.now(), asleep=false,", "let camLook=-0.45, sitA=0, lastTouch=performance.now(), asleep=false,"),
 ("window.fbTTS=location.protocol==='https:'?'/khoa/':('http://'+location.hostname+':8082/');",
  "window.fbTTS=(location.protocol==='https:'&&/^(192\\.168\\.1\\.146|fbserver(\\.local)?)$/.test(location.hostname))?'/khoa/':(/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname)?'http://127.0.0.1:8082/':'https://192.168.1.146/khoa/');"),
 ("document.body.classList.add('cine'); window.fbIntroQuiet=true;", "document.body.classList.add('cine'); window.fbIntroQuiet=true; window.fbCamZoom=1.22; window.fbCamLookY=-0.02;"),
 ("document.body.classList.remove('cine'); ttl.classList.remove('on');", "document.body.classList.remove('cine'); window.fbCamZoom=1; window.fbCamLookY=-0.45; ttl.classList.remove('on');"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fbCamZoom' in s: print(f,'already patched'); continue
    i=s.find("const say=t=>new Promise(res=>{ let done=false; const words=t.split"); j=s.find("setTimeout(fin,1500+words.length*600); });",i)
    if i<0 or j<0: sys.exit(f+': say block not found')
    s=s[:i]+NEW_SAY+s[j+len("setTimeout(fin,1500+words.length*600); });"):]
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
