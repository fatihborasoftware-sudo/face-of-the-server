const { chromium } = require('playwright');
const [,, name, outdir, full] = process.argv;
(async()=>{ const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--mute-audio']});
 const p=await b.newPage({viewport:{width:768,height:768}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript({path:'/root/holo/clock.js'}); await p.addInitScript({path:'/root/holo/notext.js'});
 await p.goto('http://localhost:8765/khoa-holo.html?embed=hero&lang=tr');
 await p.addStyleTag({content:'html,body,#stage{background:#000!important} body *{visibility:hidden!important} canvas{visibility:visible!important}'});
 const FPS=30, dt=1000/FPS;
 for(let i=0;i<9*FPS;i++) await p.evaluate(d=>window.__step(d),dt);   // warm-up: Khoa fully formed
 const N=full?20*FPS:0, SIT=Math.round(1.0*FPS);
 const probe=full?[]:[45,120,300,540];
 const total=full?N:600;
 for(let i=0;i<total;i++){ await p.evaluate(d=>window.__step(d),dt);
   if(i===SIT) await p.evaluate(n=>window.fbSituation(n),name);
   if(full || probe.includes(i)) await p.screenshot({path:outdir+'/f'+String(i).padStart(4,'0')+'.jpg',type:'jpeg',quality:95}); }
 console.log('done',name,errs.slice(0,3)); await b.close(); })();
