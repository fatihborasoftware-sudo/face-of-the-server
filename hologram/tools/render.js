const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--mute-audio']});
 const p=await b.newPage({viewport:{width:768,height:768}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript({path:'/root/holo/clock.js'});
 await p.goto('http://localhost:8765/khoa-web.html?embed=hero&lang=tr');
 await p.addStyleTag({content:'html,body,#stage{background:#000!important} body *{visibility:hidden!important} canvas{visibility:visible!important}'});
 const FPS=30, N=22*FPS, SAY=Math.round(8.5*FPS); 
 for(let i=0;i<N;i++){ await p.evaluate(d=>window.__step(d),1000/FPS);
   if(i===SAY) await p.evaluate(()=>window.fbSay('Ben Khoa. Sunucunun yüzüyüm.',{force:true}));
   await p.screenshot({path:'/root/holo/fr/f'+String(i).padStart(4,'0')+'.jpg',type:'jpeg',quality:95}); }
 console.log('done',N,errs.slice(0,5)); await b.close(); })();
