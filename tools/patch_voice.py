#!/usr/bin/env python3
# patch_voice.py - gives the Face its own voice: "Khoa". window.fbSay(text) speaks with a deep English voice
# (pick with the VOICE button, remembered), and Khoa speaks by himself: when he comes online, on every situation,
# on the hour, and "welcome back" when the camera sees you again. Double-click QUIET to mute. Idempotent.
import sys
OLD="""  document.getElementById('speak').onclick=()=>{
    const text=LINES[li++%LINES.length];cap.textContent=text;setState('speaking');
    const ms=text.split(/\\s+/).length*340; pulses.push({t0:performance.now(),ms});
    try{ speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(text),vs=speechSynthesis.getVoices();
      const v=vs.find(v=>/en-GB/i.test(v.lang)&&/female|libby|sonia|hazel|serena|kate|susan/i.test(v.name))||vs.find(v=>/en-GB/i.test(v.lang)); if(v)u.voice=v; u.rate=0.98;
      u.onboundary=()=>{tgt=0.8+Math.random()*0.3;}; u.onend=()=>{pulses=[];setState('idle');setTimeout(()=>{if(mode==='idle')cap.textContent='';},1600);};
      speechSynthesis.speak(u);}catch(e){}
    setTimeout(()=>{try{if(!speechSynthesis.speaking)setState('idle');}catch(e){setState('idle');}},ms+300);
  };"""
NEW="""  // ---------- Khoa's voice
  const PREF=/Ryan|George|Daniel|Guy|Brian|Andrew|Christopher|Eric|Roger|Thomas|Arthur|Oliver|UK English Male|US English Male|Male/i;
  window.fbVoice=()=>{ let vs=[]; try{ vs=speechSynthesis.getVoices(); }catch(e){} let name=null; try{ name=localStorage.getItem('fbVoice'); }catch(e){}
    let v=name&&vs.find(x=>x.name===name); if(!v) v=vs.find(x=>/en-GB/i.test(x.lang)&&PREF.test(x.name)&&!/female/i.test(x.name))||vs.find(x=>/^en/i.test(x.lang)&&PREF.test(x.name)&&!/female/i.test(x.name))||vs.find(x=>/en-GB/i.test(x.lang))||vs.find(x=>/^en/i.test(x.lang)); return v||null; };
  window.fbMuted=()=>{ try{ return localStorage.getItem('fbMute')==='1'; }catch(e){ return false; } };
  window.fbSay=function(text,opts){ opts=opts||{}; if(!text) return; if(window.fbMuted()&&!opts.force) return;
    cap.textContent=text; setState('speaking'); const ms=text.split(/\\s+/).length*340; pulses.push({t0:performance.now(),ms});
    try{ speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(text); const v=window.fbVoice(); if(v) u.voice=v; u.rate=opts.rate||0.92; u.pitch=opts.pitch||0.72; u.volume=1;
      u.onboundary=()=>{tgt=0.8+Math.random()*0.3;}; u.onend=()=>{pulses=[];setState('idle');setTimeout(()=>{if(mode==='idle')cap.textContent='';},1600);};
      speechSynthesis.speak(u); }catch(e){}
    setTimeout(()=>{try{if(!speechSynthesis.speaking)setState('idle');}catch(e){setState('idle');}},ms+300); };
  document.getElementById('speak').onclick=()=>{ window.fbSay(LINES[li++%LINES.length],{force:true}); };
  // VOICE button: cycles through the English voices on this machine and says hello with each one
  { const bar=document.querySelector('.bar'); const vb=document.createElement('button'); vb.id='voice'; vb.textContent='\\u266a VOICE'; bar.insertBefore(vb,document.getElementById('stop'));
    vb.onclick=e=>{ e.stopPropagation(); let vs=[]; try{ vs=speechSynthesis.getVoices().filter(x=>/^en/i.test(x.lang)); }catch(e){} if(!vs.length){ window.fbSay('No voices found in this browser.',{force:true}); return; }
      const cur=window.fbVoice(); const i=(vs.indexOf(cur)+1)%vs.length; try{ localStorage.setItem('fbVoice',vs[i].name); }catch(e){}
      window.fbSay('This is Khoa, the face of the server. Voice: '+vs[i].name.replace(/Microsoft |Google |Online|\\(Natural\\)|- English.*$/g,'').trim()+'.',{force:true}); }; }
  { const stop=document.getElementById('stop'); const paint=()=>{ stop.textContent=window.fbMuted()?'\\u25a0 MUTED':'\\u25a0 QUIET'; stop.classList.toggle('on',window.fbMuted()); }; paint();
    stop.addEventListener('dblclick',e=>{ e.stopPropagation(); try{ localStorage.setItem('fbMute',window.fbMuted()?'0':'1'); }catch(e){} paint(); if(!window.fbMuted()) window.fbSay('Khoa back online.',{force:true}); }); }
  // what Khoa says by himself
  const numWord=n=>String(Math.round(n));
  window.fbStatusLine=function(){ const D=window.fbData; if(!D) return 'All systems nominal.'; const fs=(D.fs||[]).find(f=>f.mount==='/'); const parts=[];
    parts.push('CPU at '+numWord(D.cpu_pct||0)+' percent'); if(D.temp_c) parts.push('temperature '+numWord(D.temp_c)+' degrees'); if(fs) parts.push(numWord(fs.free/1073741824)+' gigabytes free');
    const lv=(window.fbStatus&&window.fbStatus.level)||'ok'; return parts.join(', ')+'. '+(lv==='ok'?'All systems nominal.':lv==='warn'?'Attention needed.':'Critical state.'); };
  let firstWake=true; window.fbOnWake=function(){ if(firstWake){ firstWake=false; window.fbSay('Khoa online. '+window.fbStatusLine()); } else window.fbSay('Back. '+window.fbStatusLine()); };
  const SAY={ normal:()=>'Situation cleared. All systems nominal.',
    backup:v=>'Backup running. 28 gigabytes to the backup disk.',
    intrusion:v=>'Intrusion detected. '+numWord(v)+' failed logins from 185 dot 220 dot 101 dot 7. Firewall holding.',
    heat:v=>'Warning. CPU temperature '+numWord(v)+' degrees. '+(v>=85?'Throttling. Cooling required.':'Fans at full.'),
    memory:v=>'Memory pressure. '+numWord(v)+' percent used. Swapping to disk.',
    ssd:v=>'Disk almost full. '+numWord((100-v)*0.98)+' gigabytes left on root.',
    load:v=>'High load. All four cores busy.',
    update:v=>'System update in progress. 27 packages. Reboot after.',
    alarm:v=>'Service down. nginx, fbweb and cockpit are not responding.' };
  const DEMO={backup:100,intrusion:48,heat:93,memory:97,ssd:96,load:99,update:27,alarm:9};
  const hookSit=()=>{ if(!window.fbSituation||window.fbSituation._khoa) return false; const f=window.fbSituation; const g=function(name,opts){ f(name,opts); const say=SAY[name]; if(say) setTimeout(()=>window.fbSay(say(opts&&opts.value!=null?opts.value:DEMO[name]||0)),900); }; g._khoa=true; window.fbSituation=g; return true; };
  if(!hookSit()) addEventListener('load',()=>setTimeout(hookSit,0));
  let lastSeen=0; window.fbSeen=function(){ const n=performance.now(); if(lastSeen&&n-lastSeen>90000) window.fbSay('Welcome back.'); lastSeen=n; };
  setInterval(()=>{ const d=new Date(); if(d.getMinutes()===0&&d.getSeconds()<20&&document.visibilityState==='visible'){ const h=d.getHours(); window.fbSay((h===0?'Midnight':h+' hundred')+'. '+window.fbStatusLine()); } },20000);"""
R=[
 (OLD, NEW),
 ("else if(building){ building=false; setState(mode); }", "else if(building){ building=false; setState(mode); if(window.fbOnWake) setTimeout(window.fbOnWake,600); }"),
 ("else if(!wantSleep&&asleep){ asleep=false; if(window.sfx) window.sfx('assemble'); setState(mode); }", "else if(!wantSleep&&asleep){ asleep=false; if(window.sfx) window.sfx('assemble'); setState(mode); if(window.fbOnWake) setTimeout(window.fbOnWake,7000); }"),
 ('<div class="role">THE FACE OF THE SERVER</div>', '<div class="role">KHOA &middot; THE FACE OF THE SERVER</div>'),
 ("face={x:b.xCenter,y:b.yCenter,t:performance.now()};", "face={x:b.xCenter,y:b.yCenter,t:performance.now()}; if(window.fbSeen) window.fbSeen();"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'window.fbSay=' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
