#!/usr/bin/env python3
# patch_voice2.py - Khoa speaks with the server's Piper voices (khoa-tts service, deep/mature "ryan" by default),
# falling back to the browser voice when the service is not reachable. VOICE button cycles ryan/joe/alan/... /browser.
import sys
OLD_SAY="""    try{ speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(text); const v=window.fbVoice(); if(v) u.voice=v; u.rate=opts.rate||0.92; u.pitch=opts.pitch||0.72; u.volume=1;
      u.onboundary=()=>{tgt=0.8+Math.random()*0.3;}; u.onend=()=>{pulses=[];setState('idle');setTimeout(()=>{if(mode==='idle')cap.textContent='';},1600);};
      speechSynthesis.speak(u); }catch(e){}
    setTimeout(()=>{try{if(!speechSynthesis.speaking)setState('idle');}catch(e){setState('idle');}},ms+300); };"""
NEW_SAY="""    const done=()=>{ pulses=[]; setState('idle'); setTimeout(()=>{ if(mode==='idle') cap.textContent=''; },1600); };
    const browserSay=()=>{ try{ speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(text); const v=window.fbVoice(); if(v) u.voice=v; u.rate=opts.rate||0.92; u.pitch=opts.pitch||0.72; u.volume=1;
        u.onboundary=()=>{tgt=0.8+Math.random()*0.3;}; u.onend=done; speechSynthesis.speak(u); }catch(e){}
      setTimeout(()=>{try{if(!speechSynthesis.speaking)setState('idle');}catch(e){setState('idle');}},ms+300); };
    const srv=window.fbSrvVoice(); if(srv==='browser'){ browserSay(); return; }
    try{ speechSynthesis.cancel(); }catch(e){} if(window.fbAudio){ try{ window.fbAudio.pause(); }catch(e){} }
    const ctrl=new AbortController(), tm=setTimeout(()=>ctrl.abort(),8000);
    fetch(window.fbTTS+'say?text='+encodeURIComponent(text)+'&v='+encodeURIComponent(srv),{signal:ctrl.signal}).then(r=>{ clearTimeout(tm); if(!r.ok) throw 0; return r.blob(); }).then(b=>{
      const a=new Audio(URL.createObjectURL(b)); window.fbAudio=a; a.volume=1;
      try{ const c=window.fbAC=window.fbAC||new (window.AudioContext||window.webkitAudioContext)(); if(c.state==='suspended') c.resume(); const s=c.createMediaElementSource(a), an=c.createAnalyser(); an.fftSize=256; s.connect(an); an.connect(c.destination);
        const buf=new Uint8Array(an.frequencyBinCount); const iv=setInterval(()=>{ if(a.paused||a.ended){ clearInterval(iv); return; } an.getByteFrequencyData(buf); let m=0; for(let i=2;i<40;i++) m=Math.max(m,buf[i]); tgt=Math.max(tgt,Math.min(1.2,m/150)); },40); }catch(e){}
      a.onended=done; a.onerror=done; a.play().catch(browserSay); }).catch(()=>{ clearTimeout(tm); browserSay(); }); };
  window.fbTTS=location.protocol==='https:'?'/khoa/':('http://'+location.hostname+':8082/');
  window.fbSrvVoice=()=>{ try{ return localStorage.getItem('fbSrvVoice')||'ryan'; }catch(e){ return 'ryan'; } };"""
OLD_BTN="""    vb.onclick=e=>{ e.stopPropagation(); let vs=[]; try{ vs=speechSynthesis.getVoices().filter(x=>/^en/i.test(x.lang)); }catch(e){} if(!vs.length){ window.fbSay('No voices found in this browser.',{force:true}); return; }
      const cur=window.fbVoice(); const i=(vs.indexOf(cur)+1)%vs.length; try{ localStorage.setItem('fbVoice',vs[i].name); }catch(e){}
      window.fbSay('This is Khoa, the face of the server. Voice: '+vs[i].name.replace(/Microsoft |Google |Online|\\(Natural\\)|- English.*$/g,'').trim()+'.',{force:true}); }; }"""
NEW_BTN="""    const SV=['ryan','joe','alan','northern_english_male','norman','lessac','browser'];
    vb.onclick=e=>{ e.stopPropagation(); const cur=window.fbSrvVoice(); const nx=SV[(SV.indexOf(cur)+1)%SV.length]; try{ localStorage.setItem('fbSrvVoice',nx); }catch(e){}
      window.fbSay('This is Khoa, the face of the server. Voice: '+nx.replace(/_/g,' ')+'.',{force:true}); }; }"""
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'window.fbTTS=' in s: print(f,'already patched'); continue
    for a,b in [(OLD_SAY,NEW_SAY),(OLD_BTN,NEW_BTN)]:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:60])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
