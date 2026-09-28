#!/usr/bin/env python3
# patch_map.py - turns face-of-the-server v1.2 map.html (the Command Map) into map-web.html for khoa.fbserver.net
#   demo data · crew cards built in · demo crew that "speaks" in turn · ?lang=tr · ?embed=full · postMessage pause API
import sys, json
sys.path.insert(0, '.')
from map_texts import MAP_TR, UI_TR
from texts import TR
import web_i18n
TR = dict(TR); TR.update(web_i18n.EXTRA_TR)

src = open(sys.argv[1], encoding='utf-8').read()
out = src

def rep(old, new, count=1):
    global out
    n = out.count(old)
    if n != count:
        raise SystemExit('anchor found %d times (want %d): %r' % (n, count, old[:90]))
    out = out.replace(old, new)

TRX = dict(TR); TRX.update(UI_TR)
head = """<script>
window.FB_WEB=true;
(function(){ var q=location.search, m=q.match(/[?&]lang=(en|tr)/), L=m?m[1]:null; try{ if(!L) L=localStorage.getItem('khoaLang'); }catch(e){} window.KHOA_LANG=(L==='tr')?'tr':'en';
  var e=q.match(/[?&]embed=(hero|full)/); window.KHOA_EMBED=e?e[1]:null; document.documentElement.lang=window.KHOA_LANG;
  document.documentElement.classList.add('web'); if(window.KHOA_EMBED) document.documentElement.classList.add('embed-'+window.KHOA_EMBED); })();
window.KHOA_TR=%s; window.KHOA_MAP_TR=%s;
window.KT=function(s){ return (window.KHOA_LANG==='tr'&&window.KHOA_TR[s])?window.KHOA_TR[s]:s; };
window.khoaCard=function(k){ return (window.THUMBS&&window.THUMBS[k])||''; };
</script>
<style>
  html.web .bar button[data-mode], html.web #speak{display:none}
  html.web .bar button{font-size:11px;padding:10px 14px;min-height:40px}
  html.web .card .idc{display:none!important}
  html.web .spot{aspect-ratio:auto!important;width:auto!important;object-fit:contain!important;background:none!important;border-radius:8px!important}
  html.web .card .side{background:none!important;object-fit:contain!important;border-radius:8px!important;height:auto!important}
  @media (max-width:700px){ html.web .bar{display:none!important} html.web .maplbl{display:none} html.web .node.app{display:none} html.web .node .lbl{font-size:11px} }
</style>
""" % (json.dumps(TRX, ensure_ascii=False), json.dumps(MAP_TR, ensure_ascii=False))
rep('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap">',
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap">\n' + head)
rep('<title>FB Server Command Map</title>', '<title>Khoa · Command Map</title>')
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', '<script src="three.min.js"></script>')
rep("const LITE=/[?&]lite/.test(location.search)||/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname);",
    "const LITE=/[?&]lite/.test(location.search)||/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname)||matchMedia('(pointer:coarse)').matches||innerWidth<760;")
# cleaned crew cards: white/grey rims trimmed, rounded transparent corners (thumbs_clean.json from clean_thumbs step)
import re as _re
_clean=json.load(open('thumbs_clean.json'))
_m=_re.search(r'window\.THUMBS=(\{.*?\});', out)
if not _m: raise SystemExit('THUMBS not found')
out=out.replace(_m.group(1), json.dumps(_clean))

# demo data only
rep("try{ const r=await fetch('../data.json?t='+Date.now(),{cache:'no-store'});", "try{ if(window.FB_WEB) throw 0; const r=await fetch('../data.json?t='+Date.now(),{cache:'no-store'});")
rep("try{ const r=await fetch('data.json?t='+Date.now(),{cache:'no-store'});", "try{ if(window.FB_WEB) throw 0; const r=await fetch('data.json?t='+Date.now(),{cache:'no-store'});")
rep("backup_last:'26 Sep 08:48',", "backup_last:'03:00 · 28 GB',")
# crew cards from the built-in thumbnails (no server images on the public site)
rep("src=root+'crew/card-'+key+'.png'; im.style.setProperty('--c',n.c);", "src=window.khoaCard(key); im.style.setProperty('--c',n.c);")
rep("const sideSrc=(!n.app&&n.spk)?root+'crew/card-'+n.spk[0]+'.png':'';", "const sideSrc=(!n.app&&n.spk)?window.khoaCard(n.spk[0]):'';")
rep("n._img=root+'crew/card-'+key+'.png';", "n._img=window.khoaCard(n.spk[0]);")
rep("<h6>WHAT IT HANDLES</h6>", "<h6>${KT('WHAT IT HANDLES')}</h6>")
rep("<h6>EXAMPLE REQUESTS</h6>", "<h6>${KT('EXAMPLE REQUESTS')}</h6>")
rep("<div class=\"spk\"><small>SPEAKING</small>", "<div class=\"spk\"><small>'+KT('SPEAKING')+'</small>")
rep('<div class="role">COMMAND MAP · THE FACE OF THE SERVER</div>', '<div class="role" data-kt="COMMAND MAP · THE FACE OF THE SERVER">COMMAND MAP · THE FACE OF THE SERVER</div>')
rep('<div class="maplbl">CLICK A NODE · THE CREW AND THE APPS OF FBSERVER</div>', '<div class="maplbl" data-kt="CLICK A NODE · THE CREW AND THE APPS OF FBSERVER">CLICK A NODE · THE CREW AND THE APPS OF FBSERVER</div>')
# Turkish node texts
rep("  const map=document.getElementById('map'), svg=document.getElementById('wires'), card=document.getElementById('card');",
    "  if(window.KHOA_LANG==='tr'&&window.KHOA_MAP_TR) N.forEach(n=>{ const t=window.KHOA_MAP_TR[n.id]; if(t) Object.assign(n,t); });\n"
    "  const map=document.getElementById('map'), svg=document.getElementById('wires'), card=document.getElementById('card');")
# no /speaking on the public site: a demo crew speaks in turn instead
rep("setInterval(pollSpeaking,500);",
    "if(!window.FB_WEB) setInterval(pollSpeaking,500);\n"
    "  if(window.FB_WEB){ const crew=['serra','watchman','locke','corren','quill','dusk','relay','mason']; let ci=Math.floor(Math.random()*crew.length);\n"
    "    const turn=()=>{ if(window.fbPaused||document.hidden||cur||talking){ return; } const k=crew[ci++%crew.length]; showTalking(k); setTimeout(()=>showTalking(''),6500); };\n"
    "    setTimeout(turn,9000); setInterval(turn,15000); }")
rep("    for(const [n,d] of els){ const x=n.x*W, y=n.y*H;", "    for(const [n,d] of els){ if(n.app&&window.FB_WEB&&W<700) continue; const x=n.x*W, y=n.y*H;")
# pause from the parent page
rep("document.addEventListener('visibilitychange',()=>{running=!document.hidden;if(running){last=performance.now();requestAnimationFrame(tick);}});",
    "document.addEventListener('visibilitychange',()=>{const was=running; running=!document.hidden&&!window.fbPaused; if(running&&!was){last=performance.now();requestAnimationFrame(tick);}});\n"
    "  window.fbPauseSet=p=>{ window.fbPaused=!!p; const was=running; running=!p&&!document.hidden; if(running&&!was){last=performance.now();requestAnimationFrame(tick);} };")
web = r"""
<script>
// ---------- WEB LAYER (khoa.fbserver.net): language, parent-page API
(() => {
  document.querySelectorAll('[data-kt]').forEach(e=>{ e.textContent=KT(e.getAttribute('data-kt')); });
  const relabel=()=>document.querySelectorAll('.bar button').forEach(b=>{ const t=b.textContent.trim(); if(!b.dataset.en) b.dataset.en=t; b.textContent=KT(b.dataset.en); });
  addEventListener('load',()=>setTimeout(relabel,50));
  const post=m=>{ try{ if(parent!==window) parent.postMessage(Object.assign({khoa:1},m),'*'); }catch(e){} };
  addEventListener('load',()=>post({ready:true,panel:'map'}));
  addEventListener('message',e=>{ const d=e.data; if(!d||typeof d!=='object'||!d.khoa) return;
    if(d.cmd==='pause'&&window.fbPauseSet) window.fbPauseSet(!!d.on);
    else if(d.cmd==='talk'&&window.fbTalk&&typeof d.name==='string') window.fbTalk(d.name);
    else if(d.cmd==='scary'){ const b=document.getElementById('scary'); if(b) b.click(); } });
})();
</script>
"""
rep("</body></html>", web + "</body></html>")
out = web_i18n.canvas_labels(out)
rep('</body>', web_i18n.DOM_JS + '</body>')
open(sys.argv[2], 'w', encoding='utf-8').write(out)
print('ok', len(src), '->', len(out))
