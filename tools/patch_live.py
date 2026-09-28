#!/usr/bin/env python3
# patch_live.py - LIVE mode: everything the intro does (left title, transcript captions that materialise word by
# word, camera push-in, dimmed dashboard) now happens whenever Khoa speaks or a situation changes, not only in the
# intro. Also polls the khoa-tts queue (/queue) so lines pushed on the server with `khoa say "..."` are spoken
# here, with optional situation / title. Idempotent.
import sys
CSS = ("  body.live .bar,body.live .hud,body.live #status,body.live .gaze,body.live #sl,body.live #fbpanels-b{opacity:.18!important;transition:opacity 1s} body.live .caption{opacity:0!important}\n"
       "  body.live #cine .ttl b{font-size:34px} #cine .ttl b{transition:font-size .6s}\n")
LIVE = r"""  // ---------- LIVE: the intro's treatment for everyday speech and situation changes
  const rawSay=window.fbSay, rawSit=window.fbSituation; let inCap=false, liveT=0, ttlT=0;
  const liveOn=()=>{ clearTimeout(liveT); if(running) return; document.body.classList.add('live'); window.fbCamZoom=1.12; window.fbCamLookY=-0.22; };
  const liveOff=()=>{ if(running) return; document.body.classList.remove('live'); window.fbCamZoom=1; window.fbCamLookY=-0.45; ttl.classList.remove('on'); };
  const titleL=(a,c)=>{ ttlT=performance.now(); title(a,c); };
  const sitTitle=name=>{ const st=STEPS.find(s=>s[0]===name); return st?[st[1],st[2]]:(name&&name!=='normal'?[name.toUpperCase(),'SITUATION']:['KHOA','THE FACE OF THE SERVER']); };
  window.fbLive=async function(text,o){ o=o||{}; if(!text) return; if(running||inCap||o.nocine) return rawSay(text,o); if(window.fbMuted&&window.fbMuted()&&!o.force) return;
    liveOn(); if(o.title||performance.now()-ttlT>1500){ const [a,c]=sitTitle(window.fbSit&&window.fbSit.name); titleL(o.title||a,o.sub||c); }
    inCap=true; try{ await say(text); } finally{ inCap=false; } clearTimeout(liveT); liveT=setTimeout(liveOff,2600); };
  window.fbSay=function(t,o){ return window.fbLive(t,o); };
  window.fbSituation=function(name,o){ rawSit(name,o); if(running||(o&&o.quiet)) return; const isLive=document.body.classList.contains('live');
    if(name!=='normal'){ liveOn(); const [a,c]=sitTitle(name); if(performance.now()-ttlT>1500) titleL(a,c); clearTimeout(liveT); liveT=setTimeout(liveOff,7000); }
    else if(isLive){ titleL('ALL SYSTEMS NOMINAL','KHOA &middot; THE FACE OF THE SERVER'); clearTimeout(liveT); liveT=setTimeout(liveOff,4000); } };
  // ---------- QUEUE: lines pushed on the server (khoa say "...") are spoken here
  let qLast=-1, qPend=[];
  setInterval(async()=>{ try{ if(window.fbTTS){ const r=await fetch(window.fbTTS+'queue?since='+Math.max(0,qLast),{cache:'no-store'}); if(r.ok){ const items=await r.json();
      if(qLast<0) qLast=items.reduce((m,i)=>Math.max(m,i.id),0); else for(const it of items){ if(it.id>qLast){ qLast=it.id; qPend.push(it); } } } } }catch(e){}
    if(qPend.length&&!inCap&&!running){ const it=qPend.shift(); if(window.fbTouch) window.fbTouch(); if(it.sit){ const q=window.fbIntroQuiet; if(it.text) window.fbIntroQuiet=true; window.fbSituation(it.sit,it.value!=null?{value:it.value}:undefined); window.fbIntroQuiet=q; } if(it.text) window.fbLive(it.text,{title:it.title||undefined,sub:it.sub||undefined}); } },1500);
"""
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "window.fbLive=" in s: print(f,'already patched'); continue
    a="#cine .sub{display:flex;flex-direction:column-reverse;justify-content:flex-end} #cine .sn{display:none}"
    if s.count(a)!=1: sys.exit(f+': css anchor not found')
    s=s.replace(a,CSS.strip()+"\n  "+a,1)
    a="  window.fbIntro=async function(){"
    if s.count(a)!=1: sys.exit(f+': intro anchor not found')
    s=s.replace(a,LIVE+a,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
