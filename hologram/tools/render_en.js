const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--mute-audio']});
 const p=await b.newPage({viewport:{width:768,height:768}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 for(const s of ['clock','notext','camlock']) await p.addInitScript({path:'/root/holo/'+s+'.js'});
 await p.goto('http://localhost:8765/khoa-holo.html?embed=hero&lang=en');
 await p.addStyleTag({content:'html,body,#stage{background:#000!important} body *{visibility:hidden!important} canvas{visibility:visible!important} #fx{visibility:hidden!important}'});
 const L=[[7.8,1,2.98,null],[11.6,2,7.37,null],[20.0,3,2.80,'backup'],[23.8,4,5.36,'intrusion'],[30.2,5,3.42,'heat'],[34.6,6,3.11,'memory'],[38.7,7,3.45,'ssd'],[43.1,8,2.69,'update'],[46.8,9,6.69,'normal']];
 await p.evaluate(L=>{ window.fbIntroQuiet=true; L.forEach(([t,i,d])=>{ const n=Math.max(1,Math.round(d/0.34)); window['__K'+i]=('L'+i+' ').concat(Array(n-1).fill('w').join(' ')); window.KHOA_CLIPS[window['__K'+i]]='holo/l'+i+'.mp3'; }); },L);
 const FPS=30, N=56*FPS, ev={};
 for(const [t,i,d,sit] of L){ const f=Math.round(t*FPS); if(sit) (ev[f-6]=ev[f-6]||[]).push(['sit',sit]); (ev[f]=ev[f]||[]).push(['say',i]); (ev[Math.round((t+d)*FPS)+3]=ev[Math.round((t+d)*FPS)+3]||[]).push(['stop']); }
 for(let i=0;i<N;i++){ await p.evaluate(d=>window.__step(d),1000/FPS);
   for(const e of (ev[i]||[])){ if(e[0]==='sit') await p.evaluate(n=>window.fbSituation(n),e[1]); else if(e[0]==='say') await p.evaluate(k=>window.fbSay(window['__K'+k],{force:true}),e[1]); else await p.evaluate(()=>{ const s=document.getElementById('stop'); if(s) s.onclick(); try{ window.fbAudio&&window.fbAudio.pause(); }catch(e){} }); }
   await p.screenshot({path:'/root/holo/en_fr/f'+String(i).padStart(4,'0')+'.jpg',type:'jpeg',quality:92}); }
 console.log('done',N,errs.slice(0,5)); await b.close(); })();
