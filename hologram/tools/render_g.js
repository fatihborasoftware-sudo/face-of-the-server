// usage: node render_g.js <mode: idle|talk> <outdir>
const { chromium } = require('playwright'); const fs=require('fs');
const [,, MODE, OUT] = process.argv;
(async()=>{ const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--mute-audio']});
 const p=await b.newPage({viewport:{width:768,height:768}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 for(const s of ['clock','notext','camlock']) await p.addInitScript({path:'/root/holo/'+s+'.js'});
 await p.goto('http://localhost:8765/khoa-holo.html?embed=hero&lang=en');
 await p.addStyleTag({content:'html,body,#stage{background:#000!important} body *{visibility:hidden!important} canvas{visibility:visible!important} #fx{visibility:hidden!important}'});
 const TL=JSON.parse(fs.readFileSync('/root/holo/timeline_'+MODE+'.json','utf8'));
 await p.evaluate(L=>{ window.fbIntroQuiet=true; (L.says||[]).forEach(s=>{ const n=Math.max(1,Math.round(s.d/0.34)); const k=('L'+s.i+' ').concat(Array(n-1).fill('w').join(' ')); window['__K'+s.i]=k; window.KHOA_CLIPS[k]='holo/l'+s.i+'.mp3'; }); },TL);
 const FPS=30, N=Math.round(TL.dur*FPS), ev={}; const add=(t,e)=>{ const f=Math.round(t*FPS); (ev[f]=ev[f]||[]).push(e); };
 (TL.sits||[]).forEach(s=>add(s.t,['sit',s.name]));
 (TL.says||[]).forEach(s=>{ add(s.t,['say',s.i]); add(s.t+s.d+0.1,['stop']); });
 (TL.looks||[]).forEach(l=>add(l.t,['look',l.x,l.y]));
 for(let i=0;i<N;i++){ await p.evaluate(d=>window.__step(d),1000/FPS);
   for(const e of (ev[i]||[])){
     if(e[0]==='sit') await p.evaluate(n=>window.fbSituation(n),e[1]);
     else if(e[0]==='say') await p.evaluate(k=>window.fbSay(window['__K'+k],{force:true}),e[1]);
     else if(e[0]==='look') await p.evaluate(([x,y])=>window.serraLookAt&&window.serraLookAt(x,y),[e[1],e[2]]);
     else await p.evaluate(()=>{ const s=document.getElementById('stop'); if(s) s.onclick(); try{ window.fbAudio&&window.fbAudio.pause(); }catch(e){} }); }
   await p.screenshot({path:OUT+'/f'+String(i).padStart(4,'0')+'.jpg',type:'jpeg',quality:92}); }
 console.log('done',MODE,N,errs.slice(0,5)); await b.close(); })();
