#!/usr/bin/env python3
# patch_wake.py - when the body is awake, the dashboard sits in two columns left and right of the figure and
# glitters in (staggered shimmer); asleep it goes back to the full grid. Applies after patch_edge.py. Idempotent.
import sys
CSS="""  #sl.side{display:flex;justify-content:space-between;align-items:flex-start;max-width:none;opacity:1;filter:none!important;transform:none!important;letter-spacing:.06em!important}
  #sl.side .col{width:26vw;display:flex;flex-direction:column;gap:6px} #sl.side .col.R{padding-top:34px}
  #sl.side .c,#sl.side .head{grid-column:auto!important;width:100%;box-sizing:border-box}
  @keyframes glit{0%{opacity:0;filter:blur(8px) brightness(3);letter-spacing:.5em;transform:translateY(18px) scale(1.04)}35%{opacity:1;filter:blur(1px) brightness(2.2);text-shadow:0 0 22px var(--vt,#ffb347),0 0 40px var(--vt,#ffb347)}100%{opacity:1;filter:none;letter-spacing:.06em;transform:none}}
  #sl.side.in .c,#sl.side.in .head{animation:glit 1.4s cubic-bezier(.2,.8,.2,1) both}
"""
JS="""<script>
// ---------- awake layout: the dashboard in two columns beside the body, glittering in
(() => { const sl=document.getElementById('sl'); if(!sl) return;
  const colL=document.createElement('div'), colR=document.createElement('div'); colL.className='col L'; colR.className='col R';
  const cards=[...sl.children]; const order={L:[0,1,2,4],R:[3,5,6]}; let side=false;
  window.fbHudSide=function(on){ if(on===side) return; side=on;
    if(on){ order.L.forEach(i=>colL.appendChild(cards[i])); order.R.forEach(i=>colR.appendChild(cards[i])); sl.appendChild(colL); sl.appendChild(colR);
      sl.style.cssText=''; sl.classList.add('side'); [...colL.children,...colR.children].forEach((c,i)=>c.style.animationDelay=(i*0.16)+'s'); sl.classList.remove('in'); void sl.offsetWidth; sl.classList.add('in');
      if(window.sfx) window.sfx('open'); if(window.fbHudRedraw) setTimeout(window.fbHudRedraw,60); }
    else { sl.classList.remove('side','in'); cards.forEach(c=>{ c.style.animationDelay=''; sl.appendChild(c); }); colL.remove(); colR.remove(); } };
})();
</script>
"""
R=[
 ("</style>", CSS+"</style>"),
 ("function rings(){ const cv=$('sl-rings'); if(!cv||!document.body.classList.contains('sleep')) return;", "function rings(){ const cv=$('sl-rings'); if(!cv) return;"),
 ("clock(); if(document.body.classList.contains('sleep')){ rings(); spark('sl-rxc',rx); spark('sl-txc',tx); } };",
  "clock(); rings(); spark('sl-rxc',rx); spark('sl-txc',tx); };\n  window.fbHudRedraw=()=>{ if(D){ rings(); spark('sl-rxc',rx); spark('sl-txc',tx); } };"),
 ("{ const sl=document.getElementById('sl'); if(sl){ const k=", "{ const sl=document.getElementById('sl'); if(window.fbHudSide) window.fbHudSide(!asleep&&sleepV===0&&b>=1); if(sl&&!sl.classList.contains('side')){ const k="),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fbHudSide' in s: print(f,'already patched'); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:70])
        s=s.replace(a,b,1)
    s=s.replace('</body>',JS+'</body>',1) if '</body>' in s else s.rstrip('\n')+'\n'+JS
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
