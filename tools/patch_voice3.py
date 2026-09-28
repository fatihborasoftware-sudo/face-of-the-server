#!/usr/bin/env python3
# patch_voice3.py - Khoa "clear and deep": pitch lowered ~10 % (speed kept), bass shelf, presence boost, compressor.
import sys
A="fetch(window.fbTTS+'say?text='+encodeURIComponent(text)+'&v='+encodeURIComponent(srv),{signal:ctrl.signal})"
B="fetch(window.fbTTS+'say?text='+encodeURIComponent(text)+'&v='+encodeURIComponent(srv)+'&len='+(window.FB_VOICE_LEN||1.0),{signal:ctrl.signal})"
A2="const a=new Audio(URL.createObjectURL(b)); window.fbAudio=a; a.volume=1;"
B2="const a=new Audio(URL.createObjectURL(b)); window.fbAudio=a; a.volume=1; a.playbackRate=window.FB_VOICE_DEEP||0.88; try{ a.preservesPitch=false; a.mozPreservesPitch=false; }catch(e){}"
A3="const s=c.createMediaElementSource(a), an=c.createAnalyser(); an.fftSize=256; s.connect(an); an.connect(c.destination);"
B3="const s=c.createMediaElementSource(a), an=c.createAnalyser(); an.fftSize=256; const lo=c.createBiquadFilter(); lo.type='lowshelf'; lo.frequency.value=180; lo.gain.value=5; const pr=c.createBiquadFilter(); pr.type='peaking'; pr.frequency.value=2600; pr.Q.value=0.9; pr.gain.value=3; const cp=c.createDynamicsCompressor(); cp.threshold.value=-22; cp.knee.value=12; cp.ratio.value=3; cp.attack.value=0.005; cp.release.value=0.2; const g=c.createGain(); g.gain.value=1.25; s.connect(lo); lo.connect(pr); pr.connect(cp); cp.connect(g); g.connect(an); an.connect(c.destination);"
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'FB_VOICE_DEEP' in s: print(f,'already patched'); continue
    for a,b in [(A,B),(A2,B2),(A3,B3)]:
        if s.count(a)!=1: sys.exit(f+': anchor not found once ('+str(s.count(a))+'): '+a[:60])
        s=s.replace(a,b,1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
