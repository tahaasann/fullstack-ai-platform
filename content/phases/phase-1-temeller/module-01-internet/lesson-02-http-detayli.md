---
id: "http-detayli"
title: "HTTP Protokolü Detaylı: Request, Response, Methods ve Status Codes"
description: "HTTP protokolunun derinlemesine incelenmesi: request/response yapısı, HTTP methodları, status code'lar, header'lar, HTTP versiyonları, HTTPS/TLS ve cookie/session yönetimi."
estimated_minutes: 60
order: 2
tags: ["http", "https", "rest", "status-codes", "tls", "cookies", "web-protocols"]
prerequisites: ["internet-nasil-çalışır"]
---

# HTTP Protokolü Detaylı: Request, Response, Methods ve Status Codes

:::realworld
Her gün yüzlerce HTTP isteği yapıyorsun farkında olmadan. Bir Instagram hikayesine bakmak, bir tweet atmak, Netflix'te film izlemek - bunların hepsi HTTP üzerinden gerçekleşiyor. Bir frontend developer olarak fetch() veya axios ile API çağrısı yaptığında, bir backend developer olarak endpoint yazdığında, HTTP'nin her detayını bilmen gerekiyor. Bu ders, HTTP'yi "sadece biliyorum" seviyesinden "derinlemesine anlıyorum" seviyesine taşıyacak.
:::

## Neden HTTP'yi Derinlemesine Bilmelisin?

Web geliştirmenin %90'ı HTTP üzerinden iletişim kurmakla ilgili. REST API tasarlamak, hata ayıklamak, performans optimizasyonu yapmak ve güvenlik açıklarını kapatmak için HTTP'nin iç yapısını anlamalısın.

- API endpoint'lerinde doğru HTTP method'u seçemezsin
- 401 ile 403 farkını bilmezsen authorization bug'larını çözemezsin
- Cache-Control header'ını anlamadan performans optimizasyonu yapamazsın
- CORS hatalarını çözmek için preflight request mekanizmasını bilmelisin

:::deha-tip
Deha seviyesi developer'lar, bir API tasarlarken sadece "çalışıyor mu?" değil, "REST prensiplerine uygun mu?", "idempotent mi?", "doğru status code döndürüyor mu?" sorularını sorar. Browser DevTools'un Network tab'ında her request'in header'larını, timing'ini ve response body'sini analiz ederler.
:::

## HTTP Nedir?

:::concept[HTTP (HyperText Transfer Protocol)]
HTTP, web üzerinde istemci (client) ve sunucu (server) arasında veri alışverişini sağlayan uygulama katmanı protokolüdür. Stateless (durumsuz) bir protokoldür - her istek bağımsızdır.

**Türkçe karsiligi:** Hiper Metin Transfer Protokolu
**Ne ise yarar:** Tarayici ile sunucu arasinda web sayfalarini, resimleri, API verilerini ve diger kaynaklari tasir
**Gerçek hayat benzetmesi:** Bir restoranda garson (HTTP) senin siparisini (request) mutfaga (server) goturur ve yemegi (response) sana getirir. Garson bir önceki siparisini hatirlamaz (stateless).
:::

HTTP bir request-response protokoludur. Client bir istek gönderir, server bir yanit döndürür. Bu kadar basit ama detaylarda sahane bir muhendislik yatiyor.

## HTTP Request Yapısı

Bir HTTP request'i 4 ana bileşenden oluşur:

:::code[text]{title="HTTP Request Yapısı"}
POST /api/users HTTP/1.1          ← Request Line (Method + URL + Version)
Host: api.example.com             ← Headers (Başlıklar)
Content-Type: application/json
Authorization: Bearer eyJhbGci...
Accept: application/json
User-Agent: Mozilla/5.0

{                                  ← Body (Gövde - opsiyonel)
  "name": "Taha",
  "email": "taha@example.com"
}
:::

### 1. Request Line

Request line 3 parcadan oluşur:
- **Method:** Yapılacak işlemi belirtir (GET, POST, PUT, DELETE vb.)
- **URL/Path:** Hedef kaynagi gösterir (/api/users)
- **HTTP Version:** Kullanılan HTTP surumu (HTTP/1.1, HTTP/2)

### 2. Headers

Header'lar request hakkinda ek bilgi tasir. Key-value ciftleri olarak yazilir.

### 3. Body

Request body, sunucuya gonderilecek veriyi içerir. GET ve DELETE isteklerinde genellikle body olmaz. POST ve PUT isteklerinde body zorunludur.

## HTTP Response Yapısı

:::code[text]{title="HTTP Response Yapısı"}
HTTP/1.1 200 OK                   ← Status Line (Version + Code + Reason)
Content-Type: application/json    ← Response Headers
Cache-Control: max-age=3600
Set-Cookie: session=abc123
X-Request-Id: req-789

{                                  ← Response Body
  "id": 1,
  "name": "Taha",
  "email": "taha@example.com",
  "createdAt": "2026-03-20T10:00:00Z"
}
:::

### Status Line

- **HTTP Version:** HTTP/1.1
- **Status Code:** 200 (sayisal kod)
- **Reason Phrase:** OK (insan tarafindan okunabilir açıklama)

## HTTP Methods (HTTP Yöntemleri)

:::concept[HTTP Method (İng: HTTP Method / Verb)]
HTTP method, bir kaynak üzerinde yapilmak istenen işlemi belirtir. REST API tasariminin temelini oluşturur.

**Türkçe karsiligi:** HTTP Yontemi / Fiili
**Ne ise yarar:** Sunucuya "bu kaynakla ne yapmak istiyorum" bilgisini iletir
**Gerçek hayat benzetmesi:** Bir kutuphanede kitap için yapabileceklerin: bak (GET), yeni kitap ekle (POST), kitabi değiştir (PUT), sayfasini duzelt (PATCH), kitabi sil (DELETE)
:::

:::comparison
| Method | Amac | Body | Idempotent | Safe | Kullanım |
|--------|------|------|------------|------|----------|
| GET | Veri okuma | Yok | Evet | Evet | Kullanıcı listesi getir |
| POST | Yeni kayıt oluşturma | Var | Hayir | Hayir | Yeni kullanıcı oluştur |
| PUT | Tamamen güncelleme | Var | Evet | Hayir | Kullanıcı bilgisini tamamen değiştir |
| PATCH | Kismi güncelleme | Var | Hayir | Hayir | Sadece email adresini değiştir |
| DELETE | Silme | Genellikle yok | Evet | Hayir | Kullanıcıyı sil |
| HEAD | Sadece header al | Yok | Evet | Evet | Dosya boyutunu kontrol et |
| OPTIONS | Izin verilen method'lari sor | Yok | Evet | Evet | CORS preflight request |

**Idempotent:** Ayni istegi 10 kez gönderirsen de sonuç ayni olur. PUT ile bir kullanıcıyı güncellemek idempotent'tir - 10 kez gönderirsen de ayni sonucu alirsin. POST ile yeni kullanıcı oluşturmak idempotent değildir - 10 kez gönderirsen 10 kullanıcı oluşur.

**Safe:** Sunucudaki veriyi değiştirmez. GET ve HEAD safe'tir çünkü sadece okuma yapar.
:::

### Her Method'un Detayli Kullanımı

:::code[javascript]{title="HTTP Methods - Fetch API Örnekleri"}
// GET - Veri okuma
const users = await fetch('/api/users');
const user = await fetch('/api/users/42');

// POST - Yeni kayıt oluşturma
const newUser = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Taha', email: 'taha@test.com' })
});

// PUT - Tamamen güncelleme (tüm alanlari gondermelisin)
await fetch('/api/users/42', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Taha A.', email: 'taha@new.com', role: 'admin' })
});

// PATCH - Kismi güncelleme (sadece değişen alanlari gönder)
await fetch('/api/users/42', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'taha@updated.com' })
});

// DELETE - Silme
await fetch('/api/users/42', { method: 'DELETE' });
:::

:::beginner-mistake
Yaygin hata: PUT ve PATCH'i karistirmak. PUT tüm kaynagi değiştirir - göndermediğin alanlari siler veya null yapar. PATCH sadece belirttigin alanlari günceller. Bir kullanıcının sadece email'ini değiştirmek istiyorsan PATCH kullan, PUT değil. PUT ile sadece email gönderirsen, diger alanlar kaybolabilir.
:::

:::beginner-mistake
Yaygin hata: Her sey için POST kullanmak. "POST /getUsers", "POST /deleteUser/42" gibi endpoint'ler REST prensiplerini ihlal eder. Doğru yaklaşım: GET /users, DELETE /users/42. Method zaten işlemi belirtiyor, URL'de fiil kullanma.
:::

## HTTP Status Codes (Durum Kodlari)

:::concept[Status Code (İng: Status Code)]
Status code, sunucunun istege verdigi yanitin durumunu belirten 3 haneli sayisal koddur. Bes kategoriye ayrilir.

**Türkçe karsiligi:** Durum Kodu
**Ne ise yarar:** Client'a istegin başarılı mi, hatali mi, yönlendirme mi gerektigini bildirir
**Gerçek hayat benzetmesi:** Restoranda garsonun cevaplari: "Hazirliyoruz" (1xx), "Buyurun yemeginiz" (2xx), "O yemek başka subemizde" (3xx), "Yanlis sipariş verdiniz" (4xx), "Mutfakta yangin çıktı" (5xx)
:::

### 1xx - Bilgilendirme (Informational)

Nadiren karsilasirsin ama bilmelisin:
- **100 Continue:** "Body'yi gonderebilirsin, header'lari aldim"
- **101 Switching Protocols:** WebSocket baglantisina geçiş
- **103 Early Hints:** Preload ipuclari (HTTP/2+)

### 2xx - Başarı (Success)

:::code[text]{title="2xx Status Codes"}
200 OK              → Istek başarılı. GET için veri dondu, POST için işlem tamam
201 Created         → Yeni kaynak olusturuldu (POST başarılı)
204 No Content      → Başarılı ama donecek veri yok (DELETE sonrası)
206 Partial Content → Kismi içerik (büyük dosya indirme, video streaming)
:::

:::tip
POST ile yeni kayıt olusturdugunda 201 Created don, 200 değil. 201 donunce, response body'de olusturulan kaynagi ve Location header'inda yeni kaynağin URL'sini gönder. Bu REST best practice'tir.
:::

### 3xx - Yönlendirme (Redirection)

:::code[text]{title="3xx Status Codes"}
301 Moved Permanently   → Kaynak kalici olarak taşındı (SEO için önemli!)
302 Found               → Geçici yönlendirme
304 Not Modified        → Cache'deki versiyon güncel, tekrar indirme
307 Temporary Redirect  → 302 gibi ama method'u korur
308 Permanent Redirect  → 301 gibi ama method'u korur
:::

:::warning
301 ve 302 kullanırken dikkat: Bazi eski tarayicilar POST istegini GET'e cevirebilir. POST isteklerinde yönlendirme yapiyorsan 307 (geçici) veya 308 (kalici) kullan - bunlar method'u korur.
:::

### 4xx - Client Hatalari

:::code[text]{title="4xx Status Codes - Bunları Ezberle!"}
400 Bad Request         → Hatali istek (validasyon hatasi, yanlis format)
401 Unauthorized        → Kimlik dogrulanmadi (token yok veya gecersiz)
403 Forbidden           → Yetki yok (giriş yaptin ama izinin yok)
404 Not Found           → Kaynak bulunamadi
405 Method Not Allowed  → Bu endpoint POST kabul etmiyor, GET gönderdin
409 Conflict            → Cakisma (ayni email ile 2. kayıt olusturmaya calistin)
415 Unsupported Media   → Desteklenmeyen Content-Type (XML gönderdin, JSON bekliyor)
422 Unprocessable Entity→ Soz dizimi doğru ama anlamsal hata (yas: -5)
429 Too Many Requests   → Rate limit asildi, çok fazla istek gönderdin
:::

:::beginner-mistake
Yaygin hata: 401 ve 403'u karistirmak. 401 "Sen kimsin? Giriş yap." demektir - authentication eksik. 403 "Seni taniyorum ama buna yetkin yok." demektir - authorization eksik. Örneğin: Login olmadan admin paneline girme → 401. Normal kullanıcı olarak admin paneline girme → 403.
:::

### 5xx - Server Hatalari

:::code[text]{title="5xx Status Codes"}
500 Internal Server Error → Sunucuda beklenmeyen hata (bug, exception)
501 Not Implemented       → Bu özellik henuz yazilmadi
502 Bad Gateway           → Proxy/load balancer arkasindaki sunucu yanit vermedi
503 Service Unavailable   → Sunucu geçici olarak kullanilamaz (bakim, aşırı yuk)
504 Gateway Timeout       → Proxy/load balancer arkasindaki sunucu zaman asimina ugradi
:::

:::deha-tip
Production'da 500 hatasi aldığında, bu senin kodundaki bir bug demektir - client'in hatasi değil. Her 500 hatasini logla, alert oluştur ve hızla duzelt. 502/503/504 genellikle altyapi sorunudur - Nginx, load balancer veya upstream servis ile ilgili. Monitoring araclariyla (Sentry, Datadog) bu hatalari takip etmelisin.
:::

:::knowledge-check
type: multiple_choice
question: "Bir kullanıcı giriş yapmis ama admin paneline erismeye çalışıyor ve yetkisi yok. Hangi status code donmelisin?"
options:
  - "401 Unauthorized"
  - "403 Forbidden"
  - "404 Not Found"
  - "400 Bad Request"
correct: 1
explanation: "403 Forbidden kullanılır çünkü kullanıcı kimligini dogrulamis (authenticated) ama bu kaynaga erişim yetkisi (authorized) yoktur. 401 ise kimlik dogrulanmadiginda (token yok/gecersiz) kullanılır."
:::

## HTTP Headers (Basliklar)

Header'lar request ve response hakkinda meta bilgi tasir. En önemli header'lari detayli inceleyelim.

### Content-Type

Gonderilen verinin tipini belirtir.

:::code[text]{title="Yaygın Content-Type Değerleri"}
application/json                → JSON veri (API'lerde en yaygin)
application/x-www-form-urlencoded → HTML form verisi
multipart/form-data             → Dosya yükleme
text/html                       → HTML sayfasi
text/plain                      → Duz metin
application/xml                 → XML veri
image/png, image/jpeg           → Resim dosyalari
application/octet-stream        → Binary veri
:::

### Authorization

Kimlik doğrulama bilgisini tasir.

:::code[text]{title="Authorization Header Formatları"}
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...   → JWT Token (en yaygin)
Authorization: Basic dXNlcjpwYXNz              → Base64 encoded username:password
Authorization: ApiKey sk-abc123...               → API Key
:::

### Cache-Control

Tarayici ve ara sunucularin içerik cache'lemesini kontrol eder.

:::code[text]{title="Cache-Control Direktifleri"}
Cache-Control: no-store              → Hic cache'leme (hassas veri)
Cache-Control: no-cache              → Cache'le ama her seferinde sunucuya sor
Cache-Control: max-age=3600          → 1 saat cache'le
Cache-Control: public, max-age=86400 → Herkes 1 gun cache'leyebilir (CDN dahil)
Cache-Control: private, max-age=600  → Sadece tarayici cache'leyebilir (CDN değil)
Cache-Control: must-revalidate       → Süresi dolunca mutlaka sunucuya sor
:::

:::tip
Statik dosyalar (CSS, JS, resim) için uzun max-age kullan ve dosya adina hash ekle (style.a1b2c3.css). Içerik degistiginde hash değişir, tarayici yeni versiyonu indirir. Bu pattern'e "cache busting" denir.
:::

### CORS Headers

:::concept[CORS (Cross-Origin Resource Sharing)]
CORS, bir web sayfasinin farklı bir domain'deki API'ye istek gonderebilmesi için kullanılan güvenlik mekanizmasidir.

**Türkçe karsiligi:** Crapraz Kaynak Paylasimi
**Ne ise yarar:** frontend.com'dan api.backend.com'a istek gonderebilmeni sağlar
**Gerçek hayat benzetmesi:** Bir ulkenin sınır kapisi gibi - pasaportuna (Origin header) bakar, izin listesinde varsan girersin
:::

:::code[text]{title="CORS Response Headers"}
Access-Control-Allow-Origin: https://myapp.com    → Bu origin'e izin ver
Access-Control-Allow-Origin: *                     → Herkese izin ver (güvenli değil!)
Access-Control-Allow-Methods: GET, POST, PUT       → Izin verilen method'lar
Access-Control-Allow-Headers: Content-Type, Auth   → Izin verilen header'lar
Access-Control-Max-Age: 86400                      → Preflight sonucu 1 gun cache'le
:::

:::beginner-mistake
Yaygin hata: CORS hatasini frontend'de cozmeye çalışmak. CORS bir sunucu tarafi yapilandirmasidir. "Access-Control-Allow-Origin" header'ini SUNUCU gondermeli. Frontend'de proxy kullanmak sadece development için geçici cozumdur, production'da sunucu tarafinda doğru CORS ayarlarini yapman gerekir.
:::

### Preflight Request (OPTIONS)

Tarayici, "basit olmayan" isteklerden önce otomatik olarak OPTIONS istegi gönderir. Bu preflight request, sunucunun bu istege izin verip vermedigini kontrol eder.

:::code[text]{title="Preflight Request Akışı"}
1. Tarayici (otomatik):
   OPTIONS /api/users HTTP/1.1
   Origin: https://myapp.com
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: Content-Type, Authorization

2. Sunucu yaniti:
   HTTP/1.1 204 No Content
   Access-Control-Allow-Origin: https://myapp.com
   Access-Control-Allow-Methods: POST, GET, PUT
   Access-Control-Allow-Headers: Content-Type, Authorization
   Access-Control-Max-Age: 86400

3. Tarayici asil istegi gönderir:
   POST /api/users HTTP/1.1
   Origin: https://myapp.com
   Content-Type: application/json
   Authorization: Bearer token...
:::

## HTTP Versiyonlari: HTTP/1.1 vs HTTP/2 vs HTTP/3

:::comparison
| Özellik | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---------|----------|--------|--------|
| Yil | 1997 | 2015 | 2022 |
| Transport | TCP | TCP | QUIC (UDP üzerinde) |
| Multiplexing | Yok (1 istek/bağlantı) | Var (paralel stream) | Var |
| Header Compression | Yok | HPACK | QPACK |
| Server Push | Yok | Var | Var |
| Head-of-Line Blocking | Var (TCP seviyesi) | Kismi (TCP seviyesi) | Yok |
| Bağlantı kurma | TCP + TLS = 3 RTT | TCP + TLS = 3 RTT | QUIC = 1 RTT (0-RTT mumkun) |

**Pratik etki:** HTTP/2 ile bir web sayfasi yükleme %15-50 daha hızlı olabilir. HTTP/3 özellikle mobil aglarda ve yüksek latency ortamlarinda belirgin fark yaratir.
:::

### HTTP/1.1'in Problemi

:::code[text]{title="HTTP/1.1 - Head-of-Line Blocking"}
Tarayici         Sunucu
  |--- GET /style.css ----->|
  |   (bekle...)            |
  |<-- 200 OK + CSS --------|
  |--- GET /app.js -------->|   ← CSS bitene kadar beklemek zorunda!
  |   (bekle...)            |
  |<-- 200 OK + JS ---------|
  |--- GET /image.png ----->|   ← JS bitene kadar beklemek zorunda!
:::

Tarayicilar bu problemi 6-8 paralel TCP baglantisi acarak cozmeye çalışır ama bu da kaynak israfıdır.

### HTTP/2 Multiplexing

:::code[text]{title="HTTP/2 - Multiplexing ile Paralel İstekler"}
Tarayici         Sunucu
  |=== Stream 1: GET /style.css ===>|
  |=== Stream 2: GET /app.js =====>|   ← Hepsi ayni anda!
  |=== Stream 3: GET /image.png ==>|
  |                                 |
  |<=== Stream 2: JS response =====|   ← Hangisi hazirsa o gelir
  |<=== Stream 1: CSS response ====|
  |<=== Stream 3: IMG response ====|
:::

### HTTP/3 ve QUIC

HTTP/3, TCP yerine QUIC protokolunu kullanır. QUIC, UDP üzerinde çalışan ama TCP'nin guvenilirligini sağlayan bir protokoldur.

Avantajlari:
- **0-RTT bağlantı kurma:** Daha önce baglandigin sunucuya aninda baglan
- **Bağımsız stream'ler:** Bir stream'deki paket kaybi diger stream'leri etkilemez
- **Connection migration:** Wi-Fi'dan 4G'ye gecince bağlantı kopmaz

## HTTPS ve TLS Handshake

:::concept[HTTPS (HTTP Secure)]
HTTPS, HTTP iletisiminin TLS (Transport Layer Security) ile sifrelenmis halidir. Verilerin üçüncü kisiler tarafindan okunamasini ve degistirilememesini sağlar.

**Türkçe karsiligi:** Güvenli HTTP
**Ne ise yarar:** Client ile server arasindaki tüm trafigi sifreler
**Gerçek hayat benzetmesi:** Normal mektup (HTTP) vs muhurlu ve sifreli mektup (HTTPS) - postaci icerigini okuyamaz
:::

### TLS Handshake Süreci

:::code[text]{title="TLS 1.3 Handshake (Basitleştirilmiş)"}
Client                              Server
  |                                    |
  |--- ClientHello ------------------>|  1. "Merhaba, şu şifreleme
  |    (desteklenen algoritmalar,      |     algoritmalarini destekliyorum"
  |     rastgele sayi)                 |
  |                                    |
  |<-- ServerHello -------------------|  2. "Bu algortimayi kullanalim,
  |    (secilen algoritma,             |     al sana sertifikam"
  |     sertifika, anahtar)           |
  |                                    |
  |--- Doğrulama + Şifreleme -------->|  3. Client sertifikayi dogrular,
  |    baslangici                      |     şifreleme baslar
  |                                    |
  |===== SIFRELI Iletişim ============|  Artik tüm veri sifreli
:::

:::warning
HTTPS olmadan gonderdığın her veri (sifreler, kisisel bilgiler, API token'lar) ag üzerinde duz metin olarak akar. Kahvedeki Wi-Fi'da HTTPS olmayan bir siteye giriş yaparsan, ayni agdaki herkes senin sifreni gorebilir. Production'da MUTLAKA HTTPS kullan. Let's Encrypt ile ücretsiz SSL sertifikasi alabilirsin.
:::

## Request/Response Cycle (Istek/Yanit Döngüsü)

Bir HTTP isteginin tam yasam dongusunu inceleyelim:

:::code[text]{title="Tam Request/Response Cycle"}
1. DNS Resolution     → api.example.com → 93.184.216.34  (~20-120ms)
2. TCP Handshake      → SYN → SYN-ACK → ACK              (~1 RTT)
3. TLS Handshake      → ClientHello → ServerHello → Done  (~1-2 RTT)
4. HTTP Request       → GET /api/users gönder
5. Server Processing  → Sunucu istegi isler                (~10-500ms)
6. HTTP Response      → 200 OK + JSON body dondur
7. TCP Connection     → Keep-alive ile bağlantı açık kalir
                        (sonraki istekler 1-3 adimlarini atlar!)
:::

:::tip
HTTP/1.1'de Connection: keep-alive default'tür. Bu sayede her istek için yeni TCP/TLS handshake yapilmaz. Ayni sunucuya yapılan sonraki istekler çok daha hızlıdır. HTTP/2'de bu daha da optimize edilmistir - tek bağlantı üzerinden yuzlerce paralel istek gonderilebilir.
:::

## Cookies ve Session Yönetimi

:::concept[Cookie (İng: Cookie)]
Cookie, sunucunun client tarafinda (tarayicida) sakladigi küçük veri parcalaridir. Her istekte otomatik olarak sunucuya gönderilir. Stateless olan HTTP'ye "hafiza" kazandirir.

**Türkçe karsiligi:** Cerez
**Ne ise yarar:** Oturum yönetimi, kullanıcı tercihleri, takip (tracking)
**Gerçek hayat benzetmesi:** Bir kafede sana verilen musteri karti - her gelisinde karti gosterirsin ve kafeciyi seni tanir
:::

### Cookie Oluşturma ve Kullanma

:::code[text]{title="Cookie Akışı"}
1. Client login istegi gönderir:
   POST /login HTTP/1.1
   Content-Type: application/json
   {"email": "taha@test.com", "password": "***"}

2. Sunucu başarılı login sonrası cookie set eder:
   HTTP/1.1 200 OK
   Set-Cookie: sessionId=abc123; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=86400

3. Sonraki tüm isteklerde tarayici cookie'yi otomatik gönderir:
   GET /api/profile HTTP/1.1
   Cookie: sessionId=abc123
:::

### Cookie Güvenlik Attribute'lari

:::code[text]{title="Cookie Güvenlik Ayarları"}
HttpOnly    → JavaScript ile erisilemez (XSS koruması)
Secure      → Sadece HTTPS üzerinden gönderilir
SameSite    → Cross-site isteklerde gonderilme kurali
  - Strict  → Sadece ayni site'dan gelen isteklerde gönderilir
  - Lax     → Sadece navigasyon (link tiklamasi) ile gönderilir
  - None    → Her yerden gönderilir (Secure ile birlikte kullanilmali)
Max-Age     → Cookie'nin süre bitmesi (saniye cinsinden)
Domain      → Cookie'nin geçerli oldugu domain
Path        → Cookie'nin geçerli oldugu URL yolu
:::

:::warning
Session cookie'lerinde mutlaka HttpOnly, Secure ve SameSite=Strict kullan. HttpOnly olmadan, bir XSS saldirgani document.cookie ile session token'ini calabilir. Secure olmadan, HTTP üzerinden token duz metin olarak gönderilir.
:::

### Session vs Token-Based Authentication

:::comparison
| Özellik | Session-Based | Token-Based (JWT) |
|---------|--------------|-------------------|
| Depolama (Server) | Session store (Redis, DB) | Yok (stateless) |
| Depolama (Client) | Cookie'de session ID | Cookie veya localStorage'da JWT |
| Ölçeklenebilirlik | Zor (shared session store gerekir) | Kolay (her sunucu dogrulayabilir) |
| Invalidation | Kolay (session'i sil) | Zor (token süresi dolana kadar geçerli) |
| Boyut | Küçük (~32 byte session ID) | Büyük (~800+ byte JWT) |
| CSRF riski | Var (cookie otomatik gönderilir) | Az (Authorization header ile) |

**Tavsiye:** Modern web uygulamalarinda genellikle JWT token'lar HttpOnly cookie'de saklanir. Bu, her iki yontemin avantajlarini birleştirir: stateless doğrulama + XSS koruması.
:::

:::knowledge-check
type: multiple_choice
question: "Bir API'den 204 No Content yaniti aldığında ne anlama gelir?"
options:
  - "Sunucuda hata oluştu ve içerik gönderilemedi"
  - "İstek başarılı ama dönecek içerik yok (örn: DELETE sonrası)"
  - "İçerik başka bir URL'ye taşındı"
  - "İstek geçersiz, içerik reddedildi"
correct: 1
explanation: "204 No Content, isteğin başarıyla işlendiğini ama response body'de dönecek veri olmadığını belirtir. DELETE işleminden sonra veya PUT ile güncelleme yapıldığında sıkça kullanılır."
:::

:::knowledge-check
type: multiple_choice
question: "PUT ve PATCH arasindaki temel fark nedir?"
options:
  - "PUT veri okur, PATCH veri yazar"
  - "PUT tamamen günceller (tüm alanlari gönder), PATCH kismi günceller (sadece değişen alanlari gönder)"
  - "PUT idempotent değildir, PATCH idempotent'tir"
  - "Hicbir fark yoktur, ayni işlevi gorurler"
correct: 1
explanation: "PUT tüm kaynagi değiştirir - göndermediğin alanlar kaybolabilir. PATCH sadece belirttigin alanlari günceller. Bir kullanıcının sadece email'ini değiştirmek istiyorsan PATCH kullan."
:::

:::knowledge-check
type: multiple_choice
question: "HTTP/2'nin HTTP/1.1'e gore en büyük avantaji nedir?"
options:
  - "Şifreleme destegi (HTTPS)"
  - "Multiplexing - tek bağlantı üzerinden paralel istekler"
  - "Cookie destegi"
  - "Daha büyük body gonderebilme"
correct: 1
explanation: "HTTP/2'nin en büyük yeniligi multiplexing'tir. Tek TCP baglantisi üzerinden birden fazla istek/yanit paralel olarak gonderilebilir. HTTP/1.1'deki head-of-line blocking problemini çözer."
:::

## Pratik Uygulama

:::exercise
### Alıştırma 1: DevTools ile HTTP Trafigi Analizi (Kolay)

Tarayicida DevTools Network tab'ini kullanarak HTTP trafigini analiz et.

```bash
# 1. Tarayicida F12 ile DevTools ac, Network tab'ina git
# 2. https://jsonplaceholder.typicode.com/posts adresine git
# 3. Asagidaki bilgileri not et:
#    - Request method (GET/POST/...)
#    - Status code (200, 301, 404...)
#    - Content-Type header degeri
#    - Response body (Preview tab)
#    - Timing: DNS Lookup, TTFB sureleri
# 4. Ayni sayfada bir POST istegi gonder:
fetch('https://jsonplaceholder.typicode.com/posts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Test', body: 'Merhaba', userId: 1 })
}).then(r => r.json()).then(console.log)
# 5. Network tab'inda POST istegini bul ve request/response headers'i karsilastir
```

**Beklenen Sonuç:** GET istegi 200 doner ve tüm post'lari getirir. POST istegi 201 (Created) doner ve olusturulan objeyi gösterir. Timing bilgilerinde DNS ve TTFB surelerini gorebilmelisin.
**Ipucu:** Network tab'inda filtreleme butonlarini kullanarak sadece XHR/Fetch isteklerini göster.

---

### Alistirma 2: curl ile HTTP Metodlarini Test Etme (Orta)

Terminalde curl kullanarak farkli HTTP metodlarini test et ve header/body farklarini gozlemle.

```bash
# 1. Basit GET istegi (verbose - tum header'lari gor)
curl -v https://httpbin.org/get

# 2. POST istegi (JSON body ile)
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name":"Ahmet","age":25}'

# 3. PUT istegi (kaynak guncelleme)
curl -X PUT https://httpbin.org/put \
  -H "Content-Type: application/json" \
  -d '{"name":"Ahmet","age":26}'

# 4. DELETE istegi
curl -X DELETE https://httpbin.org/delete

# 5. Sadece header'lari gor (HEAD benzeri)
curl -I https://google.com
# Soru: Status code ne? Neden 301? Location header nereye yonlendiriyor?

# 6. Custom header ekle
curl https://httpbin.org/headers \
  -H "X-Custom-Header: merhaba" \
  -H "Authorization: Bearer test-token-123"
```

**Beklenen Sonuc:** Her istekte farkli HTTP metodu kullanilmali. httpbin.org gonderdigin header ve body'yi aynen geri doner, boylece ne gonderdigini gorebilirsin. google.com 301 ile https'e yonlendirir.
**Ipucu:** `-v` flag'i ile request ve response header'larinin tamamini gorebilirsin. `>` ile baslayan satirlar request, `<` ile baslayan satirlar response header'laridir.

---

### Alıştırma 3: HTTP Status Code Senaryolari (Zor)

httpbin.org kullanarak farklı HTTP status code senaryolarini simule et ve her birinin anlamini açıkla.

```bash
# 1. Basarili response'lar
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/200
curl -w "\nStatus: %{http_code}\n" -X POST https://httpbin.org/status/201
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/204

# 2. Yonlendirme (Redirect)
curl -v https://httpbin.org/redirect/3
# Soru: Kac kez yonlendirme yapildi? -L flag'i ekleyince ne degisir?
curl -L -v https://httpbin.org/redirect/3

# 3. Client Error'lar
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/400
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/401
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/403
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/404
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/429

# 4. Server Error'lar
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/500
curl -w "\nStatus: %{http_code}\n" https://httpbin.org/status/503

# GOREV: Her status code icin bir tablo olustur:
# | Code | Anlami | Gercek Hayat Ornegi |
# |------|--------|---------------------|
# | 200  | OK     | Sayfa basariyla yuklendi |
# | 201  | ...    | ...                 |
# | ...  | ...    | ...                 |
```

**Beklenen Sonuç:** En az 10 farklı status code'u test etmis ve her birinin anlamini ve gerçek hayat ornegini yazabilmis olmalisin. 301 vs 302, 401 vs 403 farklarini aciklayabilmelisin.
**Ipucu:** `-w` flag'i ile response bilgilerini formatli yazdirabilisin. `%{http_code}` status code'u, `%{time_total}` toplam sureyi verir.
:::

:::interview
**Mülakat Sorusu:** "REST API tasarlarken PUT ve PATCH arasindaki farki açıkla. Hangisini ne zaman kullanirsin?"

**Beklenen cevap:**
PUT, bir kaynagi tamamen değiştirmek için kullanılır - tüm alanlari içeren tam bir temsil gondermelisin. Göndermediğin alanlar silinir veya null olur. PUT idempotent'tir.

PATCH, bir kaynagi kismi olarak güncellemek için kullanılır - sadece değişen alanlari gonderirsin. Diger alanlar korunur.

Örnek: Bir kullanıcının sadece email'ini değiştirmek istiyorsam PATCH /users/42 ile { "email": "new@email.com" } gonderirim. PUT kullansaydim, name, role ve diger tüm alanlari da gondermem gerekirdi, aksi halde kaybolabilirlerdi.
:::

:::interview
**Mülakat Sorusu:** "CORS nedir ve neden vardir? Bir CORS hatasini nasil cozersin?"

**Beklenen cevap:**
CORS (Cross-Origin Resource Sharing), tarayicinin güvenlik mekanizmasidir. Bir web sayfasinin, kendisinden farklı bir origin'deki (domain + port + protocol) kaynaklara erisimini kontrol eder.

Same-Origin Policy geregi, frontend.com'dan api.backend.com'a istek gonderilemez. CORS, sunucu tarafinda Access-Control-Allow-Origin header'i ile belirli origin'lere izin vererek bu kisitlamayi kontrolllu şekilde gevsetir.

Çözüm her zaman sunucu tarafindadir: Sunucu, response'a uygun CORS header'larini eklemeli. Frontend'de proxy kullanmak sadece development için geçici cozumdur.
:::

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6

### Prompt Örnekleri

**1. Konuyu Derinlemesine Anla:**
> "REST API tasariminda HTTP method'larinin idempotency ve safety ozelliklerini açıkla. PUT ile PATCH arasindaki farki bir e-ticaret sepet güncelleme senaryosuyla göster. Neden bu ayrim önemli?"

*Neden:* HTTP method semantiklerini gerçek senaryolarla anlamak, doğru API tasarımı yapabilmeni sağlar

**2. Pratik Uygulama:**
> "Bir kullanıcı yönetim API'si için tüm endpoint'leri tasarla. Her endpoint için HTTP method, URL path, request body, response body ve uygun status code'u belirt. CORS preflight request'i de dahil et."

*Follow-up:* "Bu API'ye rate limiting ve cache-control header'lari eklesem, her endpoint için hangi stratejileri kullanmaliyim?"

**3. Mukemmellik Için:**
> "HTTP/1.1, HTTP/2 ve HTTP/3 arasindaki farkları multiplexing, head-of-line blocking ve connection setup acisindan karşılaştır. Bir e-ticaret sitesinin sayfa yükleme performansini her versiyonda nasil etkileyecegini somut sayilarla göster."

### Pair Programming Ipucu
API gelistirirken AI'a curl ciktini yapistir: "Bu curl -v ciktisindaki request/response header'larini analiz et. Güvenlik, performans ve REST best practices acisindan neleri degistirmeliyim?"
:::

:::exercise
### Alıştırma 4: REST API Client Sınıfı

**Görev:** Python ile bir REST API client sınıfı yaz. GET, POST, PUT, DELETE metodlarını desteklesin ve response'ları güzel formatlasın.

**Başlangıç kodu:**
```python
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

class RestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, data: dict = None) -> dict:
        """HTTP istegi gonder ve sonucu dondur."""
        url = f"{self.base_url}{path}"
        # TODO:
        # 1. Request objesi olustur (url, method, headers)
        # 2. data varsa JSON'a cevir ve body olarak ekle
        # 3. urlopen ile istegi gonder
        # 4. Response'u parse et ve dondur: {"status": int, "body": dict, "headers": dict}
        pass

    def get(self, path: str) -> dict:
        return self._request("GET", path)

    def post(self, path: str, data: dict) -> dict:
        return self._request("POST", path, data)

    def put(self, path: str, data: dict) -> dict:
        return self._request("PUT", path, data)

    def delete(self, path: str) -> dict:
        return self._request("DELETE", path)

# Test
client = RestClient("https://jsonplaceholder.typicode.com")

# GET
resp = client.get("/posts/1")
print(f"GET /posts/1 -> Status: {resp['status']}, Title: {resp['body']['title'][:30]}...")

# POST
resp = client.post("/posts", {"title": "Yeni Post", "body": "Icerik", "userId": 1})
print(f"POST /posts -> Status: {resp['status']}, ID: {resp['body']['id']}")

# PUT
resp = client.put("/posts/1", {"title": "Guncellenmis", "body": "Yeni icerik", "userId": 1})
print(f"PUT /posts/1 -> Status: {resp['status']}")

# DELETE
resp = client.delete("/posts/1")
print(f"DELETE /posts/1 -> Status: {resp['status']}")
```

**Beklenen çıktı:**
```
GET /posts/1 -> Status: 200, Title: sunt aut facere repellat pr...
POST /posts -> Status: 201, ID: 101
PUT /posts/1 -> Status: 200
DELETE /posts/1 -> Status: 200
```

**İpucu:** `Request` objesine `method` parametresi ver. JSON body için `data=json.dumps(data).encode()` kullan.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: HTTP Status Code Quiz Uygulaması

**Görev:** Terminal tabanlı bir HTTP status code quiz uygulaması yaz. Rastgele status code gösterip kullanıcıdan anlamını sorarak öğrenmesini sağla.

**Başlangıç kodu:**
```python
import random

STATUS_CODES = {
    200: ("OK", "Istek basarili"),
    201: ("Created", "Kaynak olusturuldu"),
    204: ("No Content", "Basarili ama icerik yok"),
    301: ("Moved Permanently", "Kalici yonlendirme"),
    302: ("Found", "Gecici yonlendirme"),
    304: ("Not Modified", "Cache gecerli, icerik degismedi"),
    400: ("Bad Request", "Hatali istek"),
    401: ("Unauthorized", "Kimlik dogrulama gerekli"),
    403: ("Forbidden", "Erisim reddedildi"),
    404: ("Not Found", "Kaynak bulunamadi"),
    409: ("Conflict", "Catisma var"),
    429: ("Too Many Requests", "Rate limit asildi"),
    500: ("Internal Server Error", "Sunucu hatasi"),
    502: ("Bad Gateway", "Upstream sunucu hatasi"),
    503: ("Service Unavailable", "Sunucu gecici olarak kulanilamaz"),
}

def run_quiz(num_questions: int = 5):
    score = 0
    codes = list(STATUS_CODES.keys())

    for i in range(num_questions):
        # TODO:
        # 1. Rastgele bir status code sec
        # 2. 4 secenekli coktan secmeli soru olustur (1 dogru + 3 yanlis)
        # 3. Kullanicidan cevap al
        # 4. Dogru/yanlis kontrolu yap ve skoru guncelle
        pass

    print(f"\nSonuc: {score}/{num_questions}")

run_quiz()
```

**Beklenen çıktı:**
```
Soru 1/5: HTTP 403 ne anlama gelir?
  A) Kaynak bulunamadi
  B) Erisim reddedildi
  C) Sunucu hatasi
  D) Kimlik dogrulama gerekli
Cevap (A/B/C/D): B
Dogru!

Sonuc: 4/5
```

**İpucu:** `random.sample()` ile yanlış seçenekleri rastgele seç, `random.shuffle()` ile karıştır.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 6: Cookie ve Session Simülatörü

**Görev:** HTTP cookie mekanizmasını simüle eden bir program yaz. Set-Cookie header'ını parse etsin ve sonraki isteklere cookie eklesin.

**Başlangıç kodu:**
```python
from datetime import datetime, timedelta

class CookieJar:
    def __init__(self):
        self.cookies: dict[str, dict] = {}

    def set_cookie(self, header: str):
        """Set-Cookie header'ini parse et ve sakla."""
        # TODO: "name=value; Path=/; Max-Age=3600; HttpOnly; Secure" formatini parse et
        # Ornek: "session_id=abc123; Path=/; Max-Age=3600; HttpOnly"
        pass

    def get_cookie_header(self, path: str = "/") -> str:
        """Gecerli cookie'leri Cookie header formatinda dondur."""
        # TODO: Suresi dolmamis ve path'i uygun cookie'leri "name=value; name2=value2" formatinda dondur
        pass

    def is_expired(self, cookie_name: str) -> bool:
        """Cookie'nin suresinin dolup dolmadigini kontrol et."""
        pass

# Test
jar = CookieJar()

# Sunucu Set-Cookie header'lari gonderiyor
jar.set_cookie("session_id=abc123; Path=/; Max-Age=3600; HttpOnly")
jar.set_cookie("theme=dark; Path=/; Max-Age=86400")
jar.set_cookie("tracking=xyz; Path=/analytics; Max-Age=2592000")

# Istemci cookie header'ini olustur
print(f"Cookie header (/): {jar.get_cookie_header('/')}")
print(f"Cookie header (/analytics): {jar.get_cookie_header('/analytics')}")
print(f"Toplam cookie: {len(jar.cookies)}")
print(f"session_id expired: {jar.is_expired('session_id')}")
```

**Beklenen çıktı:**
```
Cookie header (/): session_id=abc123; theme=dark
Cookie header (/analytics): session_id=abc123; theme=dark; tracking=xyz
Toplam cookie: 3
session_id expired: False
```

**İpucu:** `header.split(";")` ile attributeleri ayır. Her attribute'u `strip()` ile temizle.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: CORS Simülatörü

**Görev:** CORS (Cross-Origin Resource Sharing) kontrolünü simüle eden bir fonksiyon yaz. Origin, method ve headers'a göre isteğin kabul edilip edilmeyeceğini belirlesin.

**Başlangıç kodu:**
```python
class CORSPolicy:
    def __init__(self):
        self.allowed_origins: list[str] = []
        self.allowed_methods: list[str] = ["GET", "HEAD"]
        self.allowed_headers: list[str] = []
        self.allow_credentials: bool = False
        self.max_age: int = 0

    def allow_origin(self, origin: str):
        self.allowed_origins.append(origin)
        return self

    def allow_method(self, method: str):
        self.allowed_methods.append(method)
        return self

    def allow_header(self, header: str):
        self.allowed_headers.append(header)
        return self

    def check_request(self, origin: str, method: str, headers: list[str] = None) -> dict:
        """
        CORS istegini kontrol et.
        Returns: {"allowed": bool, "reason": str, "response_headers": dict}
        """
        # TODO:
        # 1. Origin kontrolu (allowed_origins'te var mi veya "*" mi?)
        # 2. Method kontrolu
        # 3. Header kontrolu (preflight icin)
        # 4. Uygun response headers olustur
        pass

    def is_preflight(self, method: str) -> bool:
        """Preflight (OPTIONS) gereken bir istek mi?"""
        # TODO: "Simple request" degilse preflight gerekir
        # Simple: GET/HEAD/POST + standart headers
        pass

# Test
cors = CORSPolicy()
cors.allow_origin("https://frontend.example.com")
cors.allow_origin("https://admin.example.com")
cors.allow_method("POST")
cors.allow_method("PUT")
cors.allow_method("DELETE")
cors.allow_header("Authorization")
cors.allow_header("Content-Type")

# Test senaryolari
tests = [
    ("https://frontend.example.com", "GET", []),
    ("https://frontend.example.com", "POST", ["Content-Type"]),
    ("https://evil.com", "GET", []),
    ("https://frontend.example.com", "DELETE", ["Authorization"]),
    ("https://admin.example.com", "PUT", ["Content-Type", "X-Custom"]),
]

for origin, method, headers in tests:
    result = cors.check_request(origin, method, headers)
    status = "ALLOWED" if result["allowed"] else "BLOCKED"
    print(f"{origin:40s} {method:6s} -> {status}: {result['reason']}")
```

**Beklenen çıktı:**
```
https://frontend.example.com             GET    -> ALLOWED: Origin and method permitted
https://frontend.example.com             POST   -> ALLOWED: Origin and method permitted
https://evil.com                         GET    -> BLOCKED: Origin not allowed
https://frontend.example.com             DELETE -> ALLOWED: Origin and method permitted
https://admin.example.com                PUT    -> BLOCKED: Header 'X-Custom' not allowed
```

**İpucu:** Simple request'ler preflight gerektirmez: GET/HEAD/POST + sadece `Accept`, `Content-Type` (belirli değerler), `Content-Language` header'ları.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: HTTP Cache Simülatörü

**Görev:** HTTP cache mekanizmasını simüle eden bir program yaz. Cache-Control header'ına göre cache'ten mi sunucudan mı yükleneceğine karar versin.

**Başlangıç kodu:**
```python
import time
import hashlib

class HTTPCache:
    def __init__(self):
        self.cache: dict[str, dict] = {}
        self.stats = {"hits": 0, "misses": 0, "revalidations": 0}

    def store(self, url: str, body: str, headers: dict):
        """Response'u cache'e kaydet."""
        # TODO:
        # 1. Cache-Control header'ini parse et (max-age, no-cache, no-store, must-revalidate)
        # 2. ETag olustur (body'nin hash'i)
        # 3. Cache'e kaydet: body, etag, stored_at, max_age, directives
        pass

    def get(self, url: str) -> dict:
        """
        Cache'ten response al.
        Returns: {"source": "cache"|"revalidate"|"network", "body": str, "age": int}
        """
        # TODO:
        # 1. Cache'te var mi kontrol et
        # 2. no-store ise her zaman network
        # 3. max-age suresini kontrol et
        # 4. Suresi dolmussa revalidation gerekir (ETag ile)
        pass

# Test
cache = HTTPCache()

# Farkli cache stratejileri
cache.store("/style.css", "body { color: red; }", {"Cache-Control": "max-age=31536000"})
cache.store("/api/users", '[{"id":1}]', {"Cache-Control": "no-cache"})
cache.store("/api/token", '{"token":"secret"}', {"Cache-Control": "no-store"})
cache.store("/index.html", "<html>...</html>", {"Cache-Control": "max-age=300"})

# Cache lookup
for url in ["/style.css", "/api/users", "/api/token", "/index.html", "/not-cached"]:
    result = cache.get(url)
    print(f"{url:20s} -> Source: {result['source']:12s} Age: {result.get('age', '-')}s")

print(f"\nStats: {cache.stats}")
```

**Beklenen çıktı:**
```
/style.css           -> Source: cache        Age: 0s
/api/users           -> Source: revalidate   Age: 0s
/api/token           -> Source: network      Age: -s
/index.html          -> Source: cache        Age: 0s
/not-cached          -> Source: network      Age: -s

Stats: {'hits': 2, 'misses': 2, 'revalidations': 1}
```

**İpucu:** `Cache-Control` header'ını `;` ile split et. `time.time()` ile stored timestamp'ı karşılaştır.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 9: URL Parser

**Görev:** Bir URL'i bileşenlerine ayıran bir parser yaz. Scheme, host, port, path, query parameters ve fragment'ı çıkarsın.

**Başlangıç kodu:**
```python
def parse_url(url: str) -> dict:
    """
    URL'i bilesenlerine ayir.
    Returns: {"scheme", "host", "port", "path", "query_params", "fragment"}
    """
    # TODO: Regex veya string islemleri ile parse et
    # Ornek: https://example.com:8080/api/users?page=1&limit=10#section2
    # scheme=https, host=example.com, port=8080, path=/api/users
    # query_params={"page": "1", "limit": "10"}, fragment=section2
    pass

# Test
urls = [
    "https://example.com:8080/api/users?page=1&limit=10#section2",
    "http://localhost:3000/",
    "https://google.com/search?q=python+tutorial&lang=tr",
    "ftp://files.example.com/docs/readme.txt",
    "https://api.github.com/repos/user/repo/issues?state=open&sort=created",
]

for url in urls:
    parsed = parse_url(url)
    print(f"\nURL: {url}")
    print(f"  Scheme: {parsed['scheme']}")
    print(f"  Host:   {parsed['host']}")
    print(f"  Port:   {parsed['port']}")
    print(f"  Path:   {parsed['path']}")
    print(f"  Query:  {parsed['query_params']}")
    print(f"  Fragment: {parsed.get('fragment', '')}")
```

**Beklenen çıktı:**
```
URL: https://example.com:8080/api/users?page=1&limit=10#section2
  Scheme: https
  Host:   example.com
  Port:   8080
  Path:   /api/users
  Query:  {'page': '1', 'limit': '10'}
  Fragment: section2
```

**İpucu:** `://` ile scheme'i, `:` ile port'u, `?` ile query'yi, `#` ile fragment'ı ayır. `urllib.parse` kullanmadan kendin yaz.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: HTTP Rate Limiter Simülasyonu

**Görev:** Bir HTTP API'nin rate limiting mekanizmasını simüle eden bir program yaz. Sliding window algoritması kullan.

**Başlangıç kodu:**
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> dict:
        """
        Istegin kabul edilip edilmeyecegini kontrol et.
        Returns: {
            "allowed": bool,
            "remaining": int,
            "reset_at": float,
            "retry_after": int | None,
            "headers": dict  # X-RateLimit-* headers
        }
        """
        # TODO:
        # 1. Mevcut zamani al
        # 2. Window disindaki eski istekleri temizle
        # 3. Mevcut istek sayisini kontrol et
        # 4. Izin veriliyorsa istegi kaydet
        # 5. Rate limit header'larini olustur
        pass

# Test: Dakikada 5 istek limiti
limiter = RateLimiter(max_requests=5, window_seconds=60)

# Ayni IP'den 7 istek simule et
for i in range(7):
    result = limiter.is_allowed("192.168.1.100")
    status = "ALLOWED" if result["allowed"] else "BLOCKED"
    print(f"Request {i+1}: {status} | "
          f"Remaining: {result['remaining']} | "
          f"X-RateLimit-Limit: {result['headers']['X-RateLimit-Limit']}")

# Farkli IP test
result = limiter.is_allowed("10.0.0.1")
print(f"\nFarkli IP: {'ALLOWED' if result['allowed'] else 'BLOCKED'} | Remaining: {result['remaining']}")
```

**Beklenen çıktı:**
```
Request 1: ALLOWED | Remaining: 4 | X-RateLimit-Limit: 5
Request 2: ALLOWED | Remaining: 3 | X-RateLimit-Limit: 5
Request 3: ALLOWED | Remaining: 2 | X-RateLimit-Limit: 5
Request 4: ALLOWED | Remaining: 1 | X-RateLimit-Limit: 5
Request 5: ALLOWED | Remaining: 0 | X-RateLimit-Limit: 5
Request 6: BLOCKED | Remaining: 0 | X-RateLimit-Limit: 5
Request 7: BLOCKED | Remaining: 0 | X-RateLimit-Limit: 5

Farkli IP: ALLOWED | Remaining: 4
```

**İpucu:** Her istek timestamp'ını listeye ekle. `time.time() - window_seconds`'tan eski kayıtları sil.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Content Negotiation Simülatörü

**Görev:** HTTP Content Negotiation mekanizmasını simüle eden bir program yaz. Accept header'a göre uygun format dönsün.

**Başlangıç kodu:**
```python
def negotiate_content(accept_header: str, available_types: list[str]) -> str | None:
    """Accept header'a gore en uygun content type'i sec."""
    # TODO:
    # 1. Accept header'i parse et (type/subtype;q=value)
    # 2. Quality factor'e gore sirala
    # 3. Available types ile eslestir
    # 4. En uygun type'i dondur
    pass

# Test
tests = [
    ("text/html, application/json;q=0.9, */*;q=0.1", ["application/json", "text/html", "text/xml"]),
    ("application/json", ["text/html", "application/json"]),
    ("application/xml;q=0.9, application/json;q=1.0", ["application/json", "application/xml"]),
    ("text/plain", ["application/json", "text/html"]),
]

for accept, available in tests:
    result = negotiate_content(accept, available)
    print(f"Accept: {accept[:50]:50s} -> {result or '406 Not Acceptable'}")
```

**Beklenen çıktı:**
```
Accept: text/html, application/json;q=0.9, */*;q=0.1  -> text/html
Accept: application/json                               -> application/json
Accept: application/xml;q=0.9, application/json;q=1.0  -> application/json
Accept: text/plain                                     -> 406 Not Acceptable
```

**İpucu:** Quality factor varsayılan 1.0'dır. `*/*` tüm tipleri kabul eder. Virgül ile ayrılan tipleri parse et.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 12: HTTP/2 Multiplexing Simülasyonu

**Görev:** HTTP/1.1 ile HTTP/2 multiplexing farkını gösteren bir simülasyon yaz.

**Başlangıç kodu:**
```python
import asyncio
import time

async def fetch_resource(name: str, size_kb: int, delay: float) -> dict:
    """Kaynak indirme simulasyonu."""
    await asyncio.sleep(delay)
    return {"name": name, "size": size_kb, "time": delay}

async def http11_sequential(resources: list[dict]) -> float:
    """HTTP/1.1: Kaynaklar sirayla indirilir (6 baglanti limiti)."""
    start = time.time()
    # TODO: Her kaynagi sirayla indir (max 6 paralel baglanti)
    for r in resources:
        await fetch_resource(r["name"], r["size"], r["delay"])
    return time.time() - start

async def http2_multiplexed(resources: list[dict]) -> float:
    """HTTP/2: Tum kaynaklar tek baglanti uzerinde paralel."""
    start = time.time()
    tasks = [fetch_resource(r["name"], r["size"], r["delay"]) for r in resources]
    await asyncio.gather(*tasks)
    return time.time() - start

# Test
resources = [
    {"name": "index.html", "size": 5, "delay": 0.1},
    {"name": "style.css", "size": 20, "delay": 0.15},
    {"name": "app.js", "size": 100, "delay": 0.3},
    {"name": "vendor.js", "size": 200, "delay": 0.4},
    {"name": "hero.webp", "size": 150, "delay": 0.25},
    {"name": "font.woff2", "size": 30, "delay": 0.1},
    {"name": "logo.svg", "size": 2, "delay": 0.05},
    {"name": "analytics.js", "size": 15, "delay": 0.1},
]

async def main():
    t1 = await http11_sequential(resources)
    t2 = await http2_multiplexed(resources)
    print(f"HTTP/1.1 (sirayla): {t1:.2f}s")
    print(f"HTTP/2 (paralel):   {t2:.2f}s")
    print(f"Hizlanma: {t1/t2:.1f}x")

asyncio.run(main())
```

**Beklenen çıktı:**
```
HTTP/1.1 (sirayla): 1.45s
HTTP/2 (paralel):   0.40s
Hizlanma: 3.6x
```

**İpucu:** `asyncio.gather()` tüm task'ları paralel çalıştırır. HTTP/2'nin avantajı tek TCP bağlantısında multiplexing yapmasıdır.

**Zorluk:** Zor
:::

:::must-note
- HTTP Methods: GET=oku, POST=oluştur, PUT=tamamen güncelle, PATCH=kısmen güncelle, DELETE=sil
- İdempotent: GET, PUT, DELETE (tekrar çağırsan aynı sonuç). POST idempotent DEĞİL!
- Safe: GET ve HEAD (sunucu verisini değiştirmez)
- Status: 200=OK, 201=Created, 204=No Content, 301=Moved Permanently, 304=Not Modified, 400=Bad Request, 401=Unauthorized (kimlik yok), 403=Forbidden (yetki yok), 404=Not Found, 409=Conflict, 429=Too Many Requests, 500=Server Error, 502=Bad Gateway, 503=Service Unavailable
- Content-Type: application/json (API), text/html (web sayfası), multipart/form-data (dosya upload), application/x-www-form-urlencoded (form)
- Authorization header formatları: Bearer token (JWT), Basic (Base64), ApiKey
- Cache-Control: no-store (hiç cache'leme), no-cache (cache'le ama sor), max-age=saniye, public vs private
- HTTP/1.1 = tek istek/bağlantı, HTTP/2 = multiplexing (tek bağlantıda çoklu istek), HTTP/3 = QUIC (UDP tabanlı, 0-RTT mümkün)
- HTTPS = HTTP + TLS şifreleme. TLS handshake: ClientHello → ServerHello → Certificate → Key Exchange
- CORS = sunucu tarafı ayar! Access-Control-Allow-Origin header'ını SUNUCU gönderir. Frontend'de çözülmez
- Preflight: Tarayıcı "basit olmayan" isteklerden önce otomatik OPTIONS gönderir
- Cookie güvenliği: HttpOnly (JS erişemez), Secure (sadece HTTPS), SameSite=Strict (CSRF koruması)
- PUT vs PATCH: PUT tüm alanları göndermelisin (göndermediğin silinir), PATCH sadece değişeni gönder
- 301/302 POST'u GET'e çevirebilir → POST yönlendirmesinde 307 veya 308 kullan
:::

:::senior-learns
**Senior Developer HTTP'yi Nasıl Öğrenir?**

- **Browser DevTools Network Tab:** Her request'in header'larını, timing breakdown'ını (DNS, TCP, TLS, TTFB, Content Download), response body'sini ve waterfall grafiğini inceler. "Copy as cURL" ile terminalde tekrar çalıştırır
- **curl ve httpie:** `curl -v` ile raw HTTP request/response'u görür. `httpie` (http komutu) ile daha okunabilir çıktı alır. Header'ları, redirect'leri, SSL sertifikalarını analiz eder
- **Wireshark:** TCP/TLS seviyesinde paketleri yakalar. TLS handshake sürecini, TCP window size'ı, retransmission'ları gözlemler. HTTP/2 frame'lerini inceler
- **Postman / Insomnia:** API'leri test ederken farklı method'ları, header'ları, body formatlarını dener. Collection oluşturup environment variable'lar ile çalışır
- **httpbin.org ve requestbin.com:** HTTP davranışlarını test eder - status code'ları, redirect'leri, delay'leri simüle eder. Request'in sunucuya nasıl göründüğünü görür
- **RFC okuma alışkanlığı:** RFC 7231 (HTTP Semantics), RFC 7540 (HTTP/2), RFC 9114 (HTTP/3) - en azından ilgili bölümlerini tarar. "Status code ne zaman kullanılır?" sorusunun cevabını spesifikasyondan öğrenir
- **Charles Proxy / mitmproxy:** Mobil uygulama ile sunucu arasındaki HTTP trafiğini yakalar ve analiz eder. HTTPS trafiğini decrypt ederek inceler
- **Gerçek production sorun çözme:** 502 alınca Nginx access/error log'larına bakar, upstream sunucunun durumunu kontrol eder. 429 alınca rate limit header'larını (X-RateLimit-Remaining, Retry-After) okur ve backoff stratejisi uygular
- **Performans analizi:** HTTP/2 Server Push'un gerçekten işe yarayıp yaramadığını test eder. Cache-Control stratejilerini lighthouse ile ölçer. Preflight request'lerin sayısını minimize etmek için CORS ayarlarını optimize eder
- **Yaklaşım farkı:** Senior sadece "200 döndü, çalışıyor" demez. Response time'ı, header'ların doğruluğunu, cache stratejisini, güvenlik header'larını (HSTS, X-Content-Type-Options, CSP) da kontrol eder
:::

:::english
**Teknik Ingilizce - Bu Dersteki Terimler:**

1. **Request** (rɪ-kwest) → Istek
   *"The client sends an HTTP request to the server to fetch user data."*

2. **Response** (rɪ-spɒns) → Yanit
   *"The server returns a JSON response with a 200 status code."*

3. **Header** (hed-ər) → Başlık
   *"Set the Content-Type header to application/json for API requests."*

4. **Stateless** (steɪt-ləs) → Durumsuz
   *"HTTP is a stateless protocol, meaning each request is independent."*

5. **Idempotent** (aɪ-dem-poh-tənt) → Idempotent / Etkisiz
   *"PUT is idempotent because sending the same request multiple times produces the same result."*

**Okuma Egzersizi:** MDN'de "An overview of HTTP" makalesini Ingilizce oku: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview

**Yazma Pratigi:** Aşağıdaki commit mesajini Ingilizce yaz: "Kullanıcı API endpoint'lerine CORS desteği eklendi"
→ Örnek: `feat: add CORS support to user API endpoints`
:::

:::external-resource
- 📺 **Traversy Media:** "HTTP Crash Course & Exploration" (YouTube, ücretsiz, ~35 dk)
- 📖 **MDN Web Docs:** "HTTP" bolumu (Ingilizce, ücretsiz, kapsamli referans)
- 🛠️ **httpbin.org:** HTTP isteklerini test etmek için interaktif arac (ücretsiz)
- 📖 **HTTP Status Codes:** httpstatuses.io (tüm status code'larin detayli aciklamasi, ücretsiz)
- 📺 **Hussein Nasser:** "HTTP/1.1 vs HTTP/2 vs HTTP/3" (YouTube, ücretsiz)
- 🛠️ **Postman:** API test araci - HTTP isteklerini görsel arayuzle gönder (ücretsiz plan mevcut)
:::
