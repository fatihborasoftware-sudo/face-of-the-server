const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{ const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']});
 const p=await b.newPage({viewport:{width:400,height:400}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{ const SR=44100, LEN=SR*10; const O=window.OfflineAudioContext;
   const make=function(){ const c=new O(2,LEN,SR); Object.defineProperty(c,'state',{get:()=>'running'}); c.resume=()=>Promise.resolve(); window.__OAC=c; return c; };
   window.AudioContext=make; window.webkitAudioContext=make; });
 await p.goto('http://localhost:8765/khoa-holo.html?embed=hero&lang=en'); await p.waitForTimeout(1500);
 const r=await p.evaluate(async()=>{ if(!window.sfx) return 'nosfx'; window.sfx('assemble'); const c=window.__OAC; if(!c) return 'noctx';
   const buf=await c.startRendering(); const L=buf.getChannelData(0), R=buf.numberOfChannels>1?buf.getChannelData(1):L;
   const n=L.length, dv=new DataView(new ArrayBuffer(44+n*4)); const w=(o,s)=>{for(let i=0;i<s.length;i++)dv.setUint8(o+i,s.charCodeAt(i));};
   w(0,'RIFF');dv.setUint32(4,36+n*4,true);w(8,'WAVE');w(12,'fmt ');dv.setUint32(16,16,true);dv.setUint16(20,1,true);dv.setUint16(22,2,true);dv.setUint32(24,44100,true);dv.setUint32(28,44100*4,true);dv.setUint16(32,4,true);dv.setUint16(34,16,true);w(36,'data');dv.setUint32(40,n*4,true);
   let pk=0; for(let i=0;i<n;i++){ const a=Math.max(-1,Math.min(1,L[i])),bb=Math.max(-1,Math.min(1,R[i])); pk=Math.max(pk,Math.abs(a)); dv.setInt16(44+i*4,a*32767,true); dv.setInt16(46+i*4,bb*32767,true); }
   let s=''; const u=new Uint8Array(dv.buffer); for(let i=0;i<u.length;i+=32768) s+=String.fromCharCode.apply(null,u.subarray(i,i+32768)); return {b64:btoa(s),pk}; });
 if(r&&r.b64){ fs.writeFileSync('/root/holo/assemble.wav',Buffer.from(r.b64,'base64')); console.log('peak',r.pk); } else console.log(r,errs.slice(0,3));
 await b.close(); })();
