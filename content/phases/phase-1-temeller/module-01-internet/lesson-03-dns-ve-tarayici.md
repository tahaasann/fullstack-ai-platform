---
id: "internet-03-dns-ve-tarayici"
title: "DNS ve Tarayıcı Render Pipeline"
description: "Domain Name System'in derinlemesine çalışma mekanizması, DNS record türleri, tarayıcının HTML'den piksele render süreci, Critical Render Path optimizasyonu ve CDN/caching stratejileri"
estimated_minutes: 60
order: 3
tags: ["dns", "browser", "rendering", "critical-render-path", "cdn", "caching", "dom", "cssom"]
---

# DNS ve Tarayıcı Render Pipeline

:::realworld
Kullanıcın adres çubuğuna "example.com" yazıp Enter'a bastığı andan ekranda piksellerin belirdiği ana kadar arka planda onlarca karmaşık süreç işler. Bu derste o süreci iki büyük parçaya ayırıyoruz: birincisi, domain adının IP adresine dönüştürülmesi (DNS); ikincisi, sunucudan gelen HTML/CSS/JS'in ekrandaki piksellere dönüşmesi (Render Pipeline). Bu iki konuyu deha seviyesinde anlamak, performans optimizasyonu yapabilmeni ve mülakatlarda fark yaratmanı sağlar.
:::

## Neden Bu Konuyu Öğreniyorsun?

DNS ve tarayıcı rendering, bir web developer'ın günlük hayatını doğrudan etkileyen iki temel konudur. Bunları bilmeden:

- Neden sitenin ilk açılışı yavaş olduğunu anlayamazsın
- Performans metriklerini (LCP, FCP, CLS) iyileştiremezsin
- CDN ve cache stratejileri kuramazsın
- "Tarayıcıya URL yazdığında ne olur?" mülakat sorusuna tatmin edici cevap veremezsin

:::deha-tip
Deha seviyesi geliştiriciler, DNS çözümleme süresini DevTools'tan takip eder, prefetch/preconnect stratejileri ile DNS lookup süresini sıfıra indirir ve Critical Render Path'i optimize ederek First Contentful Paint süresini 1 saniyenin altına çeker. Onlar için "sayfa yavaş" değil, "DNS lookup 120ms, TTFB 340ms, render-blocking CSS 200ms" gibi spesifik sorunlar vardır.
:::

---

## Bölüm 1: DNS (Domain Name System)

### DNS Nedir?

:::concept[DNS (Domain Name System)]
DNS, insan tarafından okunabilir domain adlarını (google.com) makinelerin anlayabildiği IP adreslerine (142.250.185.14) çeviren dağıtık bir veritabanı sistemidir.

**Türkçe karşılığı:** Alan Adı Sistemi
**Ne işe yarar:** İnsanların IP adreslerini ezberlemek yerine anlamlı isimler kullanmasını sağlar
**Gerçek hayat benzetmesi:** Telefon rehberi gibi düşün. "Ahmet" ismini arıyorsun, rehber sana 0532-XXX-XX-XX numarasını veriyor. DNS de "google.com" ismini alıp sana 142.250.185.14 IP adresini veriyor.
:::

### DNS Çözümleme Süreci (DNS Resolution)

Tarayıcıya bir URL yazdığında, IP adresini bulmak için şu adımlar sırasıyla izlenir:

:::code[text]{title="DNS Çözümleme Adımları (Detaylı)"}
Kullanıcı: "www.example.com" yazıyor

1. Browser Cache Kontrolü
   → Tarayıcı daha önce bu domain'i çözdü mü? (genelde 60 saniye cache'lenir)

2. OS Cache Kontrolü
   → İşletim sistemi DNS cache'inde var mı?
   → /etc/hosts dosyası kontrol edilir (Linux/Mac) veya C:\Windows\System32\drivers\etc\hosts (Windows)

3. Router Cache Kontrolü
   → Ev/ofis router'ının DNS cache'i kontrol edilir

4. ISP'nin Recursive Resolver'ı
   → ISP'nin (İnternet Servis Sağlayıcısı) DNS sunucusuna sorulur
   → Burada da bulunamazsa, resolver iteratif sorguya başlar:

   4a. Root DNS Server (13 adet, dünya genelinde dağıtık)
       → "com'un TLD sunucusu şurada" der

   4b. TLD (Top-Level Domain) Server
       → ".com" sunucusu → "example.com'un authoritative sunucusu şurada" der

   4c. Authoritative DNS Server
       → example.com'un kendi DNS sunucusu → "IP adresi 93.184.216.34" der

5. IP adresi tüm cache katmanlarına yazılır ve tarayıcıya döner
:::

:::tip
DNS çözümleme genelde 20-120ms sürer. Ama cache'te varsa 0ms'ye yakın olur. Bu yüzden DNS caching performans için kritiktir.
:::

:::code[text]{title="DNS Sorgu Akışı (Görsel)"}
Tarayıcı                Recursive Resolver         Root Server
   |                         |                         |
   |-- "www.example.com?" -->|                         |
   |                         |-- "com nerede?" -------->|
   |                         |<-- "com TLD: 192.5.6.30"|
   |                         |
   |                         |     TLD Server (.com)
   |                         |-- "example.com?" ------->|
   |                         |<-- "NS: ns1.example.com" |
   |                         |
   |                         |   Authoritative Server
   |                         |-- "www.example.com?" --->|
   |                         |<-- "A: 93.184.216.34"    |
   |                         |
   |<-- "93.184.216.34" -----|
:::

:::beginner-mistake
Yaygın hata: "DNS her seferinde Root Server'a kadar gider" demek. Gerçekte, DNS aggressive caching kullanır. Recursive resolver çoğu popüler domain için cevabı cache'inde tutar. Root server'a nadiren gidilir. Google'ın DNS sunucuları (8.8.8.8) günde trilyonlarca sorguyu cache'ten yanıtlar.
:::

### DNS Record Türleri

DNS sadece IP adresi döndürmez. Farklı türde kayıtlar (record) tutar:

:::comparison
| Record Türü | Açıklama | Örnek Değer | Kullanım Alanı |
|-------------|----------|-------------|----------------|
| **A** | Domain → IPv4 adresi | 93.184.216.34 | Web sitesi IP adresi |
| **AAAA** | Domain → IPv6 adresi | 2606:2800:220:1:248:1893:25c8:1946 | IPv6 desteği |
| **CNAME** | Domain → Başka domain (alias) | www.example.com → example.com | Subdomain yönlendirme |
| **MX** | Mail sunucusu adresi | mail.example.com (priority: 10) | Email routing |
| **TXT** | Metin tabanlı kayıt | "v=spf1 include:_spf.google.com" | SPF, DKIM, domain doğrulama |
| **NS** | Authoritative DNS sunucusu | ns1.example.com | DNS delegasyonu |
| **SOA** | Zone bilgisi ve yönetim verisi | serial, refresh, retry, expire | DNS zone yönetimi |
| **PTR** | IP → Domain (reverse DNS) | 34.216.184.93.in-addr.arpa → example.com | Email spam kontrolü, loglama |

**Tavsiye:** Frontend developer olarak en çok A, CNAME ve TXT kayıtlarıyla karşılaşırsın. DevOps/Backend için MX ve NS da kritiktir.
:::

:::code[bash]{title="DNS Kayıtlarını Sorgulama (Pratik)"}
# A kaydını sorgula
nslookup example.com
dig example.com A

# MX kaydını sorgula (mail sunucuları)
dig example.com MX

# Tüm DNS kayıtlarını gör
dig example.com ANY

# Belirli bir DNS sunucusundan sorgula
dig @8.8.8.8 example.com

# CNAME zincirini takip et
dig www.github.com CNAME

# TTL değerini gör
dig example.com A +ttl
:::

### DNS Cache ve TTL

:::concept[TTL (Time To Live)]
TTL, bir DNS kaydının cache'te ne kadar süre tutulacağını saniye cinsinden belirten değerdir.

**Türkçe karşılığı:** Yaşam Süresi
**Ne işe yarar:** DNS sorgularının gereksiz yere tekrarlanmasını önler, aynı zamanda değişikliklerin yayılma süresini kontrol eder
**Gerçek hayat benzetmesi:** Bir haberin "son kullanma tarihi" gibi. TTL dolana kadar eski bilgi geçerli kabul edilir, dolduktan sonra yeni bilgi sorgulanır.
:::

:::code[text]{title="Tipik TTL Değerleri"}
300   (5 dk)    → Sık değişen kayıtlar, A/B test, geçiş dönemleri
3600  (1 saat)  → Normal web siteleri
86400 (1 gün)   → Nadiren değişen kayıtlar (MX, NS)
604800 (1 hafta) → Çok stabil altyapılar
:::

:::warning
DNS değişikliği yaptığında (örneğin hosting değiştirirken), eski TTL süresi dolana kadar bazı kullanıcılar eski IP'ye yönlendirilir. Bu yüzden hosting değişikliğinden önce TTL değerini düşürün (300 saniye gibi), değişikliği yapın, sonra TTL'i tekrar yükseltin. Bu sürece "DNS propagation" denir ve 24-48 saat sürebilir.
:::

---

## Bölüm 2: Tarayıcı Render Pipeline

Tarayıcı sunucudan HTML dosyasını aldıktan sonra onu ekrandaki piksellere dönüştürmek için 6 aşamalı bir pipeline işletir.

### Aşama 1: HTML Parsing ve DOM Tree Oluşturma

:::concept[DOM (Document Object Model)]
DOM, HTML belgesinin tarayıcı tarafından oluşturulan ağaç yapısındaki nesne temsilidir. Her HTML elementi bir DOM node'u olur.

**Türkçe karşılığı:** Belge Nesne Modeli
**Ne işe yarar:** JavaScript'in HTML elementlerini okuyup değiştirmesini sağlar
**Gerçek hayat benzetmesi:** HTML bir evin planı (blueprint), DOM ise o plandan inşa edilmiş gerçek ev. Evi değiştirmek istiyorsan DOM'u manipüle edersin.
:::

:::code[html]{title="HTML'den DOM Tree'ye Dönüşüm"}
<!-- HTML Kaynak Kodu -->
<html>
  <head>
    <title>Merhaba</title>
  </head>
  <body>
    <h1>Başlık</h1>
    <p>Paragraf</p>
  </body>
</html>

<!-- DOM Tree Yapısı -->
Document
 └── html
      ├── head
      │    └── title
      │         └── "Merhaba"
      └── body
           ├── h1
           │    └── "Başlık"
           └── p
                └── "Paragraf"
:::

:::warning
HTML parser bir `<script>` etiketine rastladığında DOM oluşturmayı durdurur ve script'i çalıştırır. Bu yüzden `<script>` etiketlerini `<body>` sonuna koymak veya `defer`/`async` attribute'ları kullanmak kritiktir. Aksi halde kullanıcı boş bir sayfa görür.
:::

### Aşama 2: CSS Parsing ve CSSOM Oluşturma

:::concept[CSSOM (CSS Object Model)]
CSSOM, CSS kurallarının tarayıcı tarafından oluşturulan ağaç yapısındaki temsilidir. DOM'un CSS karşılığıdır.

**Türkçe karşılığı:** CSS Nesne Modeli
**Ne işe yarar:** Tarayıcının her elemente hangi stil kurallarının uygulanacağını hesaplamasını sağlar
**Gerçek hayat benzetmesi:** DOM evin iskeleti ise, CSSOM evin boya ve dekorasyon planıdır
:::

:::code[text]{title="CSSOM Oluşturma Süreci"}
CSS Kaynak:
body { font-size: 16px; }
h1 { color: red; font-weight: bold; }
p { color: blue; }

CSSOM Tree:
body (font-size: 16px)
 ├── h1 (color: red, font-weight: bold, font-size: 16px [inherited])
 └── p  (color: blue, font-size: 16px [inherited])

Not: CSS özellikleri cascade ve inheritance kurallarına göre hesaplanır.
:::

:::beginner-mistake
Yaygın hata: "CSS render'ı engellemez" demek. CSS kesinlikle render-blocking'dir! Tarayıcı, CSSOM tamamlanmadan Render Tree oluşturamaz. Bu yüzden critical CSS'i inline yapmak ve geri kalanını async yüklemek önemli bir optimizasyondur.
:::

### Aşama 3: Render Tree Oluşturma

:::code[text]{title="DOM + CSSOM = Render Tree"}
DOM Tree:              CSSOM:                Render Tree:
html                   body{font:16px}       (html gizli elementler
├── head               h1{color:red}          hariç DOM + stil)
│   └── title          p{color:blue}
│   └── style          span{display:none}    body (font-size:16px)
└── body                                      ├── h1 "Başlık"
    ├── h1 "Başlık"                           │    (color:red)
    ├── p "Paragraf"                          └── p "Paragraf"
    └── span "Gizli"                               (color:blue)

Not: <head>, <script>, display:none olan elementler
     Render Tree'ye dahil EDİLMEZ!
     visibility:hidden olan elementler dahil EDİLİR (yer kaplar ama görünmez).
:::

### Aşama 4: Layout (Reflow)

:::concept[Layout / Reflow]
Layout aşamasında tarayıcı, Render Tree'deki her elementin viewport (ekran) üzerindeki tam pozisyonunu ve boyutunu hesaplar.

**Türkçe karşılığı:** Yerleşim Hesaplama
**Ne işe yarar:** Her elementin piksel cinsinden x, y, width, height değerlerini belirler
**Gerçek hayat benzetmesi:** Bir odaya mobilya yerleştirmek gibi. Her mobilyanın boyutunu ve konumunu hesaplayıp yerleştiriyorsun.
:::

:::warning
Layout/Reflow pahalı bir işlemdir. DOM'a element eklemek, boyut değiştirmek veya `offsetWidth`, `clientHeight` gibi layout property'leri okumak reflow tetikler. Performans için reflow sayısını minimize etmelisin.
:::

:::code[javascript]{title="Reflow Tetikleyen ve Tetiklemeyen İşlemler"}
// REFLOW TETİKLER (pahalı):
element.offsetWidth;          // Layout property okuma
element.style.width = "100px"; // Boyut değiştirme
element.style.display = "block";
element.appendChild(newChild); // DOM'a ekleme
window.getComputedStyle(el);   // Hesaplanmış stil okuma

// REFLOW TETİKLEMEZ (ucuz):
element.style.color = "red";      // Sadece repaint
element.style.opacity = 0.5;      // Sadece composite
element.style.transform = "...";  // Sadece composite (GPU)
:::

### Aşama 5: Paint

Paint aşamasında tarayıcı, layout bilgilerini kullanarak gerçek pikselleri çizer. Renkler, kenar çizgileri, gölgeler, metinler ve resimler bu aşamada rasterize edilir.

:::tip
Paint işlemi katmanlar (layers) halinde yapılır. `will-change`, `transform`, `opacity` gibi özellikler kullanıldığında tarayıcı o elementi ayrı bir katmana çıkarır. Bu sayede o element değiştiğinde diğer katmanlar yeniden çizilmez.
:::

### Aşama 6: Compositing

:::concept[Compositing (Katman Birleştirme)]
Compositing, ayrı ayrı boyanmış katmanların doğru sırada birleştirilerek ekranda son görüntüyü oluşturma işlemidir.

**Türkçe karşılığı:** Katman Birleştirme
**Ne işe yarar:** GPU hızlandırmalı animasyonları mümkün kılar
**Gerçek hayat benzetmesi:** Animasyon filminde farklı katmanlar (arka plan, karakter, efektler) ayrı ayrı çizilir ve son aşamada üst üste birleştirilir
:::

:::code[text]{title="Render Pipeline Özet Akışı"}
HTML ──► DOM Tree ──────────────────┐
                                    ├──► Render Tree ──► Layout ──► Paint ──► Composite ──► Ekran
CSS ──► CSSOM ──────────────────────┘

Performans Maliyeti (yüksekten düşüğe):
Layout (Reflow) > Paint (Repaint) > Composite

En iyi animasyon: Sadece composite tetikleyen (transform, opacity)
En kötü animasyon: Layout tetikleyen (width, height, top, left)
:::

---

## Bölüm 3: Critical Render Path Optimizasyonu

:::concept[Critical Render Path (CRP)]
Critical Render Path, tarayıcının ilk pikseli ekrana çizmesi için tamamlaması gereken minimum adımlar dizisidir.

**Türkçe karşılığı:** Kritik Render Yolu
**Ne işe yarar:** İlk sayfa yükleme süresini (FCP - First Contentful Paint) minimize eder
**Gerçek hayat benzetmesi:** Bir restoranın mutfağında ilk yemeği en hızlı şekilde çıkarmak gibi. Tüm menüyü hazırlamayı beklemezsin, önce en kritik tabağı çıkarırsın.
:::

:::code[html]{title="CRP Optimizasyon Teknikleri"}
<head>
  <!-- 1. Critical CSS inline yap (above-the-fold stil) -->
  <style>
    body { margin: 0; font-family: system-ui; }
    .hero { height: 100vh; background: #1a1a2e; color: white; }
  </style>

  <!-- 2. Geri kalan CSS'i async yükle -->
  <link rel="preload" href="/styles.css" as="style"
        onload="this.onload=null;this.rel='stylesheet'">

  <!-- 3. DNS Prefetch ve Preconnect -->
  <link rel="dns-prefetch" href="//api.example.com">
  <link rel="preconnect" href="https://cdn.example.com" crossorigin>

  <!-- 4. Critical kaynakları preload et -->
  <link rel="preload" href="/hero-image.webp" as="image">
  <link rel="preload" href="/critical-font.woff2" as="font"
        type="font/woff2" crossorigin>

  <!-- 5. Script'leri defer ile yükle (DOM'u bloklamaz) -->
  <script src="/app.js" defer></script>
</head>
:::

:::comparison
| Teknik | Ne Yapar | Etki |
|--------|----------|------|
| **Critical CSS Inline** | İlk ekran için gereken CSS'i HTML'e gömer | FCP iyileşir |
| **defer** | Script'i arka planda indirir, DOM hazır olunca çalıştırır | DOM blocking'i önler |
| **async** | Script'i arka planda indirir, indirilince hemen çalıştırır | Bağımsız script'ler için |
| **preload** | Kaynağı öncelikli olarak indirir | LCP iyileşir |
| **preconnect** | DNS + TCP + TLS handshake'i önceden yapar | Harici API'ler hızlanır |
| **dns-prefetch** | Sadece DNS çözümlemesini önceden yapar | Üçüncü parti domainler |
| **lazy loading** | Görünmeyen resimleri sonra yükler | İlk yükleme hızlanır |

**Tavsiye:** Chrome DevTools > Lighthouse > Performance raporuyla CRP sorunlarını tespit edebilirsin.
:::

---

## Bölüm 4: "Tarayıcıya URL Yazdığında Ne Olur?" - Tam Cevap

:::interview
**Mülakat Sorusu (Klasik):** "Tarayıcının adres çubuğuna www.example.com yazıp Enter'a bastığında ne olur? Mümkün olduğunca detaylı anlat."

**Deha seviyesi cevap:**

**1. URL Parsing ve HSTS Kontrolü**
- Tarayıcı URL'i parse eder (scheme, host, path, query)
- HSTS (HTTP Strict Transport Security) listesini kontrol eder
- Listede varsa HTTP otomatik olarak HTTPS'e yönlendirilir

**2. DNS Resolution**
- Browser cache → OS cache → Router cache → ISP Recursive Resolver
- Cache miss ise: Root → TLD → Authoritative DNS Server
- IP adresi bulunur (ör: 93.184.216.34)

**3. TCP Bağlantısı**
- 3-Way Handshake: SYN → SYN-ACK → ACK
- Bir RTT (Round Trip Time) sürer

**4. TLS Handshake (HTTPS ise)**
- Client Hello → Server Hello → Sertifika doğrulama
- Symmetric key exchange (ör: ECDHE)
- TLS 1.3'te 1 RTT, TLS 1.2'de 2 RTT sürer

**5. HTTP Request**
- GET / HTTP/2 isteği gönderilir
- Headers: Host, User-Agent, Accept, Accept-Encoding, Cookie

**6. Server Processing**
- Load balancer isteği uygun sunucuya yönlendirir
- Web server (Nginx/Apache) static dosya veya reverse proxy
- Application server (Node.js/Python) isteği işler
- Gerekirse database sorgusu yapılır
- HTML response oluşturulur

**7. HTTP Response**
- Status: 200 OK
- Headers: Content-Type, Cache-Control, Set-Cookie
- Body: HTML dosyası (genellikle gzip/brotli ile sıkıştırılmış)

**8. HTML Parsing ve Render**
- Byte → Character → Token → Node → DOM Tree
- CSS indirilir → CSSOM oluşturulur
- DOM + CSSOM → Render Tree
- Layout → Paint → Composite
- Kullanıcı sayfayı görür (First Contentful Paint)

**9. Subresource Loading**
- CSS, JS, resimler, fontlar paralel olarak indirilir
- JavaScript çalışır, dinamik içerik yüklenir
- Service Worker varsa cache stratejisi uygulanır

**10. Sayfa Tamamen Yüklenir**
- window.onload eventi tetiklenir
- Lazy load edilecek kaynaklar yüklenir
- Analytics ve üçüncü parti script'ler çalışır
:::

---

## Bölüm 5: WebSocket vs HTTP vs Server-Sent Events

:::comparison
| Özellik | HTTP | WebSocket | Server-Sent Events (SSE) |
|---------|------|-----------|--------------------------|
| **Yön** | İstemci → Sunucu (request-response) | Çift yönlü (full-duplex) | Sunucu → İstemci (tek yön) |
| **Bağlantı** | Her istekte yeni (veya keep-alive) | Kalıcı bağlantı | Kalıcı bağlantı |
| **Protokol** | HTTP/1.1, HTTP/2, HTTP/3 | ws:// veya wss:// | HTTP üzerinden |
| **Veri formatı** | Text, JSON, binary | Text, binary | Text (UTF-8) |
| **Kullanım** | REST API, web sayfaları | Chat, oyunlar, canlı dashboard | Bildirimler, canlı feed |
| **Yeniden bağlanma** | Yok (stateless) | Manuel implementasyon | Otomatik (built-in) |
| **Firewall uyumu** | Mükemmel | Sorunlu olabilir | İyi (HTTP üzerinden) |
| **Overhead** | Her istekte header | İlk handshake sonrası minimal | Her mesajda minimal header |

**Tavsiye:** Çoğu gerçek zamanlı uygulama için SSE yeterlidir. WebSocket'a sadece çift yönlü iletişim gerektiğinde (chat, oyun) ihtiyaç duyarsın. REST API her zaman temel iletişim şeklin olacak.
:::

:::code[javascript]{title="WebSocket vs SSE - Kod Karşılaştırması"}
// === WebSocket (çift yönlü) ===
const ws = new WebSocket('wss://api.example.com/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({ type: 'subscribe', channel: 'prices' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Sunucudan:', data);
};

ws.send('Merhaba sunucu!'); // İstemciden sunucuya gönderim

// === Server-Sent Events (tek yön: sunucu → istemci) ===
const es = new EventSource('https://api.example.com/stream');

es.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Sunucudan:', data);
};

es.onerror = () => {
  // Otomatik yeniden bağlanma (built-in!)
  console.log('Bağlantı koptu, yeniden bağlanılıyor...');
};
:::

---

## Bölüm 6: CDN (Content Delivery Network)

:::concept[CDN (Content Delivery Network)]
CDN, dünya genelinde dağıtılmış sunucu ağı aracılığıyla içeriği kullanıcıya en yakın noktadan sunan bir sistemdir.

**Türkçe karşılığı:** İçerik Dağıtım Ağı
**Ne işe yarar:** Statik dosyaları (resim, CSS, JS, video) kullanıcıya fiziksel olarak en yakın sunucudan sunarak gecikmeyi azaltır
**Gerçek hayat benzetmesi:** Bir kitabı Amazon'un ana deposundan sipariş etmek yerine, mahalledeki kargo dağıtım noktasından almak gibi. Ürün aynı ama teslimat çok daha hızlı.
:::

:::code[text]{title="CDN Çalışma Prensibi"}
CDN olmadan:
Kullanıcı (İstanbul) ──── 200ms ────► Origin Server (ABD)

CDN ile:
Kullanıcı (İstanbul) ── 20ms ──► CDN Edge (İstanbul)
                                      │
                                 Cache miss ise
                                      │
                                      ▼
                              Origin Server (ABD)
                              (sonraki istekler cache'ten)

Popüler CDN sağlayıcıları:
- Cloudflare (ücretsiz planı var, en yaygın)
- AWS CloudFront
- Google Cloud CDN
- Fastly
- Akamai (kurumsal)
:::

:::tip
Cloudflare'in ücretsiz planı, kişisel projeler ve küçük siteler için fazlasıyla yeterli. DDoS koruması, SSL sertifikası ve CDN hizmeti ücretsiz sunulur. İlk projelerinde Cloudflare kullanarak hem performansı hem güvenliği artırabilirsin.
:::

---

## Bölüm 7: Caching Stratejileri

:::concept[Cache (Önbellek)]
Cache, sık erişilen verilerin daha hızlı erişilebilir bir konumda geçici olarak saklanmasıdır.

**Türkçe karşılığı:** Önbellek
**Ne işe yarar:** Aynı veriyi tekrar tekrar indirmeyi önleyerek hız ve bant genişliği tasarrufu sağlar
**Gerçek hayat benzetmesi:** Sık kullandığın kitabı her seferinde kütüphaneye gidip almak yerine, masanın üzerinde tutmak
:::

:::comparison
| Cache Katmanı | Konum | TTL | Kontrol | Kullanım |
|---------------|-------|-----|---------|----------|
| **Browser Cache** | Kullanıcının tarayıcısı | Cache-Control header | Developer (HTTP headers) | CSS, JS, resimler |
| **CDN Cache** | Edge sunucular | s-maxage header | Developer + CDN config | Statik varlıklar |
| **Application Cache** | Sunucu belleği (Redis vb.) | Uygulama kodu | Developer | API yanıtları, DB sorguları |
| **DNS Cache** | Tarayıcı + OS + Router + ISP | DNS TTL | Domain yöneticisi | Domain → IP eşleşmeleri |
| **Service Worker Cache** | Kullanıcının cihazı | Uygulama kodu | Developer | Offline destek, PWA |
:::

:::code[text]{title="Cache-Control Header Değerleri"}
# Tarayıcıda 1 yıl cache'le (statik dosyalar için)
Cache-Control: public, max-age=31536000, immutable

# CDN'de 1 saat, tarayıcıda 5 dakika cache'le
Cache-Control: public, max-age=300, s-maxage=3600

# Hiç cache'leme (dinamik API yanıtları)
Cache-Control: no-store

# Her seferinde sunucuya doğrula (ETag ile)
Cache-Control: no-cache

# Sadece kullanıcının tarayıcısında cache'le (özel veri)
Cache-Control: private, max-age=3600
:::

:::deha-tip
Modern frontend projelerinde statik dosyalar (JS, CSS) genellikle content hash ile isimlendirilir (ör: `app.a1b2c3.js`). Dosya içeriği değiştiğinde hash değişir, yeni URL oluşur. Bu sayede `max-age=31536000` (1 yıl) kullanılabilir ve cache invalidation sorunu ortadan kalkar. Webpack, Vite gibi build tool'ları bunu otomatik yapar.
:::

:::beginner-mistake
Yaygın hata: API yanıtlarında `Cache-Control` header'ı koymamak. Header yoksa tarayıcı kendi kurallarına göre (heuristic caching) cache'ler ve bu beklenmedik sonuçlara yol açar. Dinamik API yanıtları için `Cache-Control: no-store` belirtmek iyi bir pratiktir.
:::

---

## Pratik Uygulamalar

:::exercise
### Alistirma 1: DNS Kayit Turleri Analizi (Kolay)

Farkli DNS kayit turlerini sorgulayarak DNS sisteminin nasil calistigini gozlemle.

```bash
# 1. A kaydi — IP adresini bul
nslookup google.com
nslookup github.com

# 2. MX kaydi — Mail sunucularini bul
nslookup -type=MX google.com
nslookup -type=MX github.com

# 3. TXT kaydi — SPF, DKIM gibi dogrulama kayitlarini gor
nslookup -type=TXT google.com

# 4. CNAME kaydi — Alias kayitlarini bul
nslookup -type=CNAME www.github.com

# 5. NS kaydi — Yetkili name server'lari bul
nslookup -type=NS google.com

# GOREV: Asagidaki tabloyu doldur
# | Domain       | A (IP)       | MX (Mail)       | NS (Name Server) |
# |-------------|-------------|-----------------|-------------------|
# | google.com  |             |                 |                   |
# | github.com  |             |                 |                   |
# | twitter.com |             |                 |                   |
```

**Beklenen Sonuc:** Her domain icin A, MX ve NS kayitlarini bulmus olmalisin. google.com'un birden fazla A kaydi oldugunu (load balancing), MX kayitlarinda oncelik degerlerini gozlemlemelisin.
**Ipucu:** `nslookup -type=ANY domain.com` komutu tum kayit turlerini bir seferde gosterebilir (bazi DNS sunuculari bunu engelleyebilir).

---

### Alistirma 2: Sayfa Yukleme Performansi Olcme (Orta)

DevTools kullanarak bir web sayfasinin yukleme performansini detayli olarak analiz et.

```bash
# 1. Tarayicida F12 > Network tab'ini ac
# 2. "Disable cache" tikla (gercek performansi gormek icin)
# 3. https://www.wikipedia.org adresine git

# GOREV 1: Network tab'inda ilk HTML istegini sec ve Timing bolumunu incele:
# - DNS Lookup: ___ ms
# - TCP Connection: ___ ms
# - TLS Handshake: ___ ms
# - TTFB (Time To First Byte): ___ ms
# - Content Download: ___ ms

# GOREV 2: Tum kaynaklari analiz et:
# - Toplam kac istek yapildi?
# - Toplam kac KB/MB transfer edildi?
# - DOMContentLoaded ne zaman tetiklendi?
# - Load event ne zaman tetiklendi?

# GOREV 3: Cache-Control header'larini incele:
# - HTML dosyasinin Cache-Control degeri ne?
# - CSS dosyalarinin Cache-Control degeri ne?
# - Resim dosyalarinin Cache-Control degeri ne?
# - max-age degerleri ne anlama geliyor?

# 4. Ayni sayfayi tekrar yukle (cache acik) ve sureleri karsilastir
```

**Beklenen Sonuc:** Cache'siz yukleme ile cache'li yukleme arasinda belirgin fark gozlemlemelisin. DNS Lookup suresi ikinci istekte 0ms olmali (cache). TTFB genelde en uzun sure olmali.
**Ipucu:** Network tab'inda "Size" kolonunda "(from cache)" veya "(from disk cache)" goruyorsan kaynak cache'ten yuklenmis demektir.

---

### Alistirma 3: Lighthouse ile Performance Audit (Zor)

DevTools Lighthouse tab'ini kullanarak farkli web sitelerinin performansini olc ve karsilastir.

```bash
# 1. DevTools > Lighthouse tab'ini ac
# 2. Kategoriler: Performance, Accessibility, Best Practices, SEO sec
# 3. "Analyze page load" butonuna tikla

# GOREV: 3 farkli siteyi test et ve sonuclari karsilastir:
# Site 1: https://www.wikipedia.org (basit, hizli site)
# Site 2: Kendi sectigin bir haber sitesi
# Site 3: Kendi sectigin bir e-ticaret sitesi

# Karsilastirma tablosu:
# | Metrik                    | Wikipedia | Haber Sitesi | E-ticaret |
# |--------------------------|-----------|-------------|-----------|
# | Performance Score        |           |             |           |
# | FCP (First Contentful Paint) |       |             |           |
# | LCP (Largest Contentful Paint) |     |             |           |
# | TBT (Total Blocking Time)  |         |             |           |
# | CLS (Cumulative Layout Shift) |      |             |           |

# GOREV 2: En dusuk performans skorlu site icin:
# - Lighthouse'un onerdigi iyilestirmeleri listele
# - "Eliminate render-blocking resources" ne demek?
# - "Serve images in next-gen formats" ne demek?
# - "Reduce unused JavaScript" nasil yapilir?
```

**Beklenen Sonuc:** Wikipedia en yuksek skoru almali. Haber ve e-ticaret siteleri genelde daha dusuk skor alir (reklam scriptleri, buyuk resimler). Her Core Web Vital metriginin ne oldugunu ve neden onemli oldugunu aciklayabilmelisin.
**Ipucu:** Lighthouse testini Incognito modda yap - extension'lar sonuclari etkileyebilir.
:::

:::knowledge-check
type: multiple_choice
question: "DNS çözümleme sürecinde Recursive Resolver cache miss aldığında sorgulama sırası hangisidir?"
options:
  - "TLD Server → Root Server → Authoritative Server"
  - "Authoritative Server → TLD Server → Root Server"
  - "Root Server → TLD Server → Authoritative Server"
  - "Root Server → Authoritative Server → TLD Server"
correct: 2
explanation: "Recursive Resolver önce Root DNS Server'a sorar (.com nerede?), sonra TLD Server'a sorar (example.com nerede?), son olarak Authoritative Server'dan IP adresini alır. Hiyerarşi yukarıdan aşağıya doğrudur."
:::

:::knowledge-check
type: multiple_choice
question: "Hangisi tarayıcıda reflow (layout) tetiklemez?"
options:
  - "element.offsetWidth okumak"
  - "element.style.width = '200px' yazmak"
  - "element.style.transform = 'translateX(10px)' yazmak"
  - "document.body.appendChild(newDiv) çağırmak"
correct: 2
explanation: "transform özelliği compositing aşamasında çalışır ve layout/reflow tetiklemez. Bu yüzden animasyonlarda transform ve opacity kullanmak performans açısından en iyi pratiktir. Diğer seçeneklerin hepsi reflow tetikler."
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdaki Cache-Control değerlerinden hangisi 'her istekte sunucuya doğrula ama cache'te tut' anlamına gelir?"
options:
  - "no-store"
  - "no-cache"
  - "public, max-age=0"
  - "private"
correct: 1
explanation: "no-cache, cache'i tamamen devre dışı bırakmaz. Yanıtı cache'te tutar ama her kullanımda sunucudan doğrulama ister (ETag/Last-Modified ile). no-store ise hiç cache'lemez. Bu isimlendirme kafa karıştırıcıdır ama farkı bilmek önemlidir."
:::

:::knowledge-check
type: multiple_choice
question: "Sunucudan istemciye tek yönlü gerçek zamanlı veri akışı için en uygun teknoloji hangisidir?"
options:
  - "HTTP Polling"
  - "WebSocket"
  - "Server-Sent Events (SSE)"
  - "HTTP Long Polling"
correct: 2
explanation: "Server-Sent Events (SSE), sunucudan istemciye tek yönlü veri akışı için tasarlanmıştır. Otomatik yeniden bağlanma desteği vardır ve HTTP üzerinden çalışır. WebSocket çift yönlü iletişim gerektiğinde kullanılır. Tek yönlü akış için SSE daha basit ve yeterlidir."
:::

---

## Mülakat Köşesi

:::interview
**Soru 1:** "DNS poisoning/spoofing nedir ve nasıl önlenir?"

**Beklenen cevap:** DNS poisoning, saldırganın DNS cache'ine sahte kayıtlar enjekte ederek kullanıcıyı yanlış IP adresine yönlendirmesidir. Örneğin banka sitesinin IP'si yerine saldırganın sunucusunun IP'si yerleştirilir. DNSSEC (DNS Security Extensions) ile DNS yanıtları dijital olarak imzalanarak doğrulanır. Ayrıca DNS over HTTPS (DoH) ve DNS over TLS (DoT) ile DNS sorguları şifrelenir.
:::

:::interview
**Soru 2:** "Critical Render Path'i nasıl optimize edersin?"

**Beklenen cevap:**
1. Critical CSS'i inline yap, geri kalanını async yükle
2. JavaScript'e `defer` veya `async` ekle
3. Üçüncü parti domainler için `dns-prefetch` ve `preconnect` kullan
4. Hero image ve critical font için `preload` kullan
5. Resimlere `loading="lazy"` ekle (above-the-fold hariç)
6. Font display stratejisi belirle (`font-display: swap`)
7. HTTP/2 veya HTTP/3 kullanarak multiplexing'den faydalan
8. Lighthouse ile ölç, bottleneck'leri tespit et, iteratif olarak iyileştir
:::

:::interview
**Soru 3:** "HTTP/2 ile HTTP/1.1 arasındaki temel farklar nelerdir?"

**Beklenen cevap:** HTTP/2 binary framing layer kullanır (HTTP/1.1 text-based), multiplexing ile tek bağlantıda birden fazla request/response paralel taşınır (head-of-line blocking sorunu çözülür), header compression (HPACK) ile tekrarlayan header'lar sıkıştırılır ve server push ile sunucu istemci istemeden kaynak gönderebilir. HTTP/3 ise TCP yerine QUIC (UDP tabanlı) kullanarak connection setup süresini daha da azaltır.
:::

---

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6

### Prompt Ornekleri

**1. Konuyu Derinlemesine Anla:**
> "Tarayiciya 'example.com' yazdigimda DNS cozumlemesinin tam adimlarini anlat. Browser cache, OS cache, recursive resolver, root server, TLD server ve authoritative server arasindaki iliskiyi bir diagram gibi acikla. TTL bu surecte nasil bir rol oynuyor?"

*Neden:* DNS cozumleme zincirini uctan uca anlamak, hosting degisikligi ve DNS propagation sorunlarini cozebilmeni saglar

**2. Pratik Uygulama:**
> "Tarayicinin render pipeline'ini adim adim anlat: HTML parsing'den DOM olusturmaya, CSSOM'dan Render Tree'ye, Layout'tan Paint ve Compositing'e. Her adimda performansi etkileyen faktorler neler?"

*Follow-up:* "Bir animasyonda width degistirmek yerine transform kullanmamin performans etkisini reflow, repaint ve compositing acisindan acikla."

**3. Mukemmellik Icin:**
> "Bir web uygulamasinin First Contentful Paint suresini 3 saniyeden 1 saniyenin altina indirmem gerekiyor. Critical Render Path optimizasyonu icin dns-prefetch, preconnect, preload, critical CSS inline, defer/async script stratejilerini bir eylem plani olarak sirala."

### Pair Programming Ipucu
Performans analizi yaparken AI'a Lighthouse raporunu yapistir: "Bu Lighthouse Performance sonuclarini analiz et. LCP, FCP ve CLS metriklerini iyilestirmek icin oncelik sirasina gore ne yapmaliyim?"
:::

:::must-note
- **DNS çözümleme sırası:** Browser Cache → OS Cache → Router Cache → ISP Recursive Resolver → Root Server → TLD Server → Authoritative Server
- **DNS record türleri (en kritik 5):** A (domain→IPv4), AAAA (domain→IPv6), CNAME (domain→domain alias), MX (mail sunucusu), TXT (SPF/DKIM doğrulama)
- **Browser render pipeline 6 adımı:** HTML→DOM | CSS→CSSOM | DOM+CSSOM→Render Tree | Layout (pozisyon/boyut) | Paint (piksel çizimi) | Compositing (katman birleştirme)
- **Critical Render Path kuralları:** Critical CSS inline yap, JS'e defer/async ekle, preconnect/dns-prefetch kullan, hero image'i preload et, lazy loading uygula, font-display: swap belirle
- **Reflow tetiklemeden animasyon:** Sadece `transform` ve `opacity` kullan (GPU composite layer'da çalışır, layout/paint atlanır)
- **"URL yazdığında ne olur" özet:** URL parse → HSTS kontrol → DNS resolution → TCP 3-way handshake → TLS handshake → HTTP request → Server processing → HTTP response → HTML parse + render pipeline → Subresource loading
- **Cache-Control karışan ikili:** `no-cache` = cache'te tut ama her seferinde sunucudan doğrula (ETag ile), `no-store` = hiç cache'leme
- **WebSocket vs SSE vs HTTP (1 satır):** HTTP = request-response tek yön, SSE = sunucu→istemci tek yön + otomatik reconnect, WebSocket = çift yönlü full-duplex (chat/oyun için)
- **TTL stratejisi:** Hosting değişikliğinden önce TTL'i 300s'ye düşür, değişikliği yap, sonra tekrar yükselt
- **Content hash caching:** Statik dosyaları `app.a1b2c3.js` gibi hash'le, `max-age=31536000` ver, dosya değişince hash değişir = otomatik cache invalidation
:::

:::senior-learns
**Senior developer DNS ve browser internals'ı nasıl öğrenir?**

- **Araç seti her şeydir.** `dig`, `nslookup`, `traceroute` komutlarını refleks haline getir. Bir domain'in DNS zincirini `dig +trace example.com` ile uçtan uca görmeden "DNS biliyorum" deme. Chrome DevTools Network tab'ında Timing breakdown'ı okuyamıyorsan, performans hakkında konuşma hakkın yok.
- **Specification oku, blog değil.** RFC 1035 (DNS), HTML Living Standard'ın parsing bölümü kuru ve sıkıcı görünür ama bir senior'ı junior'dan ayıran şey budur. Blog yazıları basitleştirir, spec gerçeği gösterir.
- **Kendi lab ortamını kur.** Local DNS server (dnsmasq veya BIND) kurarak DNS'i elle yönet. `/etc/hosts` dosyasını manipüle et, custom domain'ler oluştur, TTL'lerle oyna. Teoriyi pratiğe dökmeden öğrenme tamamlanmaz.
- **DevTools Performance tab'ını günlük kullan.** Flame chart'ta Layout, Paint, Composite sürelerin gör. `will-change` property'sinin layer promotion'ı nasıl tetiklediğini Layers panel'inden izle. Rendering tab'ında "Paint flashing" ve "Layout shift regions" aktif et.
- **Performans bütçesi belirle.** "Sayfam hızlı" yerine "DNS lookup < 50ms, TTFB < 200ms, FCP < 1s, LCP < 2.5s" de. Ölçemediğin şeyi iyileştiremezsin. Lighthouse CI'ı pipeline'ına ekle ve her PR'da performans regresyonunu yakala.
- **Ağ katmanını simüle et.** DevTools'ta throttling yaparak 3G bağlantıda sayfanın nasıl yüklendiğini gör. WebPageTest ile farklı coğrafyalardan test et. Gerçek kullanıcı verisi (RUM) topla, lab verisi tek başına yetmez.
- **Kaynak kodu oku.** Chromium'un Blink rendering engine kaynak koduna göz at. `LayoutObject`, `PaintLayer`, `CompositedLayerMapping` sınıflarını incele. Tarayıcının nasıl çalıştığını tarayıcının kendisinden öğren.
- **Mindset: "Neden yavaş?" değil, "Hangi adım yavaş?"** Senior developer problemi parçalar. DNS mi yavaş? TCP handshake mi? TTFB mi? Render-blocking resource mu? Her katmanı izole ederek ölçer ve spesifik çözüm uygular.
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Resolution** (rez-uh-loo-shun) → Çözümleme
   *"DNS resolution converts domain names into IP addresses."*

2. **Rendering** (ren-duh-ring) → Görüntüleme / Ekrana Çizme
   *"The browser rendering pipeline transforms HTML into pixels on the screen."*

3. **Cache** (kash) → Önbellek
   *"Browser cache stores frequently accessed resources locally to reduce load times."*

4. **Compositing** (kom-poz-it-ing) → Katman Birleştirme
   *"GPU compositing enables smooth 60fps animations by avoiding layout recalculations."*

5. **Latency** (ley-ten-see) → Gecikme
   *"CDNs reduce latency by serving content from geographically closer edge servers."*

**Okuma Egzersizi:** Google Web Fundamentals'ta "Critical Rendering Path" makalesini İngilizce oku: https://web.dev/articles/critical-rendering-path

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "DNS ve tarayıcı render pipeline dersini tamamladım"
→ Örnek: `docs: complete DNS and browser render pipeline lesson notes`
:::

:::external-resource
- **How DNS Works:** howdns.works (interaktif gorsel anlatim, ucretsiz)
- **web.dev:** "Critical Rendering Path" serisi (Google, ucretsiz)
- **MDN Web Docs:** "How browsers work" (detayli tarayici mimarisi, ucretsiz)
- **Cloudflare Learning Center:** "What is DNS?" (anlasilir anlatim, ucretsiz)
- **Chrome DevTools Docs:** "Analyze Runtime Performance" (performans analizi rehberi, ucretsiz)
:::
