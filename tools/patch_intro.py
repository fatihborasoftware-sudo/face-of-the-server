#!/usr/bin/env python3
# patch_intro.py - INTRO: a cinematic self-presentation. Khoa assembles, introduces FB Server and walks through
# every situation with narration, letterbox bars, titles and subtitles. Button in the bar; Escape stops it.
import sys
CSS="""  #cine{position:fixed;inset:0;pointer-events:none;z-index:40}
  #cine .bt,#cine .bb{position:absolute;left:0;right:0;height:0;background:#000;transition:height 1.2s ease} #cine .bt{top:0} #cine .bb{bottom:0}
  body.cine #cine .bt,body.cine #cine .bb{height:9vh}
  #cine .sub{position:absolute;left:50%;bottom:1.6vh;transform:translateX(-50%);max-width:72vw;text-align:center;font:600 20px/1.5 "IBM Plex Mono",ui-monospace,monospace;color:#e8f4ff;letter-spacing:.06em;text-shadow:0 0 12px #000,0 0 30px #6fdcff66;opacity:0;transition:opacity .4s} #cine .sub.on{opacity:1}
  #cine .ttl{position:absolute;left:6vw;top:14vh;opacity:0} #cine .ttl.on{animation:ttlin 1.2s cubic-bezier(.2,.8,.2,1) forwards}
  #cine .ttl b{display:block;font:400 42px/1.1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.3em;color:#fff;text-shadow:0 0 20px var(--sc,#6fdcff)} #cine .ttl i{display:block;font:11px/2 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.35em;color:var(--sc,#6fdcff);font-style:normal;margin-top:6px}
  @keyframes ttlin{0%{opacity:0;transform:translateX(-30px);filter:blur(6px)}100%{opacity:1;transform:none;filter:none}}
  body.cine .bar,body.cine .hud,body.cine #status,body.cine .gaze,body.cine #sitban,body.cine #sl,body.cine .caption{opacity:0!important;transition:opacity .8s}
  #stage,#fx{transition:transform 1.4s ease;transform-origin:50% 52%} body.cine #stage,body.cine #fx{transform:scale(0.84)}
  @media (max-width:900px){#cine .ttl b{font-size:24px} #cine .sub{font-size:14px}}
"""
JS=r"""<script>
// ---------- INTRO: Khoa presents the server (cinematic run through all situations)
(() => {
  const bar=document.querySelector('.bar'); if(!bar) return;
  const b=document.createElement('button'); b.id='intro'; b.innerHTML='&#9654; INTRO'; bar.insertBefore(b,document.getElementById('sitb')||document.getElementById('stop'));
  const box=document.createElement('div'); box.id='cine'; box.innerHTML='<div class="bt"></div><div class="bb"></div><div class="sub"></div><div class="ttl"></div>'; document.body.appendChild(box);
  const sub=box.querySelector('.sub'), ttl=box.querySelector('.ttl');
  let running=false, abort=false;
  const wait=ms=>new Promise(r=>{ const t0=performance.now(); const iv=setInterval(()=>{ if(abort||performance.now()-t0>=ms){ clearInterval(iv); r(); } },50); });
  const say=t=>new Promise(res=>{ let done=false; const fin=()=>{ if(!done){ done=true; sub.classList.remove('on'); res(); } }; window.fbSayDone=fin; sub.textContent=t; sub.classList.add('on'); window.fbSay(t,{force:true}); setTimeout(fin,600+t.split(/\s+/).length*560); const iv=setInterval(()=>{ if(abort){ clearInterval(iv); fin(); } },100); });
  const title=(a,c)=>{ ttl.innerHTML='<b>'+a+'</b><i>'+(c||'')+'</i>'; ttl.classList.remove('on'); void ttl.offsetWidth; ttl.classList.add('on'); };
  const STEPS=[
    ['backup','BACKUP','EVERY NIGHT  \u00b7  TO THE BACKUP DISK','When the backup runs, my veins turn green. Twenty eight gigabytes, every night, to the backup disk.'],
    ['heat','TEMPERATURE','THE PROCESSOR  \u00b7  WATCHED EVERY SECOND','When the processor runs hot, I burn with it. The fans answer. If it goes critical, I throttle.'],
    ['memory','MEMORY','SEVEN POINT TWO GIGABYTES','Memory pressure. When it fills, I swap to disk, and I tell you before it hurts.'],
    ['ssd','STORAGE','ONE TERABYTE  \u00b7  COUNTED','When the disk fills, I sink. Every gigabyte left is counted.'],
    ['load','LOAD','FOUR CORES','High load. All four cores busy. I hold steady.'],
    ['update','UPDATES','UNATTENDED  \u00b7  DAILY','Updates arrive quietly. I scan them in, package by package, and reboot when you allow it.'],
    ['alarm','SERVICES','TWELVE  \u00b7  ALWAYS RUNNING','If a service falls, I feel it. Nginx. Cockpit. The web. I name what is down.'],
    ['intrusion','INTRUSION','THE FIREWALL HOLDS','And if someone tries the door, I turn red. Every failed login is counted. The firewall holds.'],
  ];
  window.fbIntro=async function(){ if(running){ abort=true; return; } running=true; abort=false; document.body.classList.add('cine'); window.fbIntroQuiet=true;
    try{ window.fbSituation('normal'); try{ speechSynthesis.cancel(); }catch(e){} if(window.fbAudio){ try{ window.fbAudio.pause(); }catch(e){} }
      window.fbTouch&&window.fbTouch(); document.getElementById('assemble').click();
      title('FB SERVER','LENOVO IDEAPAD  \u00b7  UBUNTU  \u00b7  HOME OF THE CREW'); await wait(7600); if(abort) return;
      await say('I am Khoa. The face of the server.'); if(abort) return;
      await say('This machine is F B Server. A Lenovo IdeaPad running Ubuntu, kept alive by a crew of eight agents. I am its body. Let me show you what I watch.');
      for(const [k,t1,t2,line] of STEPS){ if(abort) break; window.fbSituation(k); title(t1,t2); await wait(1400); await say(line); await wait(1600); }
      if(abort) return;
      window.fbSituation('normal'); title('ALL SYSTEMS NOMINAL','KHOA  \u00b7  THE FACE OF THE SERVER'); await wait(1200);
      await say('Situation cleared. All systems nominal. This is F B Server. I am Khoa, and I am watching.'); await wait(1800);
    } finally { window.fbIntroQuiet=false; if(abort){ window.fbSituation('normal'); try{ if(window.fbAudio) window.fbAudio.pause(); }catch(e){} } document.body.classList.remove('cine'); ttl.classList.remove('on'); sub.classList.remove('on'); running=false; abort=false; } };
  b.onclick=e=>{ e.stopPropagation(); window.fbIntro(); };
  addEventListener('keydown',e=>{ if(e.key==='Escape'&&running) abort=true; });
})();
</script>
"""
R=[
 ("</style>", CSS+"</style>"),
 ("const say=SAY[name]; if(say) setTimeout(", "const say=SAY[name]; if(say&&!window.fbIntroQuiet) setTimeout("),
 ("const done=()=>{ pulses=[]; setState('idle');", "const done=()=>{ if(window.fbSayDone){ const f=window.fbSayDone; window.fbSayDone=null; f(); } pulses=[]; setState('idle');"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fbIntro' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:60])
        s=s.replace(a,b,1)
    s=s.replace('</body>',JS+'</body>',1) if '</body>' in s else s.rstrip('\n')+'\n'+JS
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
