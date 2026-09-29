(()=>{ const R=[[/GB LEFT of 98 GB/g,'GB KALDI / 98 GB'],[/GB of 28 GB/g,'GB / 28 GB'],[/GB of 7\.2 GB/g,'GB / 7.2 GB'],[/of 27 PACKAGES/g,'/ 27 PAKET'],[/REBOOT AFTER/g,'SONRA YENİDEN BAŞLAT'],[/of 12 RUNNING/g,'/ 12 ÇALIŞIYOR'],
 [/FAILED LOGINS/g,'BAŞARISIZ GİRİŞ'],[/FIREWALL HOLDING/g,'GÜVENLİK DUVARI DAYANIYOR'],[/\bTHROTTLING\b/g,'HIZ DÜŞÜRÜLÜYOR'],[/\bCRITICAL\b/g,'KRİTİK'],[/\bFANS\b/g,'FANLAR'],[/\bCOOL\b/g,'SERİN'],[/\bWARM\b/g,'ILIK'],[/\bHOT\b/g,'SICAK'],[/\bSWAP\b/g,'TAKAS'],[/\bCORES\b/g,'ÇEKİRDEK'],[/^LOAD\b/g,'YÜK']];
 const tr=s=>{ if(typeof s!=='string') return s; R.forEach(([a,b])=>{ s=s.replace(a,b); }); return s; };
 const P=CanvasRenderingContext2D.prototype; const f=P.fillText, st=P.strokeText, m=P.measureText;
 P.fillText=function(t,...a){ return f.call(this,tr(t),...a); }; P.strokeText=function(t,...a){ return st.call(this,tr(t),...a); }; P.measureText=function(t){ return m.call(this,tr(t)); }; })();
