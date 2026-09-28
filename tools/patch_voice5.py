#!/usr/bin/env python3
# patch_voice5.py - Khoa's chosen voice: Alan (British, precise), natural pitch. Sets the defaults.
import sys
R=[("localStorage.getItem('fbSrvVoice')||'ryan'; }catch(e){ return 'ryan'; }","localStorage.getItem('fbSrvVoice')||'alan'; }catch(e){ return 'alan'; }"),
   ("catch(e){return null}})())||0.88;","catch(e){return null}})())||1.0;"),
   ("lo.frequency.value=180; lo.gain.value=5;","lo.frequency.value=180; lo.gain.value=3;"),
   ("const SV=['ryan','joe','alan','northern_english_male','norman','lessac','browser'];","const SV=['alan','ryan','joe','northern_english_male','norman','lessac','browser'];")]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read(); n=0
    for a,b in R:
        if s.count(a)==1: s=s.replace(a,b); n+=1
    open(f,'w',encoding='utf-8').write(s); print(f,'changed',n)
