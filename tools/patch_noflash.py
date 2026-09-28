#!/usr/bin/env python3
# patch_noflash.py - removes the white "negative flash" of scary/intrusion mode (keeps the glitches). Idempotent.
import sys
A="float inv=uMood*step(0.975,hash(gt+3.0)); col=mix(col,vec3(1.0)-col*1.5,inv*0.9);   // negative flash"
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if A not in s: print(f,'already patched'); continue
    open(f,'w',encoding='utf-8').write(s.replace(A,"/* negative flash removed */")); print(f,'patched')
