#!/usr/bin/env python3
# patch_sound.py - adds the "assembly" sound (a rising sweep + rumble that ends in a lock-in hit) to face/map/index.html.
# Plays on the REPLAY button and on the first click if the figure is still assembling. Idempotent. Usage: python3 patch_sound.py FILE...
import sys
SND = r"""else if(kind==='assemble'){ const D=(typeof BUILD_MS!=='undefined'?BUILD_MS:7000)/1000;
      if(window._asm){ try{ window._asm.gain.setTargetAtTime(0,t,0.05); }catch(e){} } window._asm=g; g.gain.value=0.9;
      // 1) low rumble: noise through a lowpass that slowly opens
      const n=c.createBufferSource(), nb=c.createBuffer(1,c.sampleRate*(D+2),c.sampleRate), nd=nb.getChannelData(0); for(let i=0;i<nd.length;i++) nd[i]=Math.random()*2-1; n.buffer=nb;
      const lp=c.createBiquadFilter(); lp.type='lowpass'; lp.Q.value=0.9; lp.frequency.setValueAtTime(80,t); lp.frequency.exponentialRampToValueAtTime(900,t+D*0.9);
      const ng=c.createGain(); ng.gain.setValueAtTime(0.0001,t); ng.gain.exponentialRampToValueAtTime(0.4,t+D*0.85); ng.gain.exponentialRampToValueAtTime(0.0001,t+D+1.8);
      n.connect(lp); lp.connect(ng); ng.connect(g); n.start(t); n.stop(t+D+2);
      // 2) the rising sweep: detuned saws + sub + octave, filter opening as the body fills in, with a quickening pulse
      const sf=c.createBiquadFilter(); sf.type='lowpass'; sf.Q.value=5; sf.frequency.setValueAtTime(140,t+0.3); sf.frequency.exponentialRampToValueAtTime(2800,t+D*0.9);
      const sg=c.createGain(); sg.gain.setValueAtTime(0.0001,t+0.3); sg.gain.exponentialRampToValueAtTime(0.11,t+D*0.88); sg.gain.exponentialRampToValueAtTime(0.0001,t+D*0.97);
      sf.connect(sg); sg.connect(g);
      [[1,'sawtooth',-8],[1,'sawtooth',8],[0.5,'sine',0],[2,'triangle',0],[3,'sine',0]].forEach(([m,ty,det])=>{ const o=c.createOscillator(); o.type=ty; o.detune.value=det; o.frequency.setValueAtTime(52*m,t+0.3); o.frequency.exponentialRampToValueAtTime(160*m,t+D*0.9); o.connect(sf); o.start(t+0.3); o.stop(t+D); });
      const lfo=c.createOscillator(), lg=c.createGain(); lfo.frequency.setValueAtTime(3,t); lfo.frequency.exponentialRampToValueAtTime(24,t+D*0.9); lg.gain.value=0.05; lfo.connect(lg); lg.connect(sg.gain); lfo.start(t); lfo.stop(t+D);
      // 3) a thin rising shimmer on top
      const o2=c.createOscillator(), g2=c.createGain(); o2.type='sine'; o2.frequency.setValueAtTime(260,t+1); o2.frequency.exponentialRampToValueAtTime(2100,t+D*0.9); g2.gain.setValueAtTime(0.0001,t+1); g2.gain.exponentialRampToValueAtTime(0.045,t+D*0.85); g2.gain.exponentialRampToValueAtTime(0.0001,t+D*0.97); o2.connect(g2); g2.connect(g); o2.start(t+1); o2.stop(t+D);
      // 4) lock-in: a deep thud, a metallic ping and a burst of air when the last particles land
      const T=D*0.93; tone(80,24,1.2,'sine',0.6,T); tone(1600,700,0.2,'square',0.05,T); tone(500,3200,0.6,'sine',0.14,T+0.04); tone(2400,2400,0.8,'triangle',0.05,T+0.1);
      const n2=c.createBufferSource(), b2=c.createBuffer(1,c.sampleRate*1.2,c.sampleRate), d2=b2.getChannelData(0); for(let i=0;i<d2.length;i++) d2[i]=(Math.random()*2-1)*Math.exp(-i/d2.length*7); n2.buffer=b2;
      const bf=c.createBiquadFilter(); bf.type='bandpass'; bf.frequency.value=1500; bf.Q.value=0.6; const g3=c.createGain(); g3.gain.value=0.3; n2.connect(bf); bf.connect(g3); g3.connect(g); n2.start(t+T); }
    else if(kind==='close'){"""
R=[
 ("else if(kind==='close'){", SND),
 ("document.getElementById('assemble').onclick=()=>{buildT0=performance.now();};",
  "document.getElementById('assemble').onclick=()=>{buildT0=performance.now(); if(window.sfx) window.sfx('assemble');};"),
 ("addEventListener('pointerdown',()=>ac(),{once:true});",
  "addEventListener('pointerdown',()=>{ const c=ac(); if(!c) return; const go=()=>{ if((performance.now()-buildT0)/BUILD_MS<0.6){ buildT0=performance.now(); window.sfx('assemble'); } }; if(c.state!=='running') c.resume().then(go).catch(()=>{}); else go(); },{once:true});"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if "kind==='assemble'" in s: print(f,'already patched'); continue
    n=0
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once: '+a[:60])
        s=s.replace(a,b,1); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'patched',n)
