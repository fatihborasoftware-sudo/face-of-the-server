#!/usr/bin/env python3
# patch_sleepgrid.py - Face page sleep mode: the dashboard data laid out as one tidy grid (like the console), drawn in the
# Face theme over the drifting glitter. Replaces the spread-out sleep HUD of patch_sleephud.py. Idempotent.
import sys, re
CSS="""  #sl{position:fixed;left:24px;right:24px;top:74px;bottom:64px;max-width:1500px;margin:0 auto;display:grid;grid-template-columns:1.15fr 1.15fr 1fr;grid-template-rows:auto auto auto 1fr;gap:12px;opacity:0;pointer-events:none;transition:opacity .9s;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.06em;color:var(--ink)}
  body.sleep #sl{opacity:1}
  #sl .c{border:0;border-radius:0;background:transparent;padding:10px 14px 10px;box-shadow:none;min-height:0;overflow:hidden}
  #sl h5{border-bottom:1px solid color-mix(in srgb,var(--vt,#ffb347) 25%,transparent);padding-bottom:6px}
  #sl h5{margin:0 0 8px;font-size:9px;letter-spacing:.3em;font-weight:400;color:var(--vt2,#8a5a1d);display:flex;justify-content:space-between}
  #sl h5 span{color:var(--vt,#ffb347)}
  #sl .head{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:6px 14px}
  #sl .head .l{display:flex;align-items:center;gap:14px}
  #sl .badge{padding:3px 10px;border:1px solid var(--vt,#ffb347);border-radius:4px;letter-spacing:.3em;font-size:10px;color:var(--vt,#ffb347)}
  #sl .sys{color:var(--dim);font-size:10px}
  #sl .clock{font-size:30px;letter-spacing:.12em;color:var(--vt,#ffb347);line-height:1;text-align:right;text-shadow:0 0 12px color-mix(in srgb,var(--vt,#ffb347) 50%,transparent)}
  #sl .date{margin-top:5px;color:var(--vt2,#8a5a1d);font-size:10px;text-align:right}
  #sl canvas{display:block;width:100%}
  #sl .r{display:grid;grid-template-columns:78px 1fr 118px;gap:8px;align-items:center;line-height:2}
  #sl .r b{font-weight:400;color:var(--vt2,#8a5a1d)} #sl .r span{text-align:right;color:var(--ink)}
  #sl .r i{display:block;height:5px;border-radius:3px;background:var(--vtd,#3a2a0f);overflow:hidden}
  #sl .r i::after{content:"";display:block;height:100%;width:var(--w);background:linear-gradient(90deg,var(--vt2,#8a5a1d),var(--vt,#ffb347));box-shadow:0 0 6px var(--vt,#ffb347)}
  #sl .g{display:grid;grid-template-columns:1fr 1fr;gap:2px 14px}
  #sl .s{display:flex;justify-content:space-between;line-height:2} #sl .s i{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--vt,#ffb347);box-shadow:0 0 6px var(--vt,#ffb347);margin-right:8px}
  #sl .s.bad i{background:#ff4a3a;box-shadow:0 0 6px #ff4a3a} #sl .s em{font-style:normal;color:var(--vt2,#8a5a1d)}
  #sl .kv{display:grid;grid-template-columns:96px 1fr;gap:0 10px;line-height:2} #sl .kv b{font-weight:400;color:var(--vt2,#8a5a1d)}
  #sl .net{display:grid;grid-template-columns:1fr 1fr;gap:10px} #sl .net .n{border:0;padding:6px 10px} #sl .net .n b{font-weight:400;color:var(--vt2,#8a5a1d);font-size:9px;letter-spacing:.2em} #sl .net .n span{float:right;font-size:14px;color:var(--vt,#ffb347)}
  #sl .ev{grid-column:1/-1} #sl .e{line-height:1.9;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:.75} #sl .e:first-child{opacity:1} #sl .e .t{color:var(--vt2,#8a5a1d);margin-right:10px} #sl .e .w{color:var(--vt,#ffb347);margin-right:6px}
  @media (max-width:1100px){#sl{grid-template-columns:1fr 1fr;font-size:10px} #sl .c.svc{grid-column:1/-1}}
  @media (max-width:700px){#sl{display:none}}
  #sl,#sl *{text-shadow:0 0 3px #000,0 0 8px #000} #sl h5,#sl .r b,#sl .kv b,#sl .s em,#sl .e .t,#sl .date,#sl .net .n b{color:var(--vt,#ffb347);opacity:.72} #sl .sys{opacity:.85}
"""
HTML="""<div id="sl">
  <div class="head"><div class="l"><span class="badge">OK</span><span class="sys"></span></div><div><div class="clock">--:--:--</div><div class="date"></div></div></div>
  <div class="c"><h5>SYSTEM LOAD <span id="sl-load"></span></h5><canvas id="sl-rings" height="150"></canvas></div>
  <div class="c"><h5>STORAGE <span id="sl-disk"></span></h5><div id="sl-fs"></div></div>
  <div class="c svc"><h5>SERVICES <span id="sl-svc-n"></span></h5><div class="g" id="sl-svc"></div></div>
  <div class="c" style="grid-column:1/3"><h5>NETWORK <span id="sl-wifi"></span></h5><div class="net"><div class="n"><b>&#9660; DOWN</b><span id="sl-rx"></span><canvas id="sl-rxc" height="54"></canvas></div><div class="n"><b>&#9650; UP</b><span id="sl-tx"></span><canvas id="sl-txc" height="54"></canvas></div></div></div>
  <div class="c"><h5>ACCESS <span>LAN ONLY</span></h5><div class="kv" id="sl-acc"></div></div>
  <div class="c ev"><h5>LATEST EVENTS</h5><div id="sl-ev"></div></div>
</div>
"""
JS="""<script>
// ---------- sleep grid: the dashboard, in the Face theme, while the figure drifts
(() => {
  const $=id=>document.getElementById(id); let D=null; const rx=[],tx=[];
  const pad=n=>String(n).padStart(2,'0'); const col=()=>getComputedStyle(document.documentElement).getPropertyValue('--vt').trim()||'#ffb347';
  const col2=()=>getComputedStyle(document.documentElement).getPropertyValue('--vt2').trim()||'#8a5a1d';
  const gb=b=>(b/1073741824).toFixed(b>1e10?0:1)+' GB'; const fmt=b=>b>1e6?(b/1e6).toFixed(1)+' MB/s':b>1e3?(b/1e3).toFixed(1)+' Kb/s':Math.round(b||0)+' b/s';
  function clock(){ const d=new Date(); $('sl').querySelector('.clock').textContent=pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());
    let up=''; if(D&&D.uptime_s){ const s=D.uptime_s; up='  \\u00b7  UPTIME '+Math.floor(s/86400)+'d '+pad(Math.floor(s%86400/3600))+':'+pad(Math.floor(s%3600/60)); }
    $('sl').querySelector('.date').textContent=d.toLocaleDateString('en-GB',{weekday:'short',day:'2-digit',month:'short',year:'numeric'}).toUpperCase()+up; }
  setInterval(clock,1000); clock();
  function rings(){ const cv=$('sl-rings'); if(!cv||!document.body.classList.contains('sleep')) return; const W=cv.clientWidth||600; cv.width=W*2; cv.height=300; const x=cv.getContext('2d'); x.scale(2,2); x.clearRect(0,0,W,150);
    const C=col(),C2=col2(); const items=[['CPU',D.cpu_pct||0,Math.round(D.cpu_pct||0)+'%',D.cpu_model||''],['MEMORY',D.mem?D.mem.pct:0,Math.round(D.mem?D.mem.pct:0)+'%',D.mem?gb(D.mem.used)+' / '+gb(D.mem.total):''],
      ['ROOT DISK',(D.fs||[]).find(f=>f.mount==='/')?.pct||0,Math.round((D.fs||[]).find(f=>f.mount==='/')?.pct||0)+'%',(()=>{const f=(D.fs||[]).find(f=>f.mount==='/');return f?gb(f.used)+' / '+gb(f.total):''})()],['CPU TEMP',Math.min(100,(D.temp_c||0)),Math.round(D.temp_c||0)+'\\u00b0',(D.temp_c||0)<60?'cool':(D.temp_c||0)<75?'warm':'hot']];
    const n=items.length, cw=W/n; items.forEach((it,i)=>{ const cx=cw*i+cw/2, cy=58, r=40; x.lineWidth=5; x.strokeStyle=C2; x.globalAlpha=.35; x.beginPath(); x.arc(cx,cy,r,0,Math.PI*2); x.stroke(); x.globalAlpha=1; x.strokeStyle=C; x.shadowColor=C; x.shadowBlur=10; x.beginPath(); x.arc(cx,cy,r,-Math.PI/2,-Math.PI/2+Math.PI*2*Math.max(0,Math.min(1,it[1]/100))); x.stroke(); x.shadowBlur=0;
      x.fillStyle='#d6eeff'; x.font='600 16px IBM Plex Mono,monospace'; x.textAlign='center'; x.fillText(it[2],cx,cy+6); x.fillStyle=C2; x.font='9px IBM Plex Mono,monospace'; x.fillText(it[0],cx,cy+r+18); x.fillStyle='#8aa4bb'; x.fillText(String(it[3]).slice(0,26),cx,cy+r+32); }); }
  function spark(id,arr){ const cv=$(id); if(!cv) return; const W=cv.clientWidth||300; cv.width=W*2; cv.height=108; const x=cv.getContext('2d'); x.scale(2,2); x.clearRect(0,0,W,54); if(arr.length<2) return; const mx=Math.max(1,...arr); x.strokeStyle=col(); x.lineWidth=1.5; x.shadowColor=col(); x.shadowBlur=6; x.beginPath(); arr.forEach((v,i)=>{ const px=i/(arr.length-1)*W, py=50-v/mx*44; i?x.lineTo(px,py):x.moveTo(px,py); }); x.stroke(); }
  window.fbSleepHud=function(data){ D=data; if(!D) return; const sl=$('sl'); if(!sl) return;
    const lv=(window.fbStatus&&window.fbStatus.level)||'ok'; sl.querySelector('.badge').textContent=lv==='bad'?'CRITICAL':lv==='warn'?'DEGRADED':'ALL SYSTEMS OK';
    sl.querySelector('.sys').textContent=[D.model,D.os,D.kernel?'KERNEL '+D.kernel:''].filter(Boolean).join('  \\u00b7  ').toUpperCase();
    $('sl-load').textContent=(D.load||[]).map(v=>Number(v).toFixed(2)).join('  \\u00b7  ');
    $('sl-disk').textContent=D.disk_model||''; const fs=D.fs||[]; let h='';
    for(const f of fs) h+='<div class="r"><b>'+f.mount+'</b><i style="--w:'+Math.round(f.pct||0)+'%"></i><span>'+gb(f.free)+' free</span></div>';
    if(D.lvm_free_gb!=null) h+='<div class="r"><b>LVM free</b><i style="--w:6%"></i><span>'+D.lvm_free_gb+' GB idle</span></div>';
    if(D.swap&&D.swap.total) h+='<div class="r"><b>swap</b><i style="--w:'+Math.round(D.swap.used/D.swap.total*100)+'%"></i><span>'+(D.swap.used/1048576).toFixed(0)+' MB / '+(D.swap.total/1073741824).toFixed(1)+' GB</span></div>';
    h+='<div class="r"><b>SMART</b><i style="--w:100%"></i><span>'+(D.smart||'')+'</span></div><div class="r"><b>last backup</b><i style="--w:100%"></i><span>'+(D.backup_last||'')+'</span></div>'; $('sl-fs').innerHTML=h;
    const sv=D.services||[]; $('sl-svc-n').textContent=sv.filter(s=>s.state==='ok').length+' / '+sv.length+' OK';
    let sh=sv.map(s=>'<div class="s'+(s.state==='ok'?'':' bad')+'"><span><i></i>'+s.name+'</span><em>'+(s.detail||s.state||'')+'</em></div>').join('');
    if(D.failed_units&&!sv.some(s=>/failed/i.test(s.name))) sh+='<div class="s bad"><span><i></i>failed units</span><em>'+D.failed_units+'</em></div>'; $('sl-svc').innerHTML=sh;
    rx.push(D.net?D.net.rx_bps||0:0); tx.push(D.net?D.net.tx_bps||0:0); if(rx.length>60){rx.shift();tx.shift();}
    $('sl-rx').textContent=fmt(rx[rx.length-1]); $('sl-tx').textContent=fmt(tx[tx.length-1]); $('sl-wifi').textContent=D.net&&D.net.signal_dbm?'WI-FI \\u00b7 '+D.net.signal_dbm+' DBM':'';
    const n=D.net||{}, ss=D.sessions||{}, pw=D.power||{};
    $('sl-acc').innerHTML=[['address',n.ip],['gateway',n.gw],['interface',n.iface],['sessions',(ss.ssh||0)+' ssh \\u00b7 '+(ss.cockpit||0)+' cockpit'],['last login',D.last_login||'\\u2014'],['failed',(D.failed_logins_7d||0)+' in 7 days'],['updates',(D.updates_pending||0)+' pending'+(D.reboot_required?' \\u00b7 reboot':'')],['power',(pw.status||pw.ac?'AC':'')+(pw.battery_pct!=null?' \\u00b7 '+pw.battery_pct+'%':'')]].filter(k=>k[1]!=null&&k[1]!=='').map(k=>'<b>'+k[0]+'</b><span>'+k[1]+'</span>').join('');
    const ev=(D.events||[]).slice(0,5); $('sl-ev').innerHTML=ev.length?ev.map(e=>'<div class="e"><span class="t">'+(e.t||'')+'</span>'+(e.level&&e.level!=='info'?'<span class="w">&#9650;</span>':'')+e.msg+'</div>').join(''):'<div class="e">no events</div>';
    clock(); if(document.body.classList.contains('sleep')){ rings(); spark('sl-rxc',rx); spark('sl-txc',tx); } };
  new MutationObserver(()=>{ if(document.body.classList.contains('sleep')&&D){ rings(); spark('sl-rxc',rx); spark('sl-txc',tx); } }).observe(document.body,{attributes:true,attributeFilter:['class']});
  addEventListener('resize',()=>{ if(D&&document.body.classList.contains('sleep')){ rings(); spark('sl-rxc',rx); spark('sl-txc',tx); } });
})();
</script>
"""
def unhud(s):
    s=re.sub(r"  body\.sleep \.vt\{display:block!important\}\n.*?@media \(max-width:900px\)\{#sl-services,#sl-events\{display:none\}\}\n","",s,count=1,flags=re.S)
    s=re.sub(r'<div id="sl-top" class="sl">.*?<div id="sl-events" class="sl">.*?</div></div></div>\n',"",s,count=1,flags=re.S)
    s=re.sub(r"<script>\n(// ---------- sleep HUD[^\n]*\n)?\(\(\) => \{\n  const \$=id=>document\.getElementById\(id\); let D=null;\n.*?\}\)\(\);\n</script>\n","",s,count=1,flags=re.S)
    return s
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'id="sl-rings"' in s: print(f,'already patched'); continue
    s=unhud(s)
    if 'sl-services' in s: sys.exit(f+': old sleep HUD not fully removed')
    if s.count('</style>')!=1 or s.count('<div id="vt-store" class="vt">')!=1: sys.exit(f+': anchors')
    if 'fbSleepHud(D)' not in s or "classList.toggle('sleep'" not in s: sys.exit(f+': needs patch_sleephud hooks (fbSleepHud / body.sleep)')
    s=s.replace('</style>',CSS+'</style>',1).replace('<div id="vt-store" class="vt">',HTML+'<div id="vt-store" class="vt">',1)
    s=s.replace('</body>',JS+'</body>',1) if '</body>' in s else s.rstrip('\n')+'\n'+JS
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
