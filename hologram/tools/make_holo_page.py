#!/usr/bin/env python3
"""make_holo_page.py - builds khoa-holo.html (the page the hologram videos are rendered from)
from the web version khoa-web.html (see wordpress/fb-khoa/app/). It only translates the
small line under each situation gauge to Turkish; everything else is the same page.

    python3 make_holo_page.py khoa-web.html khoa-holo.html
"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
R = [("' GB of 28 GB'", "' GB / 28 GB'"),
     ("' FAILED LOGINS  \\u00b7  FIREWALL HOLDING'", "' BAŞARISIZ GİRİŞ  \\u00b7  GÜVENLİK DUVARI DAYANIYOR'"),
     ("v<60?'COOL':v<75?'WARM  \\u00b7  FANS 60 %':v<85?'HOT  \\u00b7  FANS 100 %':'CRITICAL  \\u00b7  THROTTLING'",
      "v<60?'SERİN':v<75?'ILIK  \\u00b7  FANLAR 60 %':v<85?'SICAK  \\u00b7  FANLAR 100 %':'KRİTİK  \\u00b7  HIZ DÜŞÜRÜLÜYOR'"),
     ("' GB of 7.2 GB  \\u00b7  SWAP '", "' GB / 7.2 GB  \\u00b7  TAKAS '"),
     ("' GB LEFT of 98 GB'", "' GB KALDI / 98 GB'"),
     ("'LOAD '+(v/25).toFixed(2)+'  \\u00b7  4 CORES'", "'YÜK '+(v/25).toFixed(2)+'  \\u00b7  4 ÇEKİRDEK'"),
     ("' of 27 PACKAGES  \\u00b7  REBOOT AFTER'", "' / 27 PAKET  \\u00b7  SONRA YENİDEN BAŞLAT'"),
     ("' of 12 RUNNING  \\u00b7  nginx", "' / 12 ÇALIŞIYOR  \\u00b7  nginx")]
for a, b in R:
    n = s.count(a)
    if n != 1:
        raise SystemExit('anchor found %d times: %r' % (n, a[:60]))
    s = s.replace(a, b)
open(dst, 'w', encoding='utf-8').write(s)
print('ok ->', dst)
