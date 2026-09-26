#!/usr/bin/env python3
# patch_cam.py — adds the webcam look-at script to face.html / map.html (idempotent). Usage: python3 patch_cam.py webcam.js FILE...
import sys
w=open(sys.argv[1],encoding='utf-8').read()
for f in sys.argv[2:]:
    s=open(f,encoding='utf-8').read()
    if 'window.fbCamera' in s: print(f,'already patched'); continue
    if '</body>' not in s: sys.exit(f+': no </body>')
    s=s.replace('</body>','<script>\n'+w+'</script>\n</body>',1)
    open(f,'w',encoding='utf-8').write(s); print(f,'patched')
