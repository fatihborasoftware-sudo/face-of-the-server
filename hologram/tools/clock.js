(()=>{let T=0;const t0=1790000000000;
performance.now=()=>T; Date.now=()=>t0+T;
let rafs=[], id=1;
window.requestAnimationFrame=cb=>{rafs.push([id,cb]);return id++;};
window.cancelAnimationFrame=i=>{rafs=rafs.filter(r=>r[0]!==i);};
let timers=[];
window.setTimeout=(f,ms,...a)=>{const i=id++; timers.push({i,at:T+(+ms||0),f,a}); return i;};
window.clearTimeout=i=>{timers=timers.filter(t=>t.i!==i);};
window.setInterval=(f,ms,...a)=>{const i=id++; timers.push({i,at:T+Math.max(1,+ms||1),f,a,every:Math.max(1,+ms||1)}); return i;};
window.clearInterval=window.clearTimeout;
window.__T=()=>T;
window.__step=(dt)=>{const end=T+dt; let guard=0;
  for(;;){ timers.sort((x,y)=>x.at-y.at); const t=timers[0]; if(!t||t.at>end||guard++>5000) break;
    T=Math.max(T,t.at); if(t.every) t.at+=t.every; else timers.shift();
    try{ if(typeof t.f==='function') t.f(...t.a); }catch(e){ console.error('timer',e&&e.message); } }
  T=end; const r=rafs; rafs=[]; r.forEach(([i,cb])=>{ try{cb(T);}catch(e){console.error('raf',e&&e.message);} }); };
})();
