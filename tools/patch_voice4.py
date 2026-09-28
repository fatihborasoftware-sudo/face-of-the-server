#!/usr/bin/env python3
# patch_voice4.py - the Face reads the voice choice made on panels/voices.html (voice, depth, hall reverb).
import sys
A="a.playbackRate=window.FB_VOICE_DEEP||0.88;"
B="a.playbackRate=window.FB_VOICE_DEEP||parseFloat((()=>{try{return localStorage.getItem('fbVoiceDeep')}catch(e){return null}})())||0.88;"
A2="g.connect(an); an.connect(c.destination);"
B2="g.connect(an); an.connect(c.destination); try{ if(localStorage.getItem('fbVoiceHall')==='1'){ const n=c.sampleRate*1.6, ib=c.createBuffer(2,n,c.sampleRate); for(let ch=0;ch<2;ch++){ const d=ib.getChannelData(ch); for(let i=0;i<n;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/n,3.5); } const cv=c.createConvolver(); cv.buffer=ib; const wet=c.createGain(); wet.gain.value=0.28; g.connect(cv); cv.connect(wet); wet.connect(c.destination); } }catch(e){}"
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fbVoiceHall' in s: print(f,'already patched'); continue
    for a,b in [(A,B),(A2,B2)]:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:60])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
