# Turkish texts for the Command Map nodes (id -> fields that replace the English ones)
MAP_TR = {
 'serra':  {'sub':'F2 · BAŞ YZ OPERATÖRÜ · fbspeak', 'handles':['Her brifingi ve her adımı sesli okur','Tüm ekibin sesi — tek ses, sekiz üye','Sabah brifingi, gece kapanışı, sesli uyarılar'], 'ex':['fbjobs say "günaydın"','önce panoyu oku'], 'ft':'ÇEVRİMİÇİ — HER BRİFİNG ONUN ÜZERİNDEN GEÇER'},
 'watch':  {'sub':'F1 · SİSTEM MUHAFIZI · fbwatch', 'handles':['Servisleri, diskleri ve sıcaklığı izler','Bir şey bozulmadan alarm verir','Her uyanışta sağlık kontrolü'], 'ex':['fbwatch','sunucu sağlıklı mı?'], 'ft':'ÇEVRİMİÇİ — GÖZETİM'},
 'locke':  {'sub':'F3 · DEPOLAMA SORUMLUSU · fbdisks', 'handles':['Her disk, her bağlama noktası, her boş gigabayt','FB-Server sürücüsü ve yedek disk','Asla silmez — kenara taşır'], 'ex':['fbdisks','ne kadar yer kaldı?'], 'ft':'ÇEVRİMİÇİ — KASA'},
 'corren': {'sub':'F4 · YEDEKLEME UZMANI · fbbackup', 'handles':['Yedek diske anlık ve günlük yedekler','Laboratuvar konteynerinde geri yükleme testleri','Tüm ekibin güvendiği geri yükleme bilgisi'], 'ex':['fbbackup spot','geri yükleme testi seviye 1'], 'ft':'ÇEVRİMİÇİ — KURTARMA'},
 'quill':  {'sub':'F5 · İSTİHBARAT ANALİSTİ · fbtodo', 'handles':['Pano: açık kartlar, biten kartlar, brifingler','Neyin kime söz verildiği','Her emirden önce kartları okur'], 'ex':['fbtodo list','en önemli görev hangisi?'], 'ft':'ÇEVRİMİÇİ — ARŞİV'},
 'dusk':   {'sub':'F6 · GÜÇ YÖNETİCİSİ · fbsleep', 'handles':['Sessiz saatler ve iyi geceler','Uyku, uyanış ve sabah servisi','Işıklar sönünce kimse konuşmaz'], 'ex':['fbsleep','iyi geceler Serra'], 'ft':'ÇEVRİMİÇİ — GECE'},
 'relay':  {'sub':'F8 · OTOMASYON KOORDİNATÖRÜ · fbjobs', 'handles':['Zamanlanmış işler, ritüeller ve fbday','İşi doğru üyeye dağıtır','Zamanlayıcılar, yeniden denemeler, sabah rutini'], 'ex':['fbjobs list','sabah ritüelini çalıştır'], 'ft':'ÇEVRİMİÇİ — SEVK'},
 'mason':  {'sub':'F7 · SİTE MÜHENDİSİ · fbsite', 'handles':['Sunucudaki web sitelerini kurar ve yayınlar','Ekipte bir şey yaratan tek üye','Kaldırılan siteyi kenara taşır, asla silmez'], 'ex':['fbsite new','siteleri listele'], 'ft':'ÇEVRİMİÇİ — İNŞA'},
 'cockpit':{'sub':'SİSTEM KONSOLU · PORT 9090', 'handles':['Terminal, servisler, kayıtlar, güncellemeler','Claude’un komutları yazdığı yer','Sunucunun giriş ekranı'], 'ex':['terminali aç','servisleri göster'], 'ft':'ÇEVRİMİÇİ — SİSTEM'},
 'panel':  {'sub':'HOSTİNG PANELİ · PROTOTİP', 'handles':['Serinin cPanel benzeri paneli','Müşteri ve yönetici tarafı','YouTube’da birlikte inşa ediliyor'], 'ex':['FB Panel’i aç','müşteri görünümünü göster'], 'ft':'PROTOTİP — SERİDE'},
 'drive':  {'sub':'DOSYALAR · /srv/disk/FB-Server', 'handles':['Sunucunun ortak sürücüsü','Yedek klasörü, medya, rehber','Tarayıcıdan çevrimiçi'], 'ex':['sürücüyü aç','yedekler nerede?'], 'ft':'ÇEVRİMİÇİ — DEPOLAMA'},
 'console':{'sub':'EKİP KONSOLU · 0.2', 'handles':['Ekibin kendi konsol uygulaması','Kartlar, brifingler ve her üyenin durumu','Kendi servis kullanıcısıyla çalışır'], 'ex':['fbconsole','kim nöbette?'], 'ft':'ÇEVRİMİÇİ — EKİP'},
 'lab':    {'sub':'TEST LABORATUVARI · INCUS KONTEYNERLERİ', 'handles':['Sunucunun atılabilir bir kopyası','Geri yükleme testlerinin güvenle çalıştığı yer','Kendi ağı, fblab0'], 'ex':['fblab start','geri yüklemeyi laboratuvarda çalıştır'], 'ft':'ÇEVRİMİÇİ — LABORATUVAR'},
 'guide':  {'sub':'BELGELER · fbserver.net', 'handles':['Kurulum ve erişim rehberi','YouTube birlikte-inşa serisi','Projenin herkese açık sitesi'], 'ex':['rehberi aç','videoları göster'], 'ft':'ÇEVRİMİÇİ — HERKESE AÇIK'},
}
UI_TR = {
 'COMMAND MAP · THE FACE OF THE SERVER':'KOMUTA HARİTASI · SUNUCUNUN YÜZÜ',
 'CLICK A NODE · THE CREW AND THE APPS OF FBSERVER':'BİR DÜĞÜME TIKLA · FBSERVER’IN EKİBİ VE UYGULAMALARI',
 'WHAT IT HANDLES':'NE İŞ YAPAR','EXAMPLE REQUESTS':'ÖRNEK İSTEKLER','SPEAKING':'KONUŞUYOR',
}
