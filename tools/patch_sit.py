#!/usr/bin/env python3
# patch_sit.py - SITUATIONS: simulated server situations (backup, intrusion, heat, memory, ssd, load, update, alarm)
# with their own body colour, motion, big sci-fi gauge, banner and sound. Menu in the bottom bar; API for the
# automation: window.fbSituation('heat',{value:81}) / fbSituation('normal'). Face page. Idempotent.
import sys
CSS="""  #sitb{position:relative} .sitmenu{position:fixed;bottom:64px;background:#040b14f0;border:1px solid #1d3a57;border-radius:8px;padding:6px;display:none;flex-direction:column;gap:2px;z-index:30;min-width:200px;box-shadow:0 0 30px #000}
  .sitmenu.on{display:flex} .sitmenu div{padding:6px 12px;font:11px/1.6 "IBM Plex Mono",monospace;letter-spacing:.14em;color:#cfe4f5;cursor:pointer;border-radius:5px;display:flex;align-items:center;gap:10px}
  .sitmenu div:hover{background:#0f2238} .sitmenu div i{width:8px;height:8px;border-radius:50%;background:var(--c);box-shadow:0 0 8px var(--c);flex:none} .sitmenu div.on{color:#fff;background:#0c1c2e}
  #fx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:4}
  #sitban{position:fixed;left:50%;top:76px;transform:translateX(-50%) translateY(-20px);opacity:0;padding:8px 22px;border:1px solid var(--sc,#6fdcff);border-radius:6px;color:var(--sc,#6fdcff);font:12px/1.5 "IBM Plex Mono",monospace;letter-spacing:.35em;text-transform:uppercase;background:#02060acc;box-shadow:0 0 24px color-mix(in srgb,var(--sc,#6fdcff) 45%,transparent);transition:opacity .5s,transform .6s cubic-bezier(.2,1.3,.4,1);pointer-events:none;z-index:6;white-space:nowrap}
  #sitban.on{opacity:1;transform:translateX(-50%) translateY(0)} #sitban.blink{animation:sitblink .5s steps(2) infinite} @keyframes sitblink{50%{opacity:.35}}
  #sl .c.hi h5{color:#fff;text-shadow:0 0 12px var(--vt)} #sl .c.hi{animation:hipulse 1.6s ease-in-out infinite} @keyframes hipulse{50%{opacity:.55}}
"""
JS=r"""<script>
// ---------- SITUATIONS: what the server is going through, shown on the body (demo now, automation later)
(() => {
  const SIT={
    normal:   {label:'NORMAL',        color:'#6fdcff', tint:[0.35,0.85,1.0], tintAmt:0,   fx:0, fxAmt:0,   gauge:null},
    backup:   {label:'BACKUP RUNNING',color:'#39ff6a', tint:[0.25,1.0,0.45], tintAmt:.85, fx:3, fxAmt:.5,  gauge:{title:'BACKUP TO DISK',unit:'%',max:100,demo:[0,100,45],sub:v=>(v*0.28).toFixed(1)+' GB of 28 GB'}, card:2, snd:'tick'},
    intrusion:{label:'INTRUSION DETECTED',color:'#ff2a1a',tint:[1,0.1,0.08], tintAmt:1,   fx:3, fxAmt:1,   gauge:{title:'THREAT LEVEL',unit:'',max:60,demo:[0,48,30],sub:v=>Math.round(v)+' FAILED LOGINS  \u00b7  185.220.101.7'}, card:5, mood:1, snd:'alarm', blink:true},
    heat:     {label:'OVERHEATING',   color:'#ff7a1a', tint:[1,0.45,0.1],   tintAmt:.9,  fx:1, fxAmt:1,   gauge:{title:'CPU TEMPERATURE',unit:'\u00b0C',max:100,demo:[48,93,25],sub:v=>v<60?'COOL':v<75?'WARM  \u00b7  FANS 60 %':v<85?'HOT  \u00b7  FANS 100 %':'CRITICAL  \u00b7  THROTTLING'}, card:1, snd:'rumble'},
    memory:   {label:'MEMORY PRESSURE',color:'#b86bff', tint:[0.7,0.4,1.0],  tintAmt:.85, fx:3, fxAmt:.6,  gauge:{title:'MEMORY',unit:'%',max:100,demo:[41,97,25],sub:v=>(v*0.072).toFixed(1)+' GB of 7.2 GB  \u00b7  SWAP '+Math.round(Math.max(0,v-70)*12)+' MB'}, card:1, snd:'tick'},
    ssd:      {label:'DISK ALMOST FULL',color:'#ffb347', tint:[1,0.7,0.25],  tintAmt:.8,  fx:2, fxAmt:1,   gauge:{title:'SSD  \u00b7  ROOT',unit:'%',max:100,demo:[31,96,25],sub:v=>Math.round((100-v)*0.98)+' GB LEFT of 98 GB'}, card:2, snd:'rumble'},
    load:     {label:'HIGH LOAD',     color:'#e8f4ff', tint:[0.8,0.95,1.0], tintAmt:.7,  fx:3, fxAmt:1,   gauge:{title:'SYSTEM LOAD',unit:'%',max:100,demo:[20,99,20],sub:v=>'LOAD '+(v/25).toFixed(2)+'  \u00b7  4 CORES'}, card:1, snd:'tick'},
    update:   {label:'UPDATING',      color:'#4aa8ff', tint:[0.3,0.6,1.0],  tintAmt:.8,  fx:4, fxAmt:1,   gauge:{title:'SYSTEM UPDATE',unit:'',max:27,demo:[0,27,30],sub:v=>Math.round(v)+' of 27 PACKAGES  \u00b7  REBOOT AFTER'}, card:0, snd:'tick'},
    alarm:    {label:'SERVICE DOWN',  color:'#ff4a3a', tint:[1,0.3,0.2],    tintAmt:.8,  fx:3, fxAmt:.4,  gauge:{title:'SERVICES',unit:'',max:12,demo:[12,9,12],sub:v=>Math.round(v)+' of 12 RUNNING  \u00b7  nginx \u00b7 fbweb \u00b7 cockpit'}, card:3, snd:'chime', blink:true},
  };
  const ORDER=['normal','backup','intrusion','heat','memory','ssd','load','update','alarm'];
  const fx=document.createElement('canvas'); fx.id='fx'; document.body.appendChild(fx); const X=fx.getContext('2d');
  const ban=document.createElement('div'); ban.id='sitban'; document.body.appendChild(ban);
  // sounds (own tiny synth)
  let AC=null; const ac=()=>{ try{ AC=AC||new (window.AudioContext||window.webkitAudioContext)(); if(AC.state==='suspended') AC.resume(); }catch(e){} return AC; };
  let sndT=0; function snd(kind){ const c=ac(); if(!c||c.state!=='running') return; const t=c.currentTime, g=c.createGain(); g.gain.value=0.5; g.connect(c.destination); if(sndT&&sndT.stop) try{sndT.stop();}catch(e){}
    const tone=(f0,f1,d,type,vol,at)=>{ const o=c.createOscillator(), gg=c.createGain(); o.type=type; o.frequency.setValueAtTime(f0,t+at); o.frequency.exponentialRampToValueAtTime(f1,t+at+d); gg.gain.setValueAtTime(0.0001,t+at); gg.gain.exponentialRampToValueAtTime(vol,t+at+0.02); gg.gain.exponentialRampToValueAtTime(0.0001,t+at+d); o.connect(gg); gg.connect(g); o.start(t+at); o.stop(t+at+d+0.05); return o; };
    if(kind==='alarm'){ for(let i=0;i<8;i++){ tone(i%2?620:470,i%2?600:450,0.28,'sawtooth',0.12,i*0.3); } tone(80,60,2.4,'sine',0.25,0); }
    else if(kind==='rumble'){ const n=c.createBufferSource(), b=c.createBuffer(1,c.sampleRate*4,c.sampleRate), d=b.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; n.buffer=b; const f=c.createBiquadFilter(); f.type='lowpass'; f.frequency.value=140; const gg=c.createGain(); gg.gain.setValueAtTime(0.0001,t); gg.gain.exponentialRampToValueAtTime(0.5,t+0.6); gg.gain.exponentialRampToValueAtTime(0.0001,t+4); n.connect(f); f.connect(gg); gg.connect(g); n.start(t); tone(55,40,3,'sine',0.3,0); }
    else if(kind==='tick'){ for(let i=0;i<10;i++) tone(1400+((i*7)%3)*300,900,0.06,'square',0.05,i*0.16); tone(300,1200,0.9,'sine',0.08,0); }
    else if(kind==='chime'){ tone(880,880,0.5,'sine',0.14,0); tone(660,660,0.5,'sine',0.14,0.35); tone(440,440,0.9,'sine',0.14,0.7); tone(120,90,1.2,'triangle',0.2,0.7); }
    else if(kind==='whir'){ tone(200,1800,0.5,'sawtooth',0.05,0); tone(1800,600,0.35,'sine',0.08,0.4); } }
  // state
  let cur='normal', prev=null, tSwitch=0, val=0, demo=null, sub='';
  window.fbSit=null;
  window.fbSituation=function(name,opts){ opts=opts||{}; if(!SIT[name]) return; const S=SIT[name]; prev=cur; cur=name; tSwitch=performance.now(); demo=null;
    if(S.gauge){ if(opts.value!=null){ val=opts.value; } else { demo={from:S.gauge.demo[0],to:S.gauge.demo[1],dur:S.gauge.demo[2]*1000,t0:performance.now()}; val=S.gauge.demo[0]; } }
    window.fbSit=name==='normal'?null:{name,tint:new THREE.Vector3(...S.tint),tintAmt:S.tintAmt,fx:S.fx,fxAmt:S.fxAmt,vein:S.color,level:0};
    if(window.fbMood) window.fbMood(S.mood?1:0);
    document.documentElement.style.setProperty('--sc',S.color);
    ban.textContent=opts.text||S.label; ban.classList.toggle('on',name!=='normal'); ban.classList.toggle('blink',!!S.blink);
    document.querySelectorAll('#sl .c').forEach(c=>c.classList.remove('hi')); if(S.card!=null){ const cards=document.querySelectorAll('#sl .c, #sl .head'); const el=[...cards].find(c=>c.classList.contains('head')?S.card===0:false)||document.querySelectorAll('#sl .c')[S.card-1]; if(el&&S.card>0) el.classList.add('hi'); }
    if(name==='normal'){ if(window.fbStatus) document.documentElement.style.setProperty('--vt',window.fbStatus.color); snd('whir'); } else { snd('whir'); setTimeout(()=>snd(S.snd),450); }
    document.querySelectorAll('.sitmenu div').forEach(d=>d.classList.toggle('on',d.dataset.k===name)); };
  // menu
  const bar=document.querySelector('.bar'); if(bar){ const b=document.createElement('button'); b.id='sitb'; b.textContent='\u25c8 SITUATIONS'; bar.insertBefore(b,document.getElementById('cam')||document.getElementById('stop'));
    const m=document.createElement('div'); m.className='sitmenu'; document.body.appendChild(m);
    ORDER.forEach(k=>{ const d=document.createElement('div'); d.dataset.k=k; d.style.setProperty('--c',SIT[k].color); d.innerHTML='<i></i>'+SIT[k].label; if(k==='normal') d.classList.add('on'); d.onpointerdown=e=>{ e.stopPropagation(); }; d.onclick=e=>{ e.stopPropagation(); m.classList.remove('on'); window.fbSituation(k); }; m.appendChild(d); });
    b.onclick=e=>{ e.stopPropagation(); ac(); const r=b.getBoundingClientRect(); m.style.left=Math.max(8,Math.min(innerWidth-216,r.left))+'px'; m.classList.toggle('on'); };
    addEventListener('pointerdown',e=>{ if(!m.contains(e.target)&&e.target!==b) m.classList.remove('on'); }); }
  // the big gauge
  const ease=x=>1-Math.pow(1-x,3), back=x=>1+2.2*Math.pow(x-1,3)+1.2*Math.pow(x-1,2);
  function ring(cx,cy,r,S,v,a,rot,now){ if(a<=0) return; const g=S.gauge, col=S.color; X.save(); X.globalAlpha=a; X.translate(cx,cy); X.rotate(rot); X.translate(-cx,-cy);
    X.lineWidth=1; X.strokeStyle=col; X.globalAlpha=a*0.35; X.beginPath(); X.arc(cx,cy,r,0,Math.PI*2); X.stroke(); X.beginPath(); X.arc(cx,cy,r*0.86,0,Math.PI*2); X.stroke();
    X.globalAlpha=a*0.5; for(let i=0;i<72;i++){ const an=i/72*Math.PI*2, L=i%6?4:11; X.lineWidth=i%6?1:2; X.beginPath(); X.moveTo(cx+Math.cos(an)*(r-2),cy+Math.sin(an)*(r-2)); X.lineTo(cx+Math.cos(an)*(r-2-L),cy+Math.sin(an)*(r-2-L)); X.stroke(); }
    X.setLineDash([3,9]); X.lineWidth=2; X.globalAlpha=a*0.45; X.beginPath(); X.arc(cx,cy,r*1.06,now*0.3,now*0.3+Math.PI*1.5); X.stroke(); X.beginPath(); X.arc(cx,cy,r*0.93,-now*0.2,-now*0.2+Math.PI*0.8); X.stroke(); X.setLineDash([]);
    const a0=Math.PI*0.75, sweep=Math.PI*1.5, f=Math.max(0,Math.min(1,v/g.max)); X.lineWidth=r*0.045; X.strokeStyle='#ffffff18'; X.globalAlpha=a; X.beginPath(); X.arc(cx,cy,r*0.79,a0,a0+sweep); X.stroke();
    X.strokeStyle=col; X.shadowColor=col; X.shadowBlur=22; X.beginPath(); X.arc(cx,cy,r*0.79,a0,a0+sweep*f); X.stroke(); X.shadowBlur=0;
    const tip=a0+sweep*f; X.fillStyle='#fff'; X.shadowColor='#fff'; X.shadowBlur=14; X.beginPath(); X.arc(cx+Math.cos(tip)*r*0.79,cy+Math.sin(tip)*r*0.79,r*0.03,0,Math.PI*2); X.fill(); X.shadowBlur=0;
    X.restore(); X.save(); X.globalAlpha=a; X.textAlign='center'; X.fillStyle=col; X.shadowColor=col; X.shadowBlur=18;
    X.font='600 '+Math.round(r*0.34)+'px IBM Plex Mono,monospace'; X.fillText(Math.round(v)+g.unit,cx,cy+r+r*0.5);
    X.shadowBlur=0; X.font=Math.round(r*0.075)+'px IBM Plex Mono,monospace'; X.fillStyle='#d6eeff'; X.fillText(g.title.split('').join(' '),cx,cy+r+r*0.13);
    X.fillStyle=col; X.globalAlpha=a*0.85; X.font=Math.round(r*0.06)+'px IBM Plex Mono,monospace'; X.fillText((sub||'').split('').join(String.fromCharCode(8202))+'',cx,cy+r+r*0.64); X.restore(); }
  function frame(){ requestAnimationFrame(frame); const W=innerWidth,H=innerHeight; if(fx.width!==W*2||fx.height!==H*2){ fx.width=W*2; fx.height=H*2; } X.setTransform(2,0,0,2,0,0); X.clearRect(0,0,W,H);
    const now=performance.now(), S=SIT[cur], k=Math.min(1,(now-tSwitch)/900);
    if(demo){ const p=Math.min(1,(now-demo.t0)/demo.dur); val=demo.from+(demo.to-demo.from)*ease(p); }
    if(S.gauge){ sub=S.gauge.sub(val); if(window.fbSit){ window.fbSit.level=Math.max(0.15,Math.min(1,val/S.gauge.max)); window.fbTouch&&window.fbTouch(); } document.documentElement.style.setProperty('--vt',S.color); }
    let cx=W/2, cy=H*0.52; if(window.serraProject){ const p=window.serraProject(0,-0.05,0); cx=p[0]; cy=p[1]; } const r=Math.min(W,H)*0.27;
    if(prev&&SIT[prev].gauge&&k<1){ ring(cx,cy,r*(1+0.4*k),SIT[prev],val,1-k,-k*0.6,now/1000); }
    if(S.gauge){ const e=back(k); ring(cx,cy,r*(0.55+0.45*e),S,val,k,(1-k)*0.8,now/1000); } }
  frame();
  addEventListener('keydown',e=>{ const n=parseInt(e.key); if(n>=0&&n<ORDER.length&&!e.ctrlKey&&!e.altKey&&!e.metaKey) window.fbSituation(ORDER[n]); }); // 0 normal, 1 backup, 2 intrusion, 3 heat ...
})();
</script>
"""
R=[
 ("</style>", CSS+"</style>"),
 ("uSleep:{value:0},uBody:{value:0},uSpread:{value:0},", "uSleep:{value:0},uBody:{value:0},uSpread:{value:0},uTint:{value:new THREE.Vector3(0.35,0.85,1.0)},uTintAmt:{value:0},uFx:{value:0},uFxAmt:{value:0},"),
 ("uniform float uBuild,uLevel,uThink,uPix,uMood,uSleep,uBody,uSpread; uniform vec3 uDrift,uBubble;", "uniform float uBuild,uLevel,uThink,uPix,uMood,uSleep,uBody,uSpread,uTintAmt,uFx,uFxAmt; uniform vec3 uDrift,uBubble,uTint;"),
 ("vec3 p=aKind>1.5?bendL(pb,0.35+0.6*aSeed):bend(pb);",
  "if(uFxAmt>0.0){ float hh=clamp((position.y+1.6)/2.6,0.,1.); if(uFx<1.5){ pb.y+=uFxAmt*0.05*sin(uTime*4.0+aSeed*60.0)*hh; pb.x+=uFxAmt*0.03*sin(uTime*3.0+aSeed*40.0); } else if(uFx<2.5){ pb.y-=uFxAmt*(1.0-hh)*(0.25+0.35*fract(aSeed*7.3)); pb.x+=uFxAmt*(1.0-hh)*(fract(aSeed*3.1)-0.5)*0.3; } else if(uFx<3.5){ pb+=normal*uFxAmt*0.02*sin(uTime*12.0+aSeed*90.0); } }\n        vec3 p=aKind>1.5?bendL(pb,0.35+0.6*aSeed):bend(pb);"),
 ("vec3 CY=mix(vec3(0.35,0.85,1.0),vec3(1.0,0.12,0.08),uMood), OR=mix(vec3(1.0,0.55,0.12),vec3(1.0,0.2,0.05),uMood);",
  "vec3 CY=mix(vec3(0.35,0.85,1.0),vec3(1.0,0.12,0.08),uMood), OR=mix(vec3(1.0,0.55,0.12),vec3(1.0,0.2,0.05),uMood); CY=mix(CY,uTint,uTintAmt); OR=mix(OR,uTint*vec3(1.0,0.85,0.7)+vec3(0.15,0.05,0.0),uTintAmt*0.6);"),
 ("a*=mix(1.4,1.0,e)*mix(1.0,0.5,smoothstep(0.2,0.4,position.y));",
  "a*=mix(1.4,1.0,e)*mix(1.0,0.5,smoothstep(0.2,0.4,position.y)); if(uFx>3.5){ float band=smoothstep(0.14,0.0,abs(fract(uTime*0.22)*3.6-1.9-position.y)); a+=band*uFxAmt*1.4; c=mix(c,vec3(0.6,0.85,1.0),band*uFxAmt); } if(uFx<1.5) a*=1.0+uFxAmt*0.35;"),
 ("let moodTgt=0;", "let moodTgt=0; window.fbMood=v=>{ moodTgt=v?1:0; document.getElementById('scary').classList.toggle('on',!!moodTgt); document.body.style.setProperty('--cyan',moodTgt?'#ff2a1a':'#6fdcff'); };"),
 ("if(window.fbStatus) U.uVeinCol.value.set(window.fbStatus.color);",
  "if(window.fbStatus) U.uVeinCol.value.set(window.fbStatus.color); { const S=window.fbSit; const ta=S?1:0; sitA+=(ta-sitA)*Math.min(1,dt*1.6); if(S){ U.uTint.value.lerp(S.tint,Math.min(1,dt*2.5)); U.uVeinCol.value.set(S.vein); U.uFx.value=S.fx; } U.uTintAmt.value=sitA*(S?S.tintAmt:0); U.uFxAmt.value=sitA*(S?S.fxAmt*(0.3+0.7*(S.level||0)):0); }"),
 ("let lastTouch=performance.now(), asleep=false, sleepV=0,", "let sitA=0, lastTouch=performance.now(), asleep=false, sleepV=0,"),
 ("const bpm=D?Math.min(150,58+(D.cpu_pct||0)*0.8):64,", "const bpm=(window.fbSit&&{intrusion:150,heat:120,load:125,alarm:96,memory:105}[window.fbSit.name])||(D?Math.min(150,58+(D.cpu_pct||0)*0.8):64),"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fbSituation' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    s=s.replace('</body>',JS+'</body>',1) if '</body>' in s else s.rstrip('\n')+'\n'+JS
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
