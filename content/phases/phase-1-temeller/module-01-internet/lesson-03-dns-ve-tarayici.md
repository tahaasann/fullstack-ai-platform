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

### Prompt Örnekleri

**1. Konuyu Derinlemesine Anla:**
> "Tarayiciya 'example.com' yazdigimda DNS cozumlemesinin tam adimlarini anlat. Browser cache, OS cache, recursive resolver, root server, TLD server ve authoritative server arasindaki iliskiyi bir diagram gibi acikla. TTL bu surecte nasil bir rol oynuyor?"

*Neden:* DNS cozumleme zincirini uctan uca anlamak, hosting degisikligi ve DNS propagation sorunlarini cozebilmeni saglar

**2. Pratik Uygulama:**
> "Tarayicinin render pipeline'ini adim adim anlat: HTML parsing'den DOM oluşturmaya, CSSOM'dan Render Tree'ye, Layout'tan Paint ve Compositing'e. Her adimda performansi etkileyen faktorler neler?"

*Follow-up:* "Bir animasyonda width degistirmek yerine transform kullanmamin performans etkisini reflow, repaint ve compositing acisindan acikla."

**3. Mukemmellik Icin:**
> "Bir web uygulamasinin First Contentful Paint suresini 3 saniyeden 1 saniyenin altina indirmem gerekiyor. Critical Render Path optimizasyonu icin dns-prefetch, preconnect, preload, critical CSS inline, defer/async script stratejilerini bir eylem plani olarak sirala."

### Pair Programming Ipucu
Performans analizi yaparken AI'a Lighthouse raporunu yapistir: "Bu Lighthouse Performance sonuclarini analiz et. LCP, FCP ve CLS metriklerini iyilestirmek icin oncelik sirasina gore ne yapmaliyim?"
:::

:::exercise
### Alıştırma 4: DNS Record Oluşturucu

**Görev:** Bir domain için DNS zone dosyası oluşturan bir Python programı yaz. Farklı record türlerini desteklesin.

**Başlangıç kodu:**
```python
class DNSZone:
    def __init__(self, domain: str, ttl: int = 3600):
        self.domain = domain
        self.ttl = ttl
        self.records: list[dict] = []

    def add_a(self, name: str, ip: str):
        """A kaydı ekle (domain -> IPv4)."""
        # TODO: {"type": "A", "name": name, "value": ip, "ttl": self.ttl}
        pass

    def add_cname(self, name: str, target: str):
        """CNAME kaydı ekle (alias -> domain)."""
        pass

    def add_mx(self, priority: int, mail_server: str):
        """MX kaydı ekle (mail sunucusu)."""
        pass

    def add_txt(self, name: str, value: str):
        """TXT kaydı ekle (SPF, DKIM vs.)."""
        pass

    def generate_zone_file(self) -> str:
        """BIND formatinda zone dosyasi olustur."""
        # TODO: Her record'u BIND formatinda yaz
        # Ornek: example.com.  3600  IN  A  93.184.216.34
        pass

# Test
zone = DNSZone("example.com")
zone.add_a("@", "93.184.216.34")
zone.add_a("www", "93.184.216.34")
zone.add_a("api", "93.184.216.35")
zone.add_cname("blog", "example.wordpress.com")
zone.add_mx(10, "mail1.example.com")
zone.add_mx(20, "mail2.example.com")
zone.add_txt("@", "v=spf1 include:_spf.google.com ~all")

print(zone.generate_zone_file())
```

**Beklenen çıktı:**
```
; Zone file for example.com
$TTL 3600

example.com.      3600  IN  A      93.184.216.34
www.example.com.  3600  IN  A      93.184.216.34
api.example.com.  3600  IN  A      93.184.216.35
blog.example.com. 3600  IN  CNAME  example.wordpress.com.
example.com.      3600  IN  MX     10 mail1.example.com.
example.com.      3600  IN  MX     20 mail2.example.com.
example.com.      3600  IN  TXT    "v=spf1 include:_spf.google.com ~all"
```

**İpucu:** `@` sembolü domain'in kendisini temsil eder. CNAME ve MX değerleri nokta ile biter.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: DOM Ağacı Oluşturucu

**Görev:** Basit bir HTML string'ini parse ederek DOM ağacı oluşturan bir program yaz.

**Başlangıç kodu:**
```python
class DOMNode:
    def __init__(self, tag: str, attributes: dict = None):
        self.tag = tag
        self.attributes = attributes or {}
        self.children: list = []
        self.text: str = ""

    def add_child(self, child):
        self.children.append(child)
        return child

    def print_tree(self, indent: int = 0):
        """DOM agacini indentli olarak yazdir."""
        prefix = "  " * indent
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attributes.items())
        attr_str = f" {attrs}" if attrs else ""
        print(f"{prefix}<{self.tag}{attr_str}>")
        if self.text:
            print(f"{prefix}  \"{self.text}\"")
        for child in self.children:
            child.print_tree(indent + 1)

# TODO: build_dom fonksiyonu yaz - HTML etiketlerini parse ederek agac olussun
def build_dom(html_structure: list) -> DOMNode:
    """
    Basitlestirilmis HTML yapisini DOM agacina cevir.
    html_structure: [("tag", {attrs}, [children], "text")]
    """
    pass

# Test - Manuel DOM olusturma
html = DOMNode("html", {"lang": "tr"})
head = html.add_child(DOMNode("head"))
title = head.add_child(DOMNode("title"))
title.text = "Sayfa Basligi"

body = html.add_child(DOMNode("body"))
header = body.add_child(DOMNode("header", {"class": "main-header"}))
h1 = header.add_child(DOMNode("h1"))
h1.text = "Merhaba Dunya"

nav = header.add_child(DOMNode("nav"))
ul = nav.add_child(DOMNode("ul"))
for item in ["Ana Sayfa", "Hakkimda", "Iletisim"]:
    li = ul.add_child(DOMNode("li"))
    a = li.add_child(DOMNode("a", {"href": f"/{item.lower().replace(' ', '-')}"}))
    a.text = item

main = body.add_child(DOMNode("main"))
p = main.add_child(DOMNode("p"))
p.text = "Icerik buraya gelecek"

html.print_tree()
```

**Beklenen çıktı:**
```
<html lang="tr">
  <head>
    <title>
      "Sayfa Basligi"
  <body>
    <header class="main-header">
      <h1>
        "Merhaba Dunya"
      <nav>
        <ul>
          <li>
            <a href="/ana-sayfa">
              "Ana Sayfa"
          <li>
            <a href="/hakkimda">
              "Hakkimda"
          <li>
            <a href="/iletisim">
              "Iletisim"
    <main>
      <p>
        "Icerik buraya gelecek"
```

**İpucu:** Her `DOMNode` alt elemanlarını `children` listesinde tutar. Recursive `print_tree` ile ağacı görselleştir.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 6: Critical Render Path Analiz Aracı

**Görev:** Bir HTML sayfasındaki kaynakları analiz edip Critical Render Path'i etkileyen sorunları tespit eden bir script yaz.

**Başlangıç kodu:**
```python
import re

def analyze_crp(html: str) -> dict:
    """
    HTML'deki render-blocking kaynaklari analiz et.
    Returns: {"blocking_css": list, "blocking_js": list,
              "async_js": list, "defer_js": list,
              "preload": list, "issues": list, "score": int}
    """
    # TODO:
    # 1. <link rel="stylesheet"> -> render-blocking CSS
    # 2. <script src="..."> (async/defer olmayan) -> render-blocking JS
    # 3. <script async>, <script defer> -> non-blocking JS
    # 4. <link rel="preload"> -> preload kaynaklar
    # 5. Sorunlari tespit et ve skor hesapla
    pass

# Test
test_html = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/vendor.css">
    <link rel="stylesheet" href="https://cdn.example.com/bootstrap.css">
    <script src="/js/analytics.js"></script>
    <script src="/js/app.js"></script>
    <link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
</head>
<body>
    <h1>Test Page</h1>
    <script src="/js/utils.js" async></script>
    <script src="/js/vendor.js" defer></script>
    <img src="/img/hero.jpg" loading="lazy">
</body>
</html>
"""

result = analyze_crp(test_html)
print("=== Critical Render Path Analizi ===")
print(f"\nRender-blocking CSS ({len(result['blocking_css'])}):")
for css in result['blocking_css']:
    print(f"  - {css}")

print(f"\nRender-blocking JS ({len(result['blocking_js'])}):")
for js in result['blocking_js']:
    print(f"  - {js}")

print(f"\nAsync JS: {len(result['async_js'])}")
print(f"Defer JS: {len(result['defer_js'])}")
print(f"Preload:  {len(result['preload'])}")

print(f"\nSorunlar:")
for issue in result['issues']:
    print(f"  ⚠ {issue}")

print(f"\nPerformans Skoru: {result['score']}/100")
```

**Beklenen çıktı:**
```
=== Critical Render Path Analizi ===

Render-blocking CSS (3):
  - /css/main.css
  - /css/vendor.css
  - https://cdn.example.com/bootstrap.css

Render-blocking JS (2):
  - /js/analytics.js
  - /js/app.js

Async JS: 1
Defer JS: 1
Preload:  1

Sorunlar:
  - 2 render-blocking JS dosyasi var, defer/async ekleyin
  - 3. parti CSS render'i blokluyor: bootstrap.css
  - analytics.js async olmali

Performans Skoru: 45/100
```

**İpucu:** `re.findall()` ile HTML etiketlerini bul. `async` veya `defer` attribute kontrolü yap.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: DNS Cache Simülatörü

**Görev:** TTL tabanlı bir DNS cache simülatörü yaz. Cache hit/miss istatistikleri tutsun.

**Başlangıç kodu:**
```python
import time

class DNSCache:
    def __init__(self):
        self.cache: dict[str, dict] = {}
        self.stats = {"hits": 0, "misses": 0, "expired": 0}

    def put(self, domain: str, ip: str, ttl: int):
        """DNS kaydini cache'e ekle."""
        # TODO: domain, ip, ttl ve ekleme zamani kaydet
        pass

    def get(self, domain: str) -> str | None:
        """Cache'ten DNS kaydi al. TTL dolmussa None dondur."""
        # TODO:
        # 1. Cache'te var mi?
        # 2. TTL dolmus mu? (time.time() - stored_at > ttl)
        # 3. Hit/miss/expired istatistiklerini guncelle
        pass

    def flush(self):
        """Tum cache'i temizle."""
        self.cache.clear()

    def print_stats(self):
        """Cache istatistiklerini goster."""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total * 100) if total > 0 else 0
        print(f"Hits: {self.stats['hits']}, Misses: {self.stats['misses']}, "
              f"Expired: {self.stats['expired']}, Hit Rate: {hit_rate:.1f}%")

# Test
dns = DNSCache()

# DNS kayitlari ekle
dns.put("google.com", "142.250.185.14", ttl=300)
dns.put("github.com", "140.82.121.4", ttl=60)
dns.put("example.com", "93.184.216.34", ttl=1)  # 1 saniyelik TTL

# Cache hit
print(dns.get("google.com"))   # 142.250.185.14
print(dns.get("github.com"))   # 140.82.121.4
print(dns.get("example.com"))  # 93.184.216.34

# Cache miss
print(dns.get("unknown.com"))  # None

# TTL testi
time.sleep(1.5)
print(dns.get("example.com"))  # None (TTL doldu)

dns.print_stats()
```

**Beklenen çıktı:**
```
142.250.185.14
140.82.121.4
93.184.216.34
None
None
Hits: 3, Misses: 1, Expired: 1, Hit Rate: 60.0%
```

**İpucu:** `time.time()` ile ekleme zamanını kaydet. `get()` sırasında `current_time - stored_at > ttl` kontrolü yap.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 8: Preload/Prefetch Strateji Oluşturucu

**Görev:** Verilen bir sayfa yapısına göre optimal preload, prefetch ve preconnect stratejisi öneren bir program yaz.

**Başlangıç kodu:**
```python
def generate_resource_hints(page_resources: list[dict]) -> str:
    """
    Sayfa kaynaklarina gore resource hint'ler olustur.
    Her kaynak: {"url": str, "type": str, "critical": bool, "origin": str}
    """
    hints = []

    for resource in page_resources:
        # TODO:
        # 1. Critical + ayni origin -> preload
        # 2. Critical + farkli origin -> preconnect + preload
        # 3. Non-critical + sonraki sayfa icin -> prefetch
        # 4. Font dosyalari -> crossorigin attribute ekle
        # 5. Dogru 'as' attribute'u belirle (style, script, font, image)
        pass

    return "\n".join(hints)

# Test
resources = [
    {"url": "/css/critical.css", "type": "style", "critical": True, "origin": "same"},
    {"url": "/fonts/main.woff2", "type": "font", "critical": True, "origin": "same"},
    {"url": "https://cdn.example.com/vendor.js", "type": "script", "critical": True, "origin": "cross"},
    {"url": "/js/analytics.js", "type": "script", "critical": False, "origin": "same"},
    {"url": "/img/hero.webp", "type": "image", "critical": True, "origin": "same"},
    {"url": "/css/about-page.css", "type": "style", "critical": False, "origin": "same"},
    {"url": "https://fonts.googleapis.com/css2", "type": "style", "critical": True, "origin": "cross"},
]

print("<!-- Resource Hints -->")
print(generate_resource_hints(resources))
```

**Beklenen çıktı:**
```
<!-- Resource Hints -->
<link rel="preload" href="/css/critical.css" as="style">
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preconnect" href="https://cdn.example.com">
<link rel="preload" href="https://cdn.example.com/vendor.js" as="script">
<link rel="prefetch" href="/js/analytics.js" as="script">
<link rel="preload" href="/img/hero.webp" as="image">
<link rel="prefetch" href="/css/about-page.css" as="style">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preload" href="https://fonts.googleapis.com/css2" as="style">
```

**İpucu:** Font dosyaları her zaman `crossorigin` attribute'u gerektirir (CORS nedeniyle). Cross-origin kaynaklar için önce `preconnect` ekle.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: Web Performans Metrik Hesaplayıcı

**Görev:** Simüle edilmiş sayfa yükleme verileriyle Core Web Vitals metriklerini hesaplayan bir program yaz.

**Başlangıç kodu:**
```python
class WebPerformanceAnalyzer:
    def __init__(self):
        self.events: list[dict] = []

    def add_event(self, event_type: str, timestamp_ms: float, details: dict = None):
        """Sayfa yukleme event'i ekle."""
        self.events.append({"type": event_type, "time": timestamp_ms, "details": details or {}})

    def calculate_metrics(self) -> dict:
        """Core Web Vitals ve diger metrikleri hesapla."""
        # TODO:
        # FCP = First Contentful Paint (ilk icerik gorunur)
        # LCP = Largest Contentful Paint (en buyuk icerik gorunur)
        # CLS = Cumulative Layout Shift (toplam layout kaymasi)
        # TBT = Total Blocking Time (50ms ustu bloklayan sureler toplami)
        # TTFB = Time To First Byte (ilk byte alindi)
        pass

    def get_grade(self, metrics: dict) -> dict:
        """Her metrik icin iyi/orta/kotu derecelendirme yap."""
        # TODO: Google thresholds:
        # LCP: Good < 2500ms, Needs improvement < 4000ms, Poor >= 4000ms
        # CLS: Good < 0.1, Needs improvement < 0.25, Poor >= 0.25
        # FCP: Good < 1800ms, Needs improvement < 3000ms, Poor >= 3000ms
        pass

# Test
analyzer = WebPerformanceAnalyzer()
analyzer.add_event("ttfb", 280)
analyzer.add_event("fcp", 1200)
analyzer.add_event("lcp", 2800)
analyzer.add_event("layout_shift", 0, {"score": 0.05})
analyzer.add_event("layout_shift", 500, {"score": 0.03})
analyzer.add_event("layout_shift", 1200, {"score": 0.08})
analyzer.add_event("long_task", 0, {"duration": 120})
analyzer.add_event("long_task", 0, {"duration": 80})
analyzer.add_event("long_task", 0, {"duration": 200})

metrics = analyzer.calculate_metrics()
grades = analyzer.get_grade(metrics)

print("=== Core Web Vitals ===")
for metric, value in metrics.items():
    grade = grades.get(metric, "N/A")
    unit = "ms" if metric != "cls" else ""
    print(f"  {metric.upper():6s}: {value:>8.1f}{unit:2s}  [{grade}]")
```

**Beklenen çıktı:**
```
=== Core Web Vitals ===
  TTFB  :    280.0ms  [Good]
  FCP   :   1200.0ms  [Good]
  LCP   :   2800.0ms  [Needs Improvement]
  CLS   :      0.2    [Needs Improvement]
  TBT   :    300.0ms  [Poor]
```

**İpucu:** TBT = her long task'ın 50ms üstü kısmının toplamı. Örnek: 120ms task -> 70ms blocking time.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 10: CDN Yönlendirme Simülatörü

**Görev:** Bir CDN'in kullanıcıyı en yakın sunucuya yönlendirme mekanizmasını simüle eden bir program yaz.

**Başlangıç kodu:**
```python
import math

class CDNNode:
    def __init__(self, name: str, lat: float, lon: float, capacity: int):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.capacity = capacity
        self.current_load = 0

class CDN:
    def __init__(self):
        self.nodes: list[CDNNode] = []

    def add_node(self, name: str, lat: float, lon: float, capacity: int):
        self.nodes.append(CDNNode(name, lat, lon, capacity))

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Iki nokta arasindaki mesafeyi km cinsinden hesapla."""
        # TODO: Haversine formulunu uygula
        # R = 6371 (Dunyanin yaricapi km)
        pass

    def route_request(self, user_lat: float, user_lon: float) -> dict:
        """
        Kullaniciyi en uygun CDN node'una yonlendir.
        Kriter: mesafe + yuk dagilimi
        Returns: {"node": str, "distance_km": float, "latency_ms": float}
        """
        # TODO:
        # 1. Her node'a mesafeyi hesapla
        # 2. Kapasitesi dolu node'lari ele
        # 3. En yakin uygun node'u sec
        # 4. Tahmini latency hesapla (mesafe / isik hizi * 2 * overhead)
        pass

# Test
cdn = CDN()
cdn.add_node("Istanbul-POP", 41.0082, 28.9784, 1000)
cdn.add_node("Frankfurt-POP", 50.1109, 8.6821, 1000)
cdn.add_node("London-POP", 51.5074, -0.1278, 1000)
cdn.add_node("NewYork-POP", 40.7128, -74.0060, 1000)
cdn.add_node("Tokyo-POP", 35.6762, 139.6503, 1000)

# Farkli lokasyonlardan gelen istekler
users = [
    ("Ankara", 39.9334, 32.8597),
    ("Berlin", 52.5200, 13.4050),
    ("San Francisco", 37.7749, -122.4194),
    ("Sydney", -33.8688, 151.2093),
    ("Izmir", 38.4237, 27.1428),
]

print("=== CDN Yonlendirme ===")
for city, lat, lon in users:
    result = cdn.route_request(lat, lon)
    print(f"{city:15s} -> {result['node']:15s} "
          f"({result['distance_km']:.0f} km, ~{result['latency_ms']:.0f} ms)")
```

**Beklenen çıktı:**
```
=== CDN Yonlendirme ===
Ankara          -> Istanbul-POP    (350 km, ~12 ms)
Berlin          -> Frankfurt-POP   (420 km, ~14 ms)
San Francisco   -> NewYork-POP     (4130 km, ~41 ms)
Sydney          -> Tokyo-POP       (7820 km, ~78 ms)
Izmir           -> Istanbul-POP    (330 km, ~11 ms)
```

**İpucu:** Haversine formülü: `a = sin²(Δlat/2) + cos(lat1)*cos(lat2)*sin²(Δlon/2)`, `d = 2R*asin(√a)`. Latency tahmini: `distance_km / 200 * 2` (fiber optik hızı + overhead).

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Browser Render Süreci Simülasyonu

**Görev:** HTML/CSS'in Render Tree'ye dönüşme sürecini simüle eden bir program yaz.

**Başlangıç kodu:**
```python
class CSSRule:
    def __init__(self, selector: str, properties: dict):
        self.selector = selector
        self.properties = properties

class RenderNode:
    def __init__(self, tag: str, styles: dict, visible: bool = True):
        self.tag = tag
        self.styles = styles
        self.visible = visible
        self.children: list = []

def build_render_tree(dom_nodes: list[dict], css_rules: list[CSSRule]) -> list[RenderNode]:
    """DOM + CSSOM -> Render Tree olustur."""
    render_nodes = []
    for node in dom_nodes:
        styles = {}
        for rule in css_rules:
            if matches_selector(node, rule.selector):
                styles.update(rule.properties)
        visible = styles.get("display") != "none"
        if visible and node["tag"] not in ["head", "script", "style"]:
            rn = RenderNode(node["tag"], styles, visible)
            render_nodes.append(rn)
    return render_nodes

def matches_selector(node: dict, selector: str) -> bool:
    """Basit CSS selector eslestirme."""
    # TODO: tag, .class, #id eslestirme
    if selector.startswith("."):
        return selector[1:] in node.get("classes", [])
    elif selector.startswith("#"):
        return selector[1:] == node.get("id", "")
    else:
        return selector == node["tag"]

# Test
dom = [
    {"tag": "head", "classes": []},
    {"tag": "body", "classes": []},
    {"tag": "h1", "classes": ["title"], "id": "main-title"},
    {"tag": "p", "classes": ["content"]},
    {"tag": "div", "classes": ["hidden"]},
    {"tag": "span", "classes": ["badge"]},
    {"tag": "script", "classes": []},
]

css = [
    CSSRule("h1", {"font-size": "24px", "color": "blue"}),
    CSSRule(".title", {"font-weight": "bold"}),
    CSSRule(".hidden", {"display": "none"}),
    CSSRule("p", {"font-size": "16px", "line-height": "1.5"}),
]

tree = build_render_tree(dom, css)
print("=== Render Tree ===")
for node in tree:
    print(f"  <{node.tag}> visible={node.visible} styles={node.styles}")
```

**Beklenen çıktı:**
```
=== Render Tree ===
  <body> visible=True styles={}
  <h1> visible=True styles={'font-size': '24px', 'color': 'blue', 'font-weight': 'bold'}
  <p> visible=True styles={'font-size': '16px', 'line-height': '1.5'}
  <span> visible=True styles={}
```

**İpucu:** `display: none` olan elemanlar Render Tree'ye dahil edilmez. `<head>`, `<script>` gibi non-visual elemanlar da dahil edilmez.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 12: TTL ve DNS Propagation Simülasyonu

**Görev:** DNS record değişikliğinin farklı cache seviyelerinde nasıl yayıldığını simüle eden bir program yaz.

**Başlangıç kodu:**
```python
import time

class DNSServer:
    def __init__(self, name: str, ttl: int):
        self.name = name
        self.ttl = ttl
        self.cache: dict[str, dict] = {}
        self.upstream: "DNSServer | None" = None

    def resolve(self, domain: str) -> str:
        if domain in self.cache:
            entry = self.cache[domain]
            age = time.time() - entry["cached_at"]
            if age < entry["ttl"]:
                print(f"  [{self.name}] Cache HIT: {domain} -> {entry['ip']} (age: {age:.0f}s)")
                return entry["ip"]
            else:
                print(f"  [{self.name}] Cache EXPIRED: {domain}")
                del self.cache[domain]
        if self.upstream:
            ip = self.upstream.resolve(domain)
            self.cache[domain] = {"ip": ip, "ttl": self.ttl, "cached_at": time.time()}
            print(f"  [{self.name}] Cached: {domain} -> {ip} (TTL: {self.ttl}s)")
            return ip
        return "NXDOMAIN"

    def update_record(self, domain: str, new_ip: str):
        """Authoritative server'da record guncelle."""
        self.cache[domain] = {"ip": new_ip, "ttl": 999999, "cached_at": time.time()}
        print(f"  [{self.name}] Record updated: {domain} -> {new_ip}")

# DNS hiyerarsisi olustur
auth = DNSServer("Authoritative", ttl=999999)
isp = DNSServer("ISP Resolver", ttl=300)
router = DNSServer("Router", ttl=60)
browser = DNSServer("Browser", ttl=30)

browser.upstream = router
router.upstream = isp
isp.upstream = auth

# Baslangic kaydi
auth.update_record("example.com", "93.184.216.34")

print("\n=== Ilk sorgu (tum cache bos) ===")
browser.resolve("example.com")

print("\n=== DNS Degisikligi: Yeni IP ===")
auth.update_record("example.com", "198.51.100.1")

print("\n=== Hemen sonra sorgu (cache hala eski) ===")
browser.resolve("example.com")
```

**Beklenen çıktı:**
```
=== Ilk sorgu (tum cache bos) ===
  [Authoritative] Cache HIT: example.com -> 93.184.216.34
  [ISP Resolver] Cached: example.com -> 93.184.216.34 (TTL: 300s)
  [Router] Cached: example.com -> 93.184.216.34 (TTL: 60s)
  [Browser] Cached: example.com -> 93.184.216.34 (TTL: 30s)

=== DNS Degisikligi: Yeni IP ===
  [Authoritative] Record updated: example.com -> 198.51.100.1

=== Hemen sonra sorgu (cache hala eski) ===
  [Browser] Cache HIT: example.com -> 93.184.216.34 (age: 0s)
```

**İpucu:** DNS propagation süresi = en yüksek TTL değeri. Browser cache'i ilk dolar, son boşalır.

**Zorluk:** Orta
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
