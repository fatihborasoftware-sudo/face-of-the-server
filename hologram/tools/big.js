const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--mute-audio']});
 const p=await b.newPage({viewport:{width:768,height:768},deviceScaleFactor:2});
 await p.addInitScript({path:'/root/holo/clock.js'}); await p.addInitScript({path:'/root/holo/notext.js'});
 await p.goto('http://localhost:8765/khoa-holo.html?embed=hero&lang=en');
 await p.addStyleTag({content:'html,body,#stage{background:#000!important} body *{visibility:hidden!important} canvas{visibility:visible!important}'});
 const dt=1000/30; const shots={105:'asm',360:'idle'};
 for(let i=0;i<=360;i++){ await p.evaluate(d=>window.__step(d),dt); if(shots[i]) await p.screenshot({path:'/root/holo/big-'+shots[i]+'.png'}); }
 await b.close(); console.log('ok'); })();
