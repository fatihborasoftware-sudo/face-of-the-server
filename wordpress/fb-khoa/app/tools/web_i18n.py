# Shared Turkish layer for khoa-web.html and map-web.html: canvas labels (at the source) + a DOM text translator.
import re

EXTRA_TR = {'CPU': 'İŞLEMCİ', 'MEMORY': 'BELLEK', 'ROOT DISK': 'KÖK DİSK', 'CPU TEMP': 'İŞLEMCİ ISISI',
            'cool': 'serin', 'warm': 'ılık', 'hot': 'sıcak',
            'ASSEMBLING... ': 'OLUŞUYOR... ', 'STATUS: ': 'DURUM: ', 'IDLE': 'BEKLEMEDE', 'SPEAKING': 'KONUŞUYOR',
            'LISTENING': 'DİNLİYOR', 'THINKING': 'DÜŞÜNÜYOR', 'STATUS: DRIFTING': 'DURUM: SÜZÜLÜYOR'}

def canvas_labels(out):
    """Wrap the labels drawn on canvases in KT() so they follow the language."""
    out, n1 = re.subn(r",'(CPU|MEMORY|ROOT DISK|CPU TEMP)',Math", r",KT('\1'),Math", out)
    out, n2 = re.subn(r"\['(CPU|MEMORY|ROOT DISK|CPU TEMP)',", r"[KT('\1'),", out)
    out, n3 = re.subn(r"t<60\?'cool':t<80\?'warm':'hot'", "KT(t<60?'cool':t<80?'warm':'hot')", out)
    out, n4 = re.subn(r"\(D\.temp_c\|\|0\)<60\?'cool':\(D\.temp_c\|\|0\)<75\?'warm':'hot'", "KT((D.temp_c||0)<60?'cool':(D.temp_c||0)<75?'warm':'hot')", out)
    out = out.replace("statusEl.textContent='ASSEMBLING... '+", "statusEl.textContent=KT('ASSEMBLING... ')+")
    out = out.replace("statusEl.textContent='STATUS: '+s.toUpperCase()", "statusEl.textContent=KT('STATUS: ')+KT(s.toUpperCase())")
    out = out.replace("statusEl.textContent='STATUS: DRIFTING'", "statusEl.textContent=KT('STATUS: DRIFTING')")
    if n1 + n3 == 0:
        raise SystemExit('canvas labels not found')
    return out

DOM_JS = r"""
<script>
// ---------- Turkish for the dashboard texts (HUD, dashboard, status line, footer)
(() => {
  if(window.KHOA_LANG!=='tr') return;
  const EX={'ACCESS':'ERİŞİM','ALL SYSTEMS OK':'TÜM SİSTEMLER NORMAL','DEGRADED':'SORUNLU','CRITICAL':'KRİTİK','LATEST EVENTS':'SON OLAYLAR',
    'NETWORK':'AĞ','SERVICES':'SERVİSLER','STORAGE':'DEPOLAMA','SYSTEM LOAD':'SİSTEM YÜKÜ','PASSED':'GEÇTİ','LVM free':'LVM boş',
    'last':'son','backup':'yedek','last backup':'son yedek','last login':'son giriş','sessions':'oturumlar','failed':'başarısız','updates':'güncellemeler',
    'power':'güç','address':'adres','gateway':'ağ geçidi','interface':'arayüz','active':'aktif','daily':'günlük','time':'saat','swap':'takas',
    '▼ DOWN':'▼ İNDİRME','▲ UP':'▲ YÜKLEME','♪ VOICE':'♪ SES','no events':'olay yok','DEMO':'DEMO',
    'This is a demo server. The real one stays at home.':'Bu bir demo sunucu. Gerçeği evde kalıyor.',
    'KHOA · THE FACE OF THE SERVER':'KHOA · SUNUCUNUN YÜZÜ','KHOA · THE FACE OF THE SERVER ':'KHOA · SUNUCUNUN YÜZÜ',
    'ECORCHE MESH BY DIEGO LUJÁN GARCÍA (CC-BY, SKETCHFAB) · PARTICLE BODY · BLOOM':'ÉCORCHÉ MODELİ: DIEGO LUJÁN GARCÍA (CC-BY, SKETCHFAB) · PARÇACIK BEDEN · IŞIMA',
    'IT FOLLOWS THE MOUSE NOW · THE WEBCAM LATER, SAME CODE':'FAREYİ TAKİP EDER · WEB KAMERASIYLA DA, AYNI KOD'};
  const ST={IDLE:'BEKLEMEDE',SPEAKING:'KONUŞUYOR',LISTENING:'DİNLİYOR',THINKING:'DÜŞÜNÜYOR'};
  const DAY={MON:'PZT',TUE:'SAL',WED:'ÇAR',THU:'PER',FRI:'CUM',SAT:'CMT',SUN:'PAZ'};
  const MON={JAN:'OCA',FEB:'ŞUB',MAR:'MAR',APR:'NİS',MAY:'MAY',JUN:'HAZ',JUL:'TEM',AUG:'AĞU',SEPT:'EYL',SEP:'EYL',OCT:'EKİ',NOV:'KAS',DEC:'ARA'};
  const LOOK={'YOU (MOUSE)':'SANA (FARE)','AROUND THE ROOM':'ODANIN ÇEVRESİNE','MOUSE':'FARE'};
  const RX=[
    [/^(\d+) in 7 days$/, (m,a)=>a+' / 7 gün'],
    [/^(.+) free$/, (m,a)=>a+' boş'],
    [/^(.+) idle$/, (m,a)=>a+' boşta'],
    [/^(\d+) pending(.*)$/, (m,a,b)=>a+' bekliyor'+b.replace('reboot','yeniden başlat')],
    [/^(\d+ \/ \d+) OK$/, (m,a)=>a+' TAMAM'],
    [/^STATUS: (\w+)$/, (m,a)=>'DURUM: '+(ST[a]||a)],
    [/^ASSEMBLING\.\.\. (\d+)%$/, (m,a)=>'OLUŞUYOR... '+a+'%'],
    [/^LOOKING AT · (.+)$/, (m,a)=>'BAKIYOR · '+(LOOK[a]||a.replace('YOU','SANA').replace('CAMERA','KAMERA').replace('FACE','YÜZ').replace('MOTION','HAREKET'))],
    [/^([A-Z]{3}), (\d+) ([A-Z]{3,4}) (\d{4})(.*)$/, (m,d,n,mo,y,rest)=>(DAY[d]||d)+', '+n+' '+(MON[mo]||mo)+' '+y+rest.replace('UPTIME','ÇALIŞMA')],
    [/^(\d+) ssh · (\d+) cockpit$/, (m,a,b)=>a+' ssh · '+b+' cockpit'],
  ];
  const tr=s=>{ const t=s.trim(); if(!t) return null; if(EX[t]) return s.replace(t,EX[t]); for(const [re,f] of RX){ const m=t.match(re); if(m) return s.replace(t,f(...m)); } return null; };
  const walk=root=>{ const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT); let n; while((n=w.nextNode())){ const p=n.parentElement; if(!p||p.closest('script,style')) continue; const v=tr(n.nodeValue); if(v!==null&&v!==n.nodeValue) n.nodeValue=v; } };
  const run=()=>walk(document.body);
  let q=false; const obs=new MutationObserver(()=>{ if(q) return; q=true; requestAnimationFrame(()=>{ q=false; obs.disconnect(); run(); obs.observe(document.body,{subtree:true,childList:true,characterData:true}); }); });
  addEventListener('load',()=>{ run(); obs.observe(document.body,{subtree:true,childList:true,characterData:true}); });
})();
</script>
"""
