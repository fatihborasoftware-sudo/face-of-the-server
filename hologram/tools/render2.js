const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--mute-audio']});
 const p=await b.newPage({viewport:{width:768,height:768}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript({path:'/root/holo/clock.js'}); await p.addInitScript({path:'/root/holo/stub.js'});
 await p.goto('http://localhost:8765/khoa-web.html?embed=hero&lang=tr');
 await p.evaluate(()=>{ window.KHOA_CLIPS['__A2__']='holo/a2.mp3'; window.KHOA_CLIPS['__A3__']='holo/a3.mp3'; });
 await p.addStyleTag({content:'html,body,#stage{background:#000!important} body *{visibility:hidden!important} canvas{visibility:visible!important}'});
 const FPS=30, N=Math.round(23.7*FPS);
 const w=n=>Array(n).fill('söz').join(' ');
 const say={[Math.round(7.5*FPS)]:'__A2__',[Math.round(17.5*FPS)]:'__A3__'};
 for(let i=0;i<N;i++){ await p.evaluate(d=>window.__step(d),1000/FPS);
   if(say[i]) await p.evaluate(t=>window.fbSay(t,{force:true}),say[i]);
   await p.screenshot({path:'/root/holo/kb/f'+String(i).padStart(4,'0')+'.jpg',type:'jpeg',quality:95}); }
 console.log('done',N,errs.slice(0,5)); await b.close(); })();
