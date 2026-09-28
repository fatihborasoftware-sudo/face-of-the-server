#!/usr/bin/env python3
# patch_field.py - sleep as a field of glitter over the whole screen, with a margin so it never reaches the edges
# (replaces the wandering bubble of patch_bubble.py). Idempotent.
import sys, re
NEW=("if(es>0.0){ vec3 g=vec3((fract(sin(aSeed*127.1+311.7)*43758.5453)-0.5)*5.8,(fract(sin(aSeed*269.5+183.3)*43758.5453)-0.5)*2.7,(fract(sin(aSeed*419.2+371.9)*43758.5453)-0.5)*1.0);\n"
     "          g.x=mod(g.x+uTime*0.12*(fract(sin(aSeed*77.7+13.1)*43758.5453)-0.5)+2.9,5.8)-2.9; g+=vec3(sin(uTime*0.17+aSeed*40.0)*0.5,cos(uTime*0.13+aSeed*27.0)*0.35,sin(uTime*0.11+aSeed*19.0)*0.3);\n"
     "          fly=mix(fly,g,es); }")
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if '-0.5)*5.8' in s: print(f,'already patched'); continue
    s2=re.sub(r"if\(es>0\.0\)\{ vec3 rnd=.*?fly=mix\(fly,g,es\); \}", NEW, s, count=1, flags=re.S)
    if s2==s: sys.exit(f+': bubble block not found')
    s=s2.replace("a=mix(a,(0.2+0.32*tw)*(0.5+0.5*fract(aSeed*4.7)),es);","a=mix(a,(0.25+0.5*tw)*(0.5+0.5*fract(aSeed*4.7)),es);")
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
