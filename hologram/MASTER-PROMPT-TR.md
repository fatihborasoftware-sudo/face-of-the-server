# Master prompt: kendi "Sunucunun Yüzü" panonu yap (Khoa)

İki çizgi arasındaki her şeyi ilk mesajın olarak Claude'a yapıştır. Önce **SENİN** yazan üç satırı doldur, sonra Claude'un sorularını tek tek cevapla.

---

## Ben kimim, ne istiyorum

Kodlama bilmiyorum; beni adım adım yönlendir. Benim yapmam gereken bir şey olduğunda tam olarak nereye tıklayacağımı ya da hangi pencereye yazacağımı söyle. Yer tutucu değil gerçek değerler ver ve her satıra tek komut yaz.

Ev sunucum için **3D bir "yüz"** istiyorum: tam ekran bir web panosu. Ekranın ortasında ışıktan parçacıklarla oluşmuş bir insan anatomisi (écorché) figürü yaşıyor. Sunucuyu izliyor, bana dönüp bakıyor, sesli konuşuyor ve bir şey olduğunda rengi ve havası değişiyor.

- **SENİN** sunucun: (örneğin "eski bir dizüstünde Ubuntu 24.04" ya da "sunucu yok, sadece demo veri")
- **SENİN** figürünün adı ve ilk cümlesi: (örneğin "Khoa" ve "Ben Khoa. Sunucunun yüzüyüm.")
- **SENİN** dillerin: (örneğin "Türkçe, ziyaretçi seçerse İngilizce")

## Nasıl çalışacağız (lütfen bu sırayla)

1. **Önce taslak.** Gerçek kodu yazmadan önce tıklanabilir bir taslak göster (masaüstü ve telefon). Benim "onaylandı" dememi bekle.
2. **Adım adım plan.** Adımları numarala. Bir adımı yap, kendin test et, sonucu göster, sonra devam et.
3. **Kendi işini test et.** Her adımdan sonra sayfayı görünmez bir tarayıcıda (headless) aç, konsolda hata var mı bak, masaüstü ve telefon boyutunda ekran görüntüsü al.
4. **Dosya olarak teslim et.** Her sürümü indirilebilir dosya olarak ver (birden fazla dosya varsa zip). Bir CHANGELOG tut.
5. **Canlıda bir şeyi değiştirmeden önce yedek al.** Her seferinde önce sunucunun/sitenin yedeğini ya da anlık görüntüsünü al.

## Sayfa: `index.html` ("Sunucunun Yüzü")

Tek dosyadan oluşan, kendi kendine yeten bir HTML sayfası yap. three.js r128 kullan ve onu sayfanın yanında `three.min.js` olarak sakla (çalışırken CDN yok). Yazı tipi IBM Plex Mono. Arka plan neredeyse siyah bir lacivert (`#000306`); ana vurgu rengi camgöbeği `#6fdcff`, ikincisi kehribar `#ffb347`.

### Figür

- Bir insan anatomisi modeli (écorché) **parçacıklara** dönüşüyor. Modelin yüzeyinden noktalar alan ve bunları sayfanın içine gömen küçük bir Python aracı yaz: `build_body.py`. Böylece sayfanın ayrı bir model dosyasına ihtiyacı olmaz.
  - Creative Commons lisanslı bir model kullan ve alt bilgide yazarını görünür tut. Benimki Sketchfab'dan, Diego Luján García'nın "Male Full Body Ecorche" modeli (CC BY 4.0). Modeli ben indirip sana veririm.
- Yumuşak bir **bloom** parıltısı olan özel shader noktaları ve yavaş, nefes alır gibi bir ışıltı.
- **Oluşma girişi:** parçacıklar bir buluttan uçarak gelir ve yaklaşık 7 saniyede bedeni kurar. Durum satırında `OLUŞUYOR... 0–100%` yazar. Yükselen bir sentezleyici "oluşma" sesi, bir kilitlenme vuruşuyla biter. Ses sadece Web Audio ile üretilir, ses dosyası yok.
- **Bakış:** baş ve gözler fareyi takip eder (`BAKIYOR · FARE`). Web kamerası da sonra yönetebilsin diye `window.serraLookAt(x,y)` fonksiyonunu dışa aç. İsteğe bağlı bir KAMERA düğmesi ekle: yüz algılama kullansın, olmazsa harekete geçsin, sadece https üzerinde çalışsın.
- **Boşta yaşam:** hafif sallanma. Birkaç dakika kimse yoksa "uyuya kalır" (çöker ve kararır), bir dokunuşta ya da tuşa basınca uyanır.
- **Sahne:** etrafında o hareket edince savrulan ince toz parçacıkları, uzakta soluk bir parçacık dağ silsilesi ve dönen halkalar.
- **Durumlar:** `beklemede · dinliyor · düşünüyor · konuşuyor`, küçük etiketler olarak görünür. Konuşurken kollar yavaşça jest yapar (sadece kollar bükülür, beden sabit kalır) ve elden parçacıklar akar.

### HUD ve pano (figürün çevresinde)

- **Üst çubuk:** isim ("KHOA · SUNUCUNUN YÜZÜ"), durum satırı, saat, tarih, çalışma süresi ve `AĞ ▼ ▲`.
- **Yan paneller, ince ve yarı saydam:**
  - SİSTEM YÜKÜ: işlemci, bellek, kök disk ve işlemci sıcaklığı halka göstergeler olarak, yanında "serin / ılık / sıcak".
  - DEPOLAMA: diskler ve boş alan.
  - SERVİSLER: "11 / 12 TAMAM".
  - AĞ: indirme/yükleme hızı, arayüz, adres.
  - ERİŞİM: "SADECE YEREL AĞ", oturumlar, başarısız girişler, son giriş.
  - SON OLAYLAR: son 5 satır.
- **Veri kaynağı:** sayfa her 5 saniyede sunucudan `data.json` okur. Okuyamazsa içindeki **demo veriyi** kullanır; böylece sayfa her zaman çalışır.
  - `data.json` dosyasını yazan küçük bir sunucu betiği yaz (Python, systemd ile çalışsın): işlemci, bellek, diskler, sıcaklık, servisler, ağ, girişler, son yedek, olaylar.
- **Alttaki düğmeler:** `↻ TEKRAR` (giriş yeniden), `☠ KORKUNÇ` (dramatik kırmızı mod), `■ SESSİZ` (sesi kapat).

### Durumlar (işin kalbi)

Dokuz durum var. Klavyedeki **0–8** tuşları ve sunucudan gelen bir komut aralarında geçiş yapar. Her durum bütün bedeni boyar, bir efekt ekler, canlı göstergeli büyük bir başlık gösterir, kısa bir ses çalar ve ona bir cümle söyletir.

| Tuş | Durum | Renk | Gösterge |
|---|---|---|---|
| 0 | NORMAL | camgöbeği `#6fdcff` | yok |
| 1 | YEDEKLEME SÜRÜYOR | yeşil `#39ff6a` | yedek % ve "28 GB'ın x GB'ı" |
| 2 | SALDIRI TESPİT EDİLDİ | kırmızı `#ff2a1a`, yanıp söner | başarısız girişler ve saldırganın adresi |
| 3 | AŞIRI ISINMA | turuncu `#ff7a1a` | işlemci °C: serin / ılık / sıcak / kısıtlama |
| 4 | BELLEK BASKISI | mor `#b86bff` | bellek % ve takas |
| 5 | DİSK DOLMAK ÜZERE | kehribar `#ffb347` | SSD %, kalan GB |
| 6 | YÜKSEK YÜK | beyaz `#e8f4ff` | yük ortalaması, çekirdek sayısı |
| 7 | GÜNCELLENİYOR | mavi `#4aa8ff` | 27 paketten x'i |
| 8 | SERVİS ÇÖKTÜ | kırmızı `#ff4a3a`, yanıp söner | 12 servisten çalışan x |

Başlık metni gerçek değere uymalı. Örneğin 45 °C'de "AŞIRI ISINMA" yazmasın.

### Sesi

- Sesi **Piper** ile kaydet (internetsiz metinden sese):
  - İngilizce: `en_GB-alan-medium`
  - Türkçe: `tr_TR-dfki-medium`. Daha yavaş ve biraz daha kalın olsun, hafif metalik bir yankısı olsun. Önce seçmem için 5–6 kısa örnek ver.
- **Sunucuda:** kuyruklu küçük bir ses servisi (Python, systemd, port 8082). Kuyruğa satır ekleyen bir terminal komutu ekle: `khoa say "metin" --sit heat --value 63`. Sayfa kuyruğu her 1,5 saniyede kontrol eder ve her yeni satırı okur.
- **Herkese açık bir web sitesinde (sunucu yok):** her cümleyi önceden küçük mp3 dosyaları olarak kaydet ve onları çal.
- **CANLI mod:** o konuşurken kamera biraz yaklaşır, pano yaklaşık yüzde 18'e kadar kararır, solda büyük bir başlık çıkar ve altında altyazılar kelime kelime belirir. Son kelimeden yaklaşık 2,5 saniye sonra her şey eski haline döner.

### Performans

- Bir **hafif mod** ekle (`?lite`; telefonlarda, dokunmatik ve dar ekranlarda otomatik): daha düşük piksel oranı, bloom yok, parçacıkların yaklaşık yüzde 25'i, dağlar ve toz yok.
- Sekme gizliyken ya da ekrandan kaydırılmışken bütün animasyonu duraklat.
- Eski bir dizüstünde (i5, 8 GB) akıcı çalışmalı.

## İkinci sayfa: `map.html` ("Komuta Haritası")

Aynı figür, daha küçük, ortada. Çevresinde parlayan tellerle bağlı **düğümler** var:

- **Ekip (camgöbeği):** yapay zeka ajanlarım. Her birinin adı, görevi, kodu, komutu, "ne iş yapar" (3 satır), "örnek istekler" (2 satır) ve bir kimlik kartı resmi var. **SENİN** ekibin: (listele ya da Claude'dan 8 tane uydurmasını iste)
- **Uygulamalar (kehribar):** sunucumdaki araçlar; örneğin Cockpit, bir dosya sürücüsü, bir hosting paneli, bir test laboratuvarı ve bir rehber sitesi.
- Bir düğüme tıklayınca kimlik kartı açılır pencerede açılır.
- Bir ajan "konuşunca" figür ona döner, kolunu kaldırır, düğüm yanar ve kart açılır.
- "Sunucunun Yüzü" ile "Komuta Haritası" arasında geçmek için bir **PANELLER** anahtarı ekle.

## İsteğe bağlı: herkese açık bir web sitesine koy

İki sayfayı iki Elementor bileşeni olan bir **WordPress eklentisine** sar:

- **Hero:** sadece figür, tam ekran, girişi oynatan bir "Tanış" düğmesiyle.
- **Sahne:** pano, 9 durum düğmesi ve ekip düğmeleriyle.

Ayrıntılar:
- Sadece demo veri kullan; herkese açık sitede özel adres olmasın.
- Sahne ancak ziyaretçi tıklayınca yüklensin.
- Dil geçişi Polylang ile olsun (varsayılan dil `/` adresinde, diğer dil `/tr/` adresinde).
- Ana sayfa, sayfalarla `postMessage` üzerinden konuşsun (`intro`, `sit`, `talk`, `pause`).
- Her eklenti sürümünü kendim yüklerim. Her yüklemeden önce yedek al.

## Bitiş

Her şey çalışınca bir **GitHub yükleme klasörü** hazırla: sayfalar, araçlar, ekran görüntülü ve "kendine uyarla" bölümlü bir README, bir CHANGELOG ve MIT lisansı. Sonra yüklenenin klasörümle dosya dosya aynı olduğunu kontrol et.

---

### Bu promptu kullanma ipuçları

- **Parça parça ilerle.** Orijinali birkaç uzun oturum sürdü. Önce figürü, sonra panoyu, durumları, sesi, Komuta Haritası'nı ve en son web sitesini iste.
- **Taslak adımını atlama.** Saatlerce yeniden yapmaktan kurtarır.
- **Bir şey yanlış görünüyorsa hemen söyle.** Örneğin "kartların beyaz kenarları var". Claude düzeltir, test eder ve sonra devam eder.
