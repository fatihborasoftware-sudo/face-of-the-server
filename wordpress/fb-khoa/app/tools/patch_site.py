#!/usr/bin/env python3
# patch_site.py - turns face-of-the-server v1.2 index.html into khoa-web.html for the public site (khoa.fbserver.net)
#   demo data only · recorded voice clips (EN + TR) · ?lang=tr · ?embed=hero|full · postMessage API · lite on phones
import sys, json, re
sys.path.insert(0, '.')
from texts import TR
import web_i18n
TR = dict(TR); TR.update(web_i18n.EXTRA_TR)

src = open(sys.argv[1], encoding='utf-8').read()
clips = json.load(open('clips.json', encoding='utf-8'))
out = src

def rep(old, new, count=1):
    global out
    n = out.count(old)
    if n != count:
        raise SystemExit('anchor found %d times (want %d): %r' % (n, count, old[:90]))
    out = out.replace(old, new)

def K(s):  # wrap an English literal for translation
    return "KT(%s)" % json.dumps(s, ensure_ascii=False)

# ---- 0. head: flags, language, translations, clip map
head = """<script>
window.FB_WEB=true;
(function(){ var q=location.search, m=q.match(/[?&]lang=(en|tr)/), L=m?m[1]:null; try{ if(!L) L=localStorage.getItem('khoaLang'); }catch(e){} window.KHOA_LANG=(L==='tr')?'tr':'en';
  var e=q.match(/[?&]embed=(hero|full)/); window.KHOA_EMBED=e?e[1]:(/[?&]embed/.test(q)?'hero':null); document.documentElement.lang=window.KHOA_LANG;
  document.documentElement.classList.add('web'); if(window.KHOA_EMBED) document.documentElement.classList.add('embed-'+window.KHOA_EMBED); })();
window.KHOA_TR=%s;
window.KT=function(s){ return (window.KHOA_LANG==='tr'&&window.KHOA_TR[s])?window.KHOA_TR[s]:s; };
window.KHOA_CLIPS=%s;
window.khoaClip=function(t){ return window.KHOA_CLIPS[t]||null; };
</script>
<style>
  html.web #sl .c h5 span:empty{display:none}
  html.embed-hero .hud, html.embed-hero #sl, html.embed-hero .note, html.embed-hero .gaze, html.embed-hero .meter{display:none!important}
  html.embed-hero .bar, html.embed-hero .sitmenu, html.embed-hero .caption{display:none!important}
  html.embed-full .bar button[data-mode], html.embed-full #speak, html.embed-full #voice{display:none}
  html.web .bar button{font-size:11px;padding:10px 14px;min-height:40px}
  html.embed-hero body.live .bar, html.embed-hero body.cine .bar{opacity:.18!important}
  @media (max-width:700px){ html.embed-full .bar, html.embed-full .sitmenu{display:none!important} html.embed-hero .status{display:none} }
</style>
""" % (json.dumps(TR, ensure_ascii=False), json.dumps(clips, ensure_ascii=False))
rep('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap">',
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap">\n' + head)
rep('<title>Face of the Server</title>', '<title>Khoa · the face of the server</title>')

rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', '<script src="three.min.js"></script>')

# ---- 1. lite on phones / touch screens
rep("const LITE=/[?&]lite/.test(location.search)||/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname);",
    "const LITE=/[?&]lite/.test(location.search)||/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname)||matchMedia('(pointer:coarse)').matches||innerWidth<760;")

# ---- 2. no home server: no TTS server, no queue, demo data only
rep("window.fbTTS=(location.protocol==='https:'&&/^(192\\.168\\.1\\.146|fbserver(\\.local)?)$/.test(location.hostname))?'/khoa/':(/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname)?'http://127.0.0.1:8082/':'https://192.168.1.146/khoa/');",
    "window.fbTTS='';")
rep("fetch(window.fbTTS+'say?text='+encodeURIComponent(text)+'&v='+encodeURIComponent(srv)+'&len='+(window.FB_VOICE_LEN||1.0),{signal:ctrl.signal})",
    "(window.khoaClip(text)?fetch(window.khoaClip(text),{signal:ctrl.signal}):Promise.reject(0))")
rep("try{ const r=await fetch('../data.json?t='+Date.now(),{cache:'no-store'});", "try{ if(window.FB_WEB) throw 0; const r=await fetch('../data.json?t='+Date.now(),{cache:'no-store'});")
rep("try{ const r=await fetch('data.json?t='+Date.now(),{cache:'no-store'});", "try{ if(window.FB_WEB) throw 0; const r=await fetch('data.json?t='+Date.now(),{cache:'no-store'});")
rep("backup_last:'26 Sep 08:48',", "backup_last:'03:00 · 28 GB',")
rep("disk_model:'WDC WD10JPCX-24U · 1 TB'}; }",
    "disk_model:'WDC WD10JPCX-24U · 1 TB',model:'Lenovo IdeaPad',os:'Ubuntu 26.04 LTS',cpu_model:'Intel Core i5-7200U',uptime_s:Math.floor(t%604800)+86400*3,"
    "sessions:{ssh:0,cockpit:0},updates_pending:26,failed_logins_7d:0,power:{ac:1,battery_pct:100},last_login:'—',"
    "services:[['ssh',':22'],['cockpit',':9090'],['networkd','wi-fi'],['resolved','dns'],['chrony','time'],['unattended','daily'],['thermald','active'],['cron','active'],['smartd','active'],['firewall','active'],['nginx',':443'],['fbweb','active']].map(s=>({name:s[0],state:'ok',detail:s[1]})),"
    "events:[{t:'demo',msg:'This is a demo server. The real one stays at home.'}]}; }")
rep('<h5>ACCESS <span>LAN ONLY</span></h5>', '<h5>ACCESS <span>DEMO</span></h5>')

# ---- 3. fixed, translatable lines
rep("window.fbSay('Khoa online. '+window.fbStatusLine()); } else window.fbSay('Back. '+window.fbStatusLine()); };",
    "window.fbSay(KT('Khoa online. All systems nominal.')); } else window.fbSay(KT('Back. All systems nominal.')); };")
rep("window.fbSay('Welcome back.');", "window.fbSay(KT('Welcome back.'));")
rep("let firstWake=true; window.fbOnWake=function(){ if(window.fbIntroQuiet||window.fbSit) return;",
    "let firstWake=true; window.fbOnWake=function(){ if(window.fbIntroQuiet||window.fbSit||window.KHOA_EMBED==='hero') return;")
rep("let lastSeen=0; window.fbSeen=function(){ const n=performance.now();",
    "let lastSeen=0; window.fbSeen=function(){ if(window.KHOA_EMBED==='hero') return; const n=performance.now();")
rep("window.fbSay('Khoa back online.',{force:true});", "window.fbSay(KT('Khoa back online.'),{force:true});")
rep("setInterval(()=>{ const d=new Date(); if(d.getMinutes()===0", "setInterval(()=>{ if(window.FB_WEB) return; const d=new Date(); if(d.getMinutes()===0")
say_old = out[out.index("const SAY={ normal:"):out.index("const DEMO={")]
say_new = ("const SAY={ normal:()=>" + K('Situation cleared. All systems nominal.') + ",\n"
  "    backup:v=>" + K('Backup running. Twenty eight gigabytes to the backup disk.') + ",\n"
  "    intrusion:v=>" + K('Intrusion detected. Forty eight failed logins. Firewall holding.') + ",\n"
  "    heat:v=>" + K('Warning. CPU temperature ninety three degrees. Throttling. Cooling required.') + ",\n"
  "    memory:v=>" + K('Memory pressure. Ninety seven percent used. Swapping to disk.') + ",\n"
  "    ssd:v=>" + K('Disk almost full. Four gigabytes left on root.') + ",\n"
  "    load:v=>" + K('High load. All four cores busy.') + ",\n"
  "    update:v=>" + K('System update in progress. Twenty seven packages. Reboot after.') + ",\n"
  "    alarm:v=>" + K('Service down. Nginx, fbweb and cockpit are not responding.') + " };\n  ")
rep(say_old, say_new)

# intro
for a in ["'FB SERVER','LENOVO IDEAPAD  ·  UBUNTU  ·  HOME OF THE CREW'"]:
    rep("title(" + a + ")", "title(KT('FB SERVER'),KT('LENOVO IDEAPAD  ·  UBUNTU  ·  HOME OF THE CREW'))")
rep("await say('I am Khoa. The face of the server.');", "await say(KT('I am Khoa. The face of the server.'));")
rep("await say('This machine is F B Server. A Lenovo IdeaPad running Ubuntu, kept alive by a crew of eight agents. I am its body. Let me show you what I watch.');",
    "await say(KT('This machine is FB Server. A Lenovo IdeaPad running Ubuntu, kept alive by a crew of eight agents. I am its body. Let me show you what I watch.'));")
rep("await say('Situation cleared. All systems nominal. This is F B Server. I am Khoa, and I am watching.');",
    "await say(KT('Situation cleared. All systems nominal. This is FB Server. I am Khoa, and I am watching.'));")
rep("title('ALL SYSTEMS NOMINAL','KHOA  ·  THE FACE OF THE SERVER');", "title(KT('ALL SYSTEMS NOMINAL'),KT('KHOA  ·  THE FACE OF THE SERVER'));")
rep("titleL('ALL SYSTEMS NOMINAL','KHOA &middot; THE FACE OF THE SERVER');", "titleL(KT('ALL SYSTEMS NOMINAL'),KT('KHOA &middot; THE FACE OF THE SERVER'));")
rep("[name.toUpperCase(),'SITUATION']:['KHOA','THE FACE OF THE SERVER']", "[name.toUpperCase(),KT('SITUATION')]:['KHOA',KT('THE FACE OF THE SERVER')]")
steps_old = out[out.index("const STEPS=["):out.index("  // ---------- LIVE:")]
def kt_all(block):
    return re.sub(r"'([^']+)'", lambda m: ("KT('%s')" % m.group(1)) if m.group(1) in TR or m.group(1) in ('BACKUP',) else m.group(0), block)
rep(steps_old, kt_all(steps_old))

# situation labels + gauge titles; no IP address on the public site
sit_old = out[out.index("  const SIT={"):out.index("  const ORDER=['normal'")]
sit_new = re.sub(r"(label|title):'([^']+)'", lambda m: "%s:KT('%s')" % (m.group(1), m.group(2)) if m.group(2) in TR else m.group(0), sit_old)
sit_new = sit_new.replace("FAILED LOGINS  \\u00b7  185.220.101.7", "FAILED LOGINS  \\u00b7  FIREWALL HOLDING")
rep(sit_old, sit_new)

# ---- 4. pause from the parent page (hero scrolled out of view)
rep("document.addEventListener('visibilitychange',()=>{running=!document.hidden;if(running){last=performance.now();requestAnimationFrame(tick);}});",
    "document.addEventListener('visibilitychange',()=>{const was=running; running=!document.hidden&&!window.fbPaused; if(running&&!was){last=performance.now();requestAnimationFrame(tick);}});\n"
    "  window.fbPauseSet=p=>{ window.fbPaused=!!p; const was=running; running=!p&&!document.hidden; if(running&&!was){last=performance.now();requestAnimationFrame(tick);} };")

# ---- 4b. hero framing: on wide screens the figure stands right of centre, leaving room for the page title
rep("camera.lookAt(0,-0.45,0);camera.updateProjectionMatrix();",
    "camera.lookAt(0,-0.45,0); if(window.KHOA_EMBED==='hero'&&w>900) camera.setViewOffset(w,h,-Math.round(w*0.16),0,w,h); else camera.clearViewOffset(); camera.updateProjectionMatrix();")

# ---- 5. web layer: button labels, browser-voice language, parent API, hero framing
web = r"""
<script>
// ---------- WEB LAYER (khoa.fbserver.net): language, parent-page API, hero framing
(() => {
  const L=window.KHOA_LANG;
  const relabel=()=>document.querySelectorAll('.bar button').forEach(b=>{ const t=b.textContent.trim(); if(!b.dataset.en) b.dataset.en=t; b.textContent=KT(b.dataset.en); });
  addEventListener('load',()=>setTimeout(relabel,50));
  // browser fallback voice in the visitor's language
  const PREF=/(Daniel|George|Arthur|Ryan|Guy|Christopher|Male|Google UK English Male|Tolga|Ahmet)/i;
  window.fbVoice=()=>{ let vs=[]; try{ vs=speechSynthesis.getVoices(); }catch(e){} if(L==='tr') return vs.find(v=>/^tr/i.test(v.lang)&&/Tolga|Ahmet|male/i.test(v.name))||vs.find(v=>/^tr/i.test(v.lang))||null;
    return vs.find(x=>/en-GB/i.test(x.lang)&&PREF.test(x.name))||vs.find(x=>/en-GB/i.test(x.lang))||vs.find(x=>/^en/i.test(x.lang))||null; };
  // tell the parent page when Khoa takes the stage (so it can fade its own title)
  const post=m=>{ try{ if(parent!==window) parent.postMessage(Object.assign({khoa:1},m),'*'); }catch(e){} };
  let lastOn=null; new MutationObserver(()=>{ const on=document.body.classList.contains('live')||document.body.classList.contains('cine'); if(on!==lastOn){ lastOn=on; post({stage:on}); } }).observe(document.body,{attributes:true,attributeFilter:['class']});
  addEventListener('load',()=>post({ready:true}));
  // commands from the parent page
  addEventListener('message',e=>{ const d=e.data; if(!d||typeof d!=='object'||!d.khoa) return;
    if(window.fbTouch) window.fbTouch();
    if(d.cmd==='intro'&&window.fbIntro) window.fbIntro();
    else if(d.cmd==='sit'&&window.fbSituation&&typeof d.name==='string') window.fbSituation(d.name);
    else if(d.cmd==='pause'&&window.fbPauseSet) window.fbPauseSet(!!d.on);
    else if(d.cmd==='quiet'){ try{ speechSynthesis.cancel(); }catch(_){} try{ if(window.fbAudio) window.fbAudio.pause(); }catch(_){} }
    else if(d.cmd==='scary'){ const b=document.getElementById('scary'); if(b) b.click(); } });
})();
</script>
"""
rep("</body>", web + "</body>")
out = web_i18n.canvas_labels(out)
rep('</body>', web_i18n.DOM_JS + '</body>')
open(sys.argv[2], 'w', encoding='utf-8').write(out)
print('ok', len(src), '->', len(out))
